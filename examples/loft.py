import cadscript as cad

sketch1 = cad.make_sketch()
sketch1.add_circle(d=10)

sketch2 = cad.make_sketch()
sketch2.add_rect(10, 10)

p1 = "XY"
p2 = cad.make_construction_plane("XY", offset=10)

body = cad.make_loft(p1, sketch1, p2, sketch2)

cad.show(body)
