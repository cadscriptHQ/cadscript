import re

import traceback

from pathlib import Path

from json import dumps

from cadquery import Assembly, Compound, Color, Sketch
from cadquery import cqgi
import cadquery
from cadquery.occ_impl.assembly import toJSON
from cadquery.occ_impl.jupyter_tools import DEFAULT_COLOR
from docutils.parsers.rst import directives

from cadquery.cq_directive import cq_directive_vtk, template_vtk, rendering_code

from docs.ext.svg import get_svg


prefix = """
import cadscript
import cadscript as cad
"""

postfix = """
result = {result_var}
if isinstance(result, cadscript.Sketch):
    sketch = result.cq()
    sketch.finalize()
    result = cadquery.Workplane("XY").placeSketch(sketch.clean()).extrude(0.001, False)
else:
    result = result.cq()
"""

template_img = """

.. raw:: html

    <div class="{html_class}">
        {out_svg}
    </div>
    <div style="clear:both;">
    </div>

"""


class cadscript_directive(cq_directive_vtk):

    option_spec = {
        "height": directives.length_or_unitless,
        "width": directives.length_or_percentage_or_unitless,
        "select": directives.unchanged,
        "interactive": directives.flag,
        "source": directives.path,
        "text_from_comment": directives.flag,
        "steps": directives.unchanged,
        "preset": directives.unchanged,
        "side-by-side": directives.flag,
    }

    def get_file(self, path):
        # get the absolute path of the file. If the file is not found, try to find it in parent directory
        file_path = Path(setup.confdir) / path
        file_path = file_path.resolve()
        if not file_path.exists():
            file_path = Path(setup.confdir.parent) / path
            file_path = file_path.resolve()
        # if the file is still not found, print error, then raise error
        if not file_path.exists():
            print("ERROR: File not found: ", path)
            print("confdir: ", setup.confdir)
            raise FileNotFoundError
        return file_path

    def run(self):
        options = self.options
        script = self.content
        state_machine = self.state_machine
        result_var = options.get("select", "result")
        text = ""
        pre_script = ""

        if "source" in options:
            # load the script from a file
            source_file = options["source"].strip()
            with open(self.get_file(source_file)) as f:
                content = f.read()
                pre_script, script, text = self.get_source_file(content, options.get("steps", None), "text_from_comment" in options)
        else:
            # else use inline code
            script = "\n".join(script)        

        # add the prefix and postfix
        plot_code = prefix + "\n" + pre_script + "\n" + script + "\n" + postfix.format(result_var=result_var)

        # collect the result
        lines = self.generate_output(plot_code, text, script, options)

        if len(lines):
            state_machine.insert_input(lines, state_machine.input_lines.source(0))

        return []

    def get_source_file(self, content, steps, text_from_comment):

        content = re.sub(r'^cadscript.show\(.*$', '', content, flags=re.MULTILINE)  # remove show() calls
        text = []
        pre_script = []
        content = content + "\n"  # fix problem with last line
        ellipsis = False

        # split script at lines starting with "#STEP"
        steps_sources = re.split(r'#\s?STEP.*\n', content)
        if steps:
            if steps.startswith("..."):
                steps = steps[3:]
                ellipsis = True

            if '-' in steps:
                start, end = steps.split('-')
                start = int(start)
                end = int(end) + 1
                script = steps_sources[start:end]
                pre_script = steps_sources[1:start]
            else:
                index = int(steps)
                script = [steps_sources[index]]
                pre_script = steps_sources[1:index]
        else:
            script = steps_sources[1:]  # skip everything before step 1

        if text_from_comment:
            # extract the text from the comment
            newscript = []
            last_comment = []
            for part in script:
                last_comment = []
                new_part = ""
                for line in part.split("\n")[:-1]:  # skip last empty item with [:-1]
                    if line.startswith("# "):
                        last_comment.append(line[2:])
                    elif line.startswith("#"):
                        last_comment.append(line[1:])
                    else:
                        new_part += line + "\n"
                newscript.append(new_part)
            script = newscript
            text = last_comment

        script = "".join(script)
        pre_script = "".join(pre_script)

        if ellipsis:
            script = "...\n" + script

        return pre_script, script, text

    def generate_output(self, plot_code, text, script, options):

        lines = []

        if len(text):
            lines.append("")
            lines.extend(text)
            lines.append("")

        if "side-by-side" in options:
            lines.append(".. raw:: html")
            lines.append("")
            lines.append("    <div class=\"side-by-side\"><div class=\"leftside\">")
            lines.append("")

        lines.extend(["", "::", ""])
        lines.extend(["    %s" % row.rstrip() for row in script.split("\n")])
        lines.append("")

        if "side-by-side" in options:
            lines.append(".. raw:: html")
            lines.append("")
            lines.append("    </div>")
            lines.append("")

        try:
            result = cqgi.parse(plot_code).build()

            if result.success:
                if result.first_result:
                    shape = result.first_result.shape
                else:
                    shape = result.env["result"]

                if isinstance(shape, Assembly):
                    assy = shape
                elif isinstance(shape, Sketch):
                    assy = Assembly(shape._faces, color=Color(*DEFAULT_COLOR))

                else:
                    assy = Assembly(shape, color=Color(*DEFAULT_COLOR))
            else:
                raise result.exception

            # add the output
            if "is_interactive" in options:
                # rendering as interactive 3d view with vtk.js
                render = self.render_vtk(assy, options)
            else:
                # rendering as image
                render = self.render_image(assy, options)
            lines.extend(render)

        except Exception:
            traceback.print_exc()
            assy = Assembly(Compound.makeText("CQGI error", 10, 5))

        if "side-by-side" in options:
            lines.append("")
            lines.append(".. raw:: html")
            lines.append("")
            lines.append("    </div>")
        lines.append("")

        return lines

    def render_vtk(self, assy, options):
        data = dumps(toJSON(assy))
        return template_vtk.format(
            data=data,
            element="document.currentScript.parentNode",
            width=options.get("width", "100%"),
            height=options.get("height", "500px"),
        ).splitlines()


    def render_image(self, assy, options):

        preset = options.get("preset", "3D")
        side_by_side = "side-by-side" in options
        out_svg = ""

        if preset == "3D":
            svg_options = {
                "projectionOrigin": (0, 0, 0),
                "projectionDir": (0, -10, 5),
                "projectionXDir": (1, 0, 0),
                "showHidden": True,
                "width": 400 if side_by_side else 600,
                "focus": 200,
                "rotateAxis": "Z",
                "rotateAngle": -30,
            }

            style1 = {
                "visible": {
                    "stroke": "rgb(0,0,0)",
                    "stroke-width": ".2",
                },
                "hidden": None,
                "smooth_edges": {
                    "stroke": "rgb(0,0,0)",
                    "stroke-width": "0.1",
                },
            }
            style2 = {
                "visible": {
                    "stroke": "rgb(100,100,255)",
                    "stroke-width": "0.1",
                },
                "hidden": {
                    "stroke": "rgb(100,100,255)",
                    "stroke-width": "0.02",
                },
            }
            axisX = cadquery.Workplane().moveTo(-30, 0).lineTo(30, 0)
            axisY = cadquery.Workplane().moveTo(0, -30).lineTo(0, 30)

            shapes = [
                (assy.toCompound(), style1),
                (cadquery.Shape(axisX.toOCC()), style2),
                (cadquery.Shape(axisY.toOCC()), style2),
            ]
            out_svg = get_svg(shapes, svg_options)
        else:
            raise Exception("Unknown preset: " + preset)

        out_svg = out_svg.replace("\n", "")

        return template_img.format(
            out_svg=out_svg,
            html_class="rightside" if "side-by-side" in options else "cq",
            width="100%",
            height="100%",
        ).splitlines()



class cadscript_auto_directive(cadscript_directive):

    option_spec = {
        "height": directives.length_or_unitless,
        "width": directives.length_or_percentage_or_unitless,
        "interactive": directives.flag,
        "source": directives.path,
        "preset": directives.unchanged,
        "side-by-side": directives.flag,
    }


    def run(self):
        options = self.options
        script = self.content
        state_machine = self.state_machine

        # load the script from a file
        source_file = options["source"].strip()
        with open(self.get_file(source_file)) as f:
            content = f.read()

            # get all lines starting with "#DOCSTEP"
            # get (step_string, result_var) tuples from the lines
            steps = re.findall(r'#\s?DOCSTEP:\s*(.*),(.*)$', content, flags=re.MULTILINE)

            lines = []
            for step, result_var in steps:
                pre_script, script, text = self.get_source_file(content, step, text_from_comment=True)
                # print("STEP: ", step)
                # print("SCRIPT: \n", script)
                # print("TEXT: \n", text)

                # add the prefix and postfix
                plot_code = prefix + "\n" + pre_script + "\n" + script + "\n" + postfix.format(result_var=result_var)

                # collect the result
                lines.extend(self.generate_output(plot_code, text, script, options))

            if len(lines):
                state_machine.insert_input(lines, state_machine.input_lines.source(0))

        return []


def setup(app):
    setup.app = app
    setup.config = app.config
    setup.confdir = app.confdir

    app.add_directive("cadquery", cq_directive_vtk)
    app.add_directive('cadscript', cadscript_directive)
    app.add_directive('cadscript-auto', cadscript_auto_directive)

    app.add_css_file("cadscript.css")

    # add vtk.js
    app.add_js_file("vtk.js")
    app.add_js_file(None, body=rendering_code)



if __name__ == "__main__":
    # debug helper
    c = cadscript_auto_directive(
        name="test", arguments=[],
        options={"source": "test", "steps": "2-14", "text_from_comment": True},
        content=[], lineno=1, content_offset=0, block_text="", state=None, state_machine=None)
    try:
        # create a dummy object with attribute confdir
        app = lambda: None
        app.config = None
        app.confdir = "."
        setup(app)
    except Exception:
        pass
    pre_script, script, text = c.get_source_file(open(c.get_file('./examples/bracket.py')).read(), "2", True)
    pre_script, script, text = c.get_source_file(open(c.get_file('./examples/getting_started.py')).read(), None, None)
