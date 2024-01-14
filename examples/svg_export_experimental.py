import cadscript as cad
import docs.ext.svg as svg_exporter

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
    #"projectionDir": (-1.75, -2, 8),
    "showHidden": True,
    "width": 600,
    "height": 400,
    "focus": 200,
    "rotateAxis": "Z",
    "rotateAngle": -30,
}

style1 = {
    "visible": {
        "stroke": "rgb(90,90,90)",
        "stroke-width": ".2",
    },
    "hidden": None,
    "smooth_edges": {
        "stroke": "rgb(0,0,0)",
        "stroke-width": ".1",
    },
}
style2 = {
    "visible": {
        "stroke": "rgb(0,0,200)",
        "stroke-width": ".3",
    },
    "hidden": {
        "stroke": "rgb(160,160,255)",
        "stroke-width": "0.1",
        "stroke-dasharray": "0.15,0.15",
    },
    "smooth_edges": {
        "stroke": "rgb(0,0,200)",
        "stroke-width": ".1",
    },
}

shapes = [
    (plate1.cq().findSolid(), style1),
    (plate2.cq().findSolid(), style1),
    (peg.cq().findSolid(), style2),
]
out_svg = svg_exporter.get_svg(shapes, svg_options)

with open("private.svg", "w") as f:
    f.write(out_svg)
