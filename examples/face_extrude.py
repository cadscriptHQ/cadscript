import cadscript as cad

body1 = cad.make_box(10, 10, 10).chamfer(">Z", 2.5)
body2 = body1.copy()
body3 = body2.copy()

sketch = cad.make_sketch().add_circle(d=5)

body1.add_extrude(">Z", None, 5)
body2.add_extrude(">Z", sketch, 5)
body4 = body3.make_extrude(">Z", None, (2, 5))

body1.move((-12, 0, 0))
body3.move((12, 0, 0))
body4.move((12, 0, 0))

cad.show(body1.add(body2).add(body3).add(body4))
