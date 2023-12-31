# Copyright (C) 2023 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

import cadscript

result = cadscript.make_box(30, 20, 4)
result.fillet("|Z", 3)
result.chamfer("#Z", 0.6)

sketch = cadscript.make_sketch()
sketch.add_rect(8, 8)
sketch.add_circle(diameter=8, positions=[(4, 0), (0, 4)])

result.cut_extrude(">Z", sketch.rotate(45), -4)

result.export_stl("build/heart.stl")
