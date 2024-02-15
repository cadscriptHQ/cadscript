# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

import unittest
import cadscript
from cadscript.interval import Interval2D


class SketchMirrorTest(unittest.TestCase):

    def test_sketch_mirror_x(self):
        s = cadscript.make_sketch()
        s.add_rect(10, 10, center=False)
        s.mirror("X")
        self.assertEqual(s.get_extent(), Interval2D(-10, 10, 0, 10))

    def test_sketch_mirror_y(self):
        s = cadscript.make_sketch()
        s.add_rect(10, 10, center=False)
        s.mirror("Y")
        self.assertEqual(s.get_extent(), Interval2D(0, 10, -10, 10))

    def test_sketch_mirror_x_no_copy(self):
        s = cadscript.make_sketch()
        s.add_rect(10, 10, center=False)
        s.mirror("X", copy_and_merge=False)
        self.assertEqual(s.get_extent(), Interval2D(-10, 0, 0, 10))

    def test_sketch_mirror_y_no_copy(self):
        s = cadscript.make_sketch()
        s.add_rect(10, 10, center=False)
        s.mirror("Y", copy_and_merge=False)
        self.assertEqual(s.get_extent(), Interval2D(0, 10, -10, 0))

    def test_invalid_axis(self):
        s = cadscript.make_sketch()
        s.add_rect(10, 10, center=False)
        with self.assertRaises(ValueError):
            s.mirror("A")  # invalid axis 


if __name__ == '__main__':
    unittest.main()
