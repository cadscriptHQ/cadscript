import cadscript

result = cadscript.make_box(30, 20, 4)
result.fillet("|Z", 3)
result.chamfer("#Z", 0.6)

sketch = cadscript.make_sketch()
sketch.add_rect(10, 10)
sketch.add_circle(diameter=10, positions=[(5, 0), (0, 5)])

result.cut_extrude(">Z", sketch.rotate(45), -4)

result.export_stl("heart.stl")
