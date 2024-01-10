# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

import cadscript as cad

sketch = cad.make_sketch()
sketch.add_rect(70, 5, center=False)
sketch.add_circle(d=26, positions=[(0,10)])
sketch.fillet(">>X[1]", 15)
sketch.cut_circle(d=12, positions=[(0,10)])
sketch.cut_rect(100, (-100,0), center="X")

sketch2 = cad.make_sketch()
sketch2.add_rect(70, 30)
sketch2.chamfer(">X", 10)
sketch2.add_rect(50, 20, center="Y")
sketch2.add_circle(d=30, positions=[(50,0)])
sketch2.cut_rect((-50,20), 16, center="Y")
sketch2.fillet("not <X", 4)
sketch2.cut_circle(d=16, positions=[(50,0)])

extr1 = cad.make_extrude("XZ", sketch, (-100, 100))
extr2 = cad.make_extrude("XY", sketch2, (-100, 100))

result = extr1.intersect(extr2)

cad.show(result) 


