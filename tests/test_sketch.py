# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

import unittest
import cadscript


class SketchTest(unittest.TestCase):

    def test_ellipse_extend_uncentered(self):
        s = cadscript.make_sketch()
        s.add_ellipse(20, 10, center=False)
        (xmin, xmax), (ymin, ymax) = s.get_extent()
        self.assertAlmostEqual(xmin, 0)
        self.assertAlmostEqual(xmax, 20)
        self.assertAlmostEqual(ymin, 0)
        self.assertAlmostEqual(ymax, 10)

    def test_ellipse_extend_centered(self):
        s = cadscript.make_sketch()
        s.add_ellipse(20, 10, center=True)
        (xmin, xmax), (ymin, ymax) = s.get_extent()
        self.assertAlmostEqual(xmin, -10)
        self.assertAlmostEqual(xmax, 10)
        self.assertAlmostEqual(ymin, -5)
        self.assertAlmostEqual(ymax, 5)

    def test_ellipse_extend_rotated90(self):
        s = cadscript.make_sketch()
        s.add_ellipse(20, 10, angle=90)
        (xmin, xmax), (ymin, ymax) = s.get_extent()
        self.assertAlmostEqual(xmin, -5)
        self.assertAlmostEqual(xmax, 5)
        self.assertAlmostEqual(ymin, -10)
        self.assertAlmostEqual(ymax, 10)


if __name__ == '__main__':
    unittest.main()
