# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

import unittest
import cadscript


class SketchTest(unittest.TestCase):

    def test_ellipse_extend_uncentered(self):
        s = cadscript.make_sketch()
        s.add_ellipse(20, 10, center=False)
        dim = s.get_extent()
        self.assertAlmostEqual(dim.min_x, 0)
        self.assertAlmostEqual(dim.max_x, 20)
        self.assertAlmostEqual(dim.min_y, 0)
        self.assertAlmostEqual(dim.max_y, 10)

    def test_ellipse_extend_centered(self):
        s = cadscript.make_sketch()
        s.add_ellipse(20, 10, center=True)
        dim = s.get_extent()
        self.assertAlmostEqual(dim.min_x, -10)
        self.assertAlmostEqual(dim.max_x, 10)
        self.assertAlmostEqual(dim.min_y, -5)
        self.assertAlmostEqual(dim.max_y, 5)

    def test_ellipse_extend_rotated90(self):
        s = cadscript.make_sketch()
        s.add_ellipse(20, 10, angle=90)
        dim = s.get_extent()
        self.assertAlmostEqual(dim.min_x, -5)
        self.assertAlmostEqual(dim.max_x, 5)
        self.assertAlmostEqual(dim.min_y, -10)
        self.assertAlmostEqual(dim.max_y, 10)


if __name__ == '__main__':
    unittest.main()
