import cadscript
import traceback

from json import dumps

from cadquery import exporters, Assembly, Compound, Color, Sketch
from cadquery import cqgi
from cadquery.occ_impl.assembly import toJSON
from cadquery.occ_impl.jupyter_tools import DEFAULT_COLOR
from docutils.parsers.rst import directives, Directive

from cadquery.cq_directive import cq_directive_vtk, template_vtk, rendering_code


prefix = """
import cadscript
"""

postfix = """
result = result.cq()
"""

class cadscript_directive(cq_directive_vtk):

    option_spec = {
        "height": directives.length_or_unitless,
        "width": directives.length_or_percentage_or_unitless,
        "align": directives.unchanged,
        "select": directives.unchanged,
      }
    
    def run(self):
          options = self.options
          content = self.content
          state_machine = self.state_machine

          # only consider inline snippets
          script = "\n".join(content)
          plot_code = prefix + "\n" + script + "\n" + postfix

          # collect the result
          try:
              result = cqgi.parse(plot_code).build()

              if result.success:
                  if result.first_result:
                      shape = result.first_result.shape
                  else:
                      shape = result.env[options.get("select", "result")]

                  if isinstance(shape, Assembly):
                      assy = shape
                  elif isinstance(shape, Sketch):
                      assy = Assembly(shape._faces, color=Color(*DEFAULT_COLOR))
                  else:
                      assy = Assembly(shape, color=Color(*DEFAULT_COLOR))
              else:
                  raise result.exception

          except Exception:
              traceback.print_exc()
              assy = Assembly(Compound.makeText("CQGI error", 10, 5))

          # add the output
          lines = []

          data = dumps(toJSON(assy))

          lines.extend(
              template_vtk.format(
                  data=data,
                  element="document.currentScript.parentNode",
                  txt_align=options.get("align", "left"),
                  width=options.get("width", "100%"),
                  height=options.get("height", "500px"),
              ).splitlines()
          )

          lines.extend(["::", ""])
          lines.extend(["    %s" % row.rstrip() for row in script.split("\n")])
          lines.append("")

          if len(lines):
              state_machine.insert_input(lines, state_machine.input_lines.source(0))

          return []

def setup(app):
    setup.app = app
    setup.config = app.config
    setup.confdir = app.confdir

    app.add_directive("cadquery", cq_directive_vtk)
    app.add_directive('cadscript', cadscript_directive)

    # add vtk.js
    app.add_js_file("vtk.js")
    app.add_js_file(None, body=rendering_code)


