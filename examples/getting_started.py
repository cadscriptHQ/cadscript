# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

import cadscript

# STEP 1
result = cadscript.make_box(40, 30, 4)
# STEP 2
result.fillet("|Z", 5)
# STEP 3
result.chamfer("#Z", 0.8)

# STEP 4
sketch = cadscript.make_sketch()
sketch.add_rect(12, 12)
# STEP 5
sketch.add_circle(diameter=12, positions=[(6, 0), (0, 6)])

# STEP 6
result.cut_extrude(">Z", sketch.rotate(45), -4)

cadscript.show(result)
