# Copyright (C) 2023 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

import cadscript

#STEP 1
result = cadscript.make_box(30, 20, 4)
#STEP 2
result.fillet("|Z", 3)
#STEP 3
result.chamfer("#Z", 0.6)

#STEP 4
sketch = cadscript.make_sketch()
sketch.add_rect(8, 8)
#STEP 5
sketch.add_circle(diameter=8, positions=[(4, 0), (0, 4)])

#STEP 6
result.cut_extrude(">Z", sketch.rotate(45), -4)

cadscript.show(result) 


