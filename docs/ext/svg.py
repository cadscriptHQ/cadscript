# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

# This file is based on the cadquery exporters/svg.py file
# Copyright (C) 2015  Parametric Products Intellectual Holdings, LLC

# It uses improvements similarily implemented by Pieter Hijma in osh-autodoc
# https://forum.freecad.org/viewtopic.php?t=79648


import io as StringIO

from cadquery.occ_impl.shapes import Shape, Compound, TOLERANCE


from OCP.gp import gp_Ax2, gp_Pnt, gp_Dir
from OCP.BRepLib import BRepLib
from OCP.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape
from OCP.HLRAlgo import HLRAlgo_Projector
from OCP.GCPnts import GCPnts_QuasiUniformDeflection

DISCRETIZATION_TOLERANCE = 1e-3

SVG_TEMPLATE = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   width="%(width)s"
   height="%(height)s"

>
    <g transform="scale(%(unitScale)s, -%(unitScale)s) translate(%(xTranslate)s,%(yTranslate)s)" fill="none">
       <!-- lines -->
%(content)s
    </g>
</svg>
"""

SVG_PATH_TEMPLATE = """
    <path %(attributes)s fill="none"
          d="%(content)s"></path>
"""



class UNITS:
    MM = "mm"
    IN = "in"




def makeSVGedge(e, style):
    """
    Creates an SVG edge from a OCCT edge.
    """

    svg = ""

    curve = e._geomAdaptor()  # adapt the edge into curve
    start = curve.FirstParameter()
    end = curve.LastParameter()

    points = GCPnts_QuasiUniformDeflection(curve, DISCRETIZATION_TOLERANCE, start, end)

    if points.IsDone():
        cs = StringIO.StringIO()
        point_it = (points.Value(i + 1) for i in range(points.NbPoints()))

        p = next(point_it)
        cs.write("M{},{} ".format(p.X(), p.Y()))

        for p in point_it:
            cs.write("L{},{} ".format(p.X(), p.Y()))

        svg = SVG_PATH_TEMPLATE % (
            {
                "attributes": " ".join([f'{k}="{v}"' for k, v in style.items()]),
                "content": cs.getvalue(),
            }
        )
    return svg


def getPaths(lines_list):
    """
    Collects the visible and hidden edges from the CadQuery object.
    """
    svg_lines = []
    for (lines, style) in lines_list:
        for e in Shape(lines).Edges():
            svg_lines.append(makeSVGedge(e, style))

    return svg_lines


def get_svg(shape, opts=None):
    """
    Export a shape to SVG text.

    :param shape: A CadQuery shape object to convert to an SVG string.
    :type Shape: Vertex, Edge, Wire, Face, Shell, Solid, or Compound.
    :param opts: An options dictionary that influences the SVG that is output.
    :type opts: Dictionary, keys are as follows:
        width: Width of the resulting image (None to fit based on height).
        height: Height of the resulting image (None to fit based on width).
        marginLeft: Inset margin from the left side of the document.
        marginTop: Inset margin from the top side of the document.
        projectionOrigin:
        projectionDir:
        projectionXDir:

        showAxes: Whether or not to show the axes indicator, which will only be
                  visible when the projectionDir is also at the default.
        strokeWidth: Width of the line that visible edges are drawn with.
        strokeColor: Color of the line that visible edges are drawn with.
        hiddenColor: Color of the line that hidden edges are drawn with.
        showHidden: Whether or not to show hidden lines.
        focus: If specified, creates a perspective SVG with the projector
               at the distance specified.
    """

    # Available options and their defaults
    options = {
        "width": 800,
        "height": 240,
        "marginLeft": 20,
        "marginTop": 20,
        "projectionOrigin": (0, 0, 0),
        "projectionDir": (-1.75, 1.1, 5),
        "projectionXDir": (1, 0, 0),
        "showAxes": True,
        "showHidden": True,
        "focus": None,
        "rotateAxis": "Z",
        "rotateAngle": 0,
    }

    if opts:
        options.update(opts)

    uom = UNITS.MM

    # Handle the case where the height or width are None
    width = options["width"]
    if width is not None:
        width = float(options["width"])
    height = options["height"]
    if options["height"] is not None:
        height = float(options["height"])
    marginLeft = float(options["marginLeft"])
    marginTop = float(options["marginTop"])
    projectionOrigin = tuple(options["projectionOrigin"])
    projectionDir = tuple(options["projectionDir"])
    projectionXDir = tuple(options["projectionXDir"])
    rotateAxis = options["rotateAxis"]
    rotateAngle = float(options["rotateAngle"])

    showAxes = bool(options["showAxes"])
    showHidden = bool(options["showHidden"])
    focus = float(options["focus"]) if options.get("focus") else None

    default_style = {
        "visible": {
            "stroke": "rgb(0,0,0)",
            "stroke-width": ".2",
        },
        "hidden": {
            "stroke": "rgb(160,160,160)",
            "stroke-width": "0.1",
            "stroke-dasharray": "0.15,0.15",
        },
    }

    transform = lambda s: s
    if rotateAngle != 0:
        rot_p1 = (0, 0, 0)
        if rotateAxis == "X":
            rot_p2 = (1, 0, 0)
        elif rotateAxis == "Y":
            rot_p2 = (0, 1, 0)
        elif rotateAxis == "Z":
            rot_p2 = (0, 0, 1)
        else:
            raise ValueError("Invalid rotateAxis value")

        transform = lambda s: s.rotate(rot_p1, rot_p2, rotateAngle)

    shapes = []
    styles = []
    # test if shape is list of tupes
    if isinstance(shape, list):
        for (s, style) in shape:
            shapes.append(transform(s))
            styles.append(style)
    else:
        shapes.append(transform(shape))
        styles.append(default_style)


    coordinate_system = gp_Ax2(gp_Pnt(*projectionOrigin), gp_Dir(*projectionDir), gp_Dir(*projectionXDir))

    if focus is not None:
        projector = HLRAlgo_Projector(coordinate_system, focus)
    else:
        projector = HLRAlgo_Projector(coordinate_system)

    hlr = HLRBRep_Algo()
    for s in shapes:
        hlr.Add(s.wrapped)
    hlr.Projector(projector)
    hlr.Update()
    hlr.Hide()

    hlr_shapes = HLRBRep_HLRToShape(hlr)

    lines_list = []  # list of lines as tuples of (lines, style)

    # add hidden lines first (so they are in the background)
    if showHidden:
        for i, shape in enumerate(shapes):
            shape = shape.wrapped
            style = styles[i]["hidden"]
            if style is not None:
                lines_list.append((hlr_shapes.HCompound(shape), style))  # hidden sharp edges
                lines_list.append((hlr_shapes.OutLineHCompound(shape), style))  # hidden contour edges

    # then add visible lines
    for i, shape in enumerate(shapes):
        shape = shape.wrapped
        if styles[i].get("smooth_edges"):
            style = styles[i]["smooth_edges"]
        else:
            style = styles[i]["visible"]  # fallback to visible style
        if style is not None:
            lines_list.append((hlr_shapes.Rg1LineVCompound(shape), style))  # smooth edges
        style = styles[i]["visible"]
        if style is not None:
            lines_list.append((hlr_shapes.VCompound(shape), style))  # sharp edges
            lines_list.append((hlr_shapes.OutLineVCompound(shape), style))  # contour edges

    # Fix the underlying geometry - otherwise we will get segfaults
    for (lines, style) in lines_list:
        if lines is not None:
            BRepLib.BuildCurves3d_s(lines, TOLERANCE)

    # filter out empty items
    lines_list = [(lines, style)
                  for (lines, style)
                  in lines_list
                  if lines is not None and not lines.IsNull()]

    svg_paths = getPaths(lines_list)
    content = "\n".join(svg_paths)

    # get bounding box -- these are all in 2D space
    bb = Compound.makeCompound([Shape(lines) for (lines, _) in lines_list]).BoundingBox()

    # Determine whether the user wants to fit the drawing to the bounding box
    if width is None or height is None:
        # Fit image to specified width (or height)
        if width is None:
            width = (height - (2.0 * marginTop)) * (
                bb.xlen / bb.ylen
            ) + 2.0 * marginLeft
        else:
            height = (width - 2.0 * marginLeft) * (bb.ylen / bb.xlen) + 2.0 * marginTop

        # width pixels for x, height pixels for y
        unitScale = (width - 2.0 * marginLeft) / bb.xlen
    else:
        bb_scale = 0.75
        # width pixels for x, height pixels for y
        unitScale = min(width / bb.xlen * bb_scale, height / bb.ylen * bb_scale)

    # compute amount to translate-- move the top left into view
    (xTranslate, yTranslate) = (
        (0 - bb.xmin) + marginLeft / unitScale,
        (0 - bb.ymax) - marginTop / unitScale,
    )

    svg = SVG_TEMPLATE % (
        {
            "unitScale": str(unitScale),
            "content": content,
            "xTranslate": str(xTranslate),
            "yTranslate": str(yTranslate),
            "width": str(width),
            "height": str(height),
            "textboxY": str(height - 30),
            "uom": str(uom),
        }
    )

    return svg


if __name__ == "__main__":

    import cadquery as cq
    import cadscript as cad

    s = cad.make_sketch()
    s.add_rect(40, 20)
    s.cut_circle(d=6)

    plate1 = cad.make_extrude("XY", s, -4).chamfer("|Z and >X", 5)
    plate2 = cad.make_extrude("XY", s.rotate(90), (-8, -4)).fillet("|Z", 2)

    peg = cad.make_extrude("XY", cad.make_sketch().add_circle(d=6), -20)
    peg = peg.add(cad.make_extrude("XY", cad.make_sketch().add_circle(d=10), 5))

    svg_options = {
        "projectionOrigin": (0, 0, 0),
        "projectionDir": (0, -10, 5),
        "projectionXDir": (1, 0, 0),
        "showHidden": True,
        "width": 600,
        "height": 400,
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

    axisX = cq.Workplane().moveTo(-30, 0).lineTo(30, 0)
    axisY = cq.Workplane().moveTo(0, -30).lineTo(0, 30)

    a = cad.Assembly()
    a.add(plate1)
    a.add(plate2)
    a.add(peg)

    shapes = [
        (a.cq().toCompound(), style1),
        (cq.Shape(axisX.toOCC()), style2),
        (cq.Shape(axisY.toOCC()), style2),
    ]
    out_svg = get_svg(shapes, svg_options)

    with open("private.svg", "w") as f:
        f.write(out_svg)
