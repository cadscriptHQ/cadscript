import cadscript as cad
import cadscript.exporters.svg as svg_exporter

s = cad.make_sketch()
s.add_rect(40, 20)
s.cut_circle(d=6)

plate1 = cad.make_extrude("XY", s, -4)
plate2 = cad.make_extrude("XY", s.rotate(90), (-8, -4))

peg = cad.make_extrude("XY", cad.make_sketch().add_circle(d=6), -20)
peg = peg.add(cad.make_extrude("XY", cad.make_sketch().add_circle(d=10), 5))

svg_options = {
    "projectionDir": (-1.75, 4, 1),
    "showHidden": True,
    "width": 600,
    "height": 400,
}

style1 = {
    "visible": {
        "stroke": "rgb(90,90,90)",
        "stroke-width": ".2",
    },
    "hidden": {
        "stroke": "rgb(160,160,160)",
        "stroke-width": "0.1",
        "stroke-dasharray": "0.15,0.15",
    },
}
style2 = {
    "visible": {
        "stroke": "rgb(200,0,0)",
        "stroke-width": ".3",
    },
    "hidden": {
        "stroke": "rgb(255,160,160)",
        "stroke-width": "0.1",
        "stroke-dasharray": "0.15,0.15",
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
