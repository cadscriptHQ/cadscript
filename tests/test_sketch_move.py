# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

import unittest
import cadscript


class SketchMoveTest(unittest.TestCase):

    def test_move(self):
        s = cadscript.make_sketch()
        s.add_circle(d=10)
        s.move((15, 5))
        dim = s.get_extent()
        self.assertAlmostEqual(dim.min_x, 10)
        self.assertAlmostEqual(dim.max_x, 20)
        self.assertAlmostEqual(dim.min_y, 0)
        self.assertAlmostEqual(dim.max_y, 10)

    def test_move_to_origin(self):
        s = cadscript.make_sketch()
        s.add_circle(d=10, pos=(10, 20))
        s.move_to_origin()
        dim = s.get_extent()
        self.assertAlmostEqual(dim.min_x, 0)
        self.assertAlmostEqual(dim.max_x, 10)
        self.assertAlmostEqual(dim.min_y, 0)
        self.assertAlmostEqual(dim.max_y, 10)

        s = cadscript.make_sketch()
        s.add_circle(r=5, pos=(-10, -20))
        s.move_to_origin("X")
        dim = s.get_extent()
        self.assertAlmostEqual(dim.min_x, 0)
        self.assertAlmostEqual(dim.max_x, 10)
        self.assertAlmostEqual(dim.min_y, -25)
        self.assertAlmostEqual(dim.max_y, -15)

    def test_move_to_origin_y(self):
        s = cadscript.make_sketch()
        s.add_circle(r=5)
        s.move_to_origin("Y")
        dim = s.get_extent()
        self.assertAlmostEqual(dim.min_x, -5)
        self.assertAlmostEqual(dim.max_x, 5)
        self.assertAlmostEqual(dim.min_y, 0)
        self.assertAlmostEqual(dim.max_y, 10)

    def test_move_to_origin_false(self):
        s = cadscript.make_sketch()
        s.add_circle(r=5)
        s.move_to_origin(False)
        dim = s.get_extent()
        self.assertAlmostEqual(dim.min_x, -5)
        self.assertAlmostEqual(dim.max_x, 5)
        self.assertAlmostEqual(dim.min_y, -5)
        self.assertAlmostEqual(dim.max_y, 5)

    def test_center(self):
        s = cadscript.make_sketch()
        s.add_circle(r=5, pos=(10, 10))
        s.center()
        dim = s.get_extent()
        self.assertAlmostEqual(dim.min_x, -5)
        self.assertAlmostEqual(dim.max_x, 5)
        self.assertAlmostEqual(dim.min_y, -5)
        self.assertAlmostEqual(dim.max_y, 5)


    def test_center_x(self):
        s = cadscript.make_sketch()
        s.add_circle(r=5, pos=(10, 10))
        s.center(center="X")
        dim = s.get_extent()
        self.assertAlmostEqual(dim.min_x, -5)
        self.assertAlmostEqual(dim.max_x, 5)
        self.assertAlmostEqual(dim.min_y, 5)
        self.assertAlmostEqual(dim.max_y, 15)


    def test_center_y(self):
        s = cadscript.make_sketch()
        s.add_circle(r=5, pos=(10, 10))
        s.center(center="Y")
        dim = s.get_extent()
        self.assertAlmostEqual(dim.min_x, 5)
        self.assertAlmostEqual(dim.max_x, 15)
        self.assertAlmostEqual(dim.min_y, -5)
        self.assertAlmostEqual(dim.max_y, 5)

    def test_center_false(self):
        s = cadscript.make_sketch()
        s.add_circle(r=5, pos=(10, 10))
        s.center(center=False)
        dim = s.get_extent()
        self.assertAlmostEqual(dim.min_x, 5)
        self.assertAlmostEqual(dim.max_x, 15)
        self.assertAlmostEqual(dim.min_y, 5)
        self.assertAlmostEqual(dim.max_y, 15)


if __name__ == '__main__':
    unittest.main()
