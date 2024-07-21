import cadscript as cad

sketch = cad.make_sketch()
sketch.add_slot(start=(10, 2), end=(10, 10), radius=2)

rev = cad.make_revolve("Z", sketch, angle=(10, 90))

base = cad.make_box(25, 25, (-1, 0))

cad.show(base.add(rev))
