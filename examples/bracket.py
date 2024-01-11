# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

# this is used by the documentation generation
# DOCSTEP: 2,sketch1
# DOCSTEP: ...3,sketch1
# DOCSTEP: ...4,sketch1
# DOCSTEP: ...5,sketch1
# DOCSTEP: ...6,sketch1
# DOCSTEP: ...7,sketch1
# DOCSTEP: 8,sketch2
# DOCSTEP: ...9,sketch2
# DOCSTEP: ...10,sketch2
# DOCSTEP: 11,extr1
# DOCSTEP: 12,extr2
# DOCSTEP: ...13,result
# DOCSTEP: 2-14,result

# STEP 1
import cadscript

# STEP 2
# Let's start with a sketch.
# We add a rectangle with width 70 and height 30, centered at the origin.
sketch1 = cadscript.make_sketch()
sketch1.add_rect(70, 30)
# STEP 3
# Now we add a chamfer. ">X" selects all vertices with maximum X coordinate.
# This will add a chamfer at the corners at the right side of the rectangle.
# The chamfer will be 10mm long.
sketch1.chamfer(">X", 10)
# STEP 4
# We add another rectangle, this time with width 50 and height 20.
# This time, the centering is done along the Y axis only.
# The new rectangle will be "added", that is, it will be unioned with the first rectangle.
# After that we add a circle with diameter 30, its center at x=50,y=0.
sketch1.add_rect(50, 20, center="Y")
sketch1.add_circle(d=30, pos=(50, 0))
# STEP 5
# Now we cut a rectangle from the sketch.
# The dimension in x direction is here given by a tuple.
# The first value is the start position, the second value is the end position.
# In y direction, the dimension is 16mm.
# It will be centered, so it will range from -8 to +8 in y direction.
sketch1.cut_rect((-50, 20), 16, center="Y")
# STEP 6
# Now we do a couple of fillets. "<X" selects all vertices with minimum X coordinate.
# You can invert that by using "not <X", which selects all vertices but the ones with minimum X coordinate.
sketch1.fillet("not <X", 4)
# STEP 7
# Cutting a circle from the sketch, centered at x=50, y=0 with diameter 16.
sketch1.cut_circle(d=16, pos=(50, 0))

# STEP 8
# Make a new sketch, add a rectangle and a circle.
sketch2 = cadscript.make_sketch()
sketch2.add_rect(70, 5, center=False)
sketch2.add_circle(d=26, pos=(0, 10))
# STEP 9
# We add a fillet now. We want only the point where the circle and the rectangle meet.
# The search string ">>X" sorts all vertices in positive X direction.
# The "[1]" selects the second vertex in that list, which is the one we want.
sketch2.fillet(">>X[1]", 15)
# STEP 10
# Now we cut a circle and a rectangle from the sketch
# The circle is centered at x=0,y=10 with diameter 12.
# The rectangle ranges from -50 to 50 in x direction
# and -100 to 0 in y direction, effectively cutting off the lower half of the sketch.
sketch2.cut_circle(d=12, pos=(0, 10))
sketch2.cut_rect(100, (-100, 0), center="X")

# STEP 11
# Now we place the first sketch on the XY plane and make an extrusion.
# The extrusion will happen perpendicular to the plane, that is, in positive Z direction.
# The extrusion amount is given as a tuple,
# the first value is the start position, the second value is the end position.
extr1 = cadscript.make_extrude("XY", sketch1, (-100, 100))
# STEP 12
# Now we do the same for the second sketch.
# We use the XZ plane this time, so the extrusion will happen in Y direction.
extr2 = cadscript.make_extrude("XZ", sketch2, (-100, 100))

# STEP 13
# Finally, we intersect the two extrusions.
# This performs a boolean intersection of the two bodies.
result = extr2.intersect(extr1)

# STEP 14 dummy step to show whole script in documentation
# The complete script looks like this:

cadscript.show(result)
