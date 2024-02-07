import cadscript as cad

box = cad.make_box(50, 20, 20)

box.cut_hole(">Z", d=5, depth=10, pos=(-15, 0))
box.cut_hole(">Z", d=5, countersink_angle=90, d2=10)
box.cut_hole(">Z", d=5, counterbore_depth=5, d2=10, pos=(15, 0))


cad.show(box)
