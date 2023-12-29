'''
Copyright (C) 2023 Andreas Kahler
This file is part of Cadscript
SPDX-License-Identifier: Apache-2.0
'''

import cadscript as cad

def make_beam(length, hole_spacing, long_axis_hole_dia, mounting_holes_dia):
    # Construct the overall shape
    beam = cad.make_box(20, 20, length)
    beam = beam.fillet("|Z", 2.0)

    # Long-axis hole for connecting multiple leg sections together
    long_axis_hole = cad.make_sketch()
    long_axis_hole.add_circle(d=long_axis_hole_dia)
    beam = beam.cut_extrude(">Z", long_axis_hole, -length)
    
    # Channel cutouts
    sketch = cad.make_sketch()
    sketch.add_polygon([(-2.5, -1.5), (-5, 1.5), (5, 1.5), (2.5, -1.5)])
    for angle in [0,90,180,270]:
        s = sketch.copy().move((0,10)).rotate(angle)
        beam.cut_extrude("<Z", s, -length)

    # Mounting holes
    mount_hole_ptn = cad.pattern_grid(1, 21, spacing_y = hole_spacing)
    sketch = cad.make_sketch()
    sketch.add_circle(d=mounting_holes_dia, positions = mount_hole_ptn)

    beam.cut_extrude("<Y", sketch, -20.0)
    beam.cut_extrude("<X", sketch, -20.0)

    return beam

beam = make_beam(length = 294, hole_spacing = 14, long_axis_hole_dia = 4.6, mounting_holes_dia = 3.6)
beam.export_stl("beam.stl")