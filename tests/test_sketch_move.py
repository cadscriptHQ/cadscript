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
        (xmin, xmax), (ymin, ymax) = s.get_extent()
        self.assertAlmostEqual(xmin, 10)
        self.assertAlmostEqual(xmax, 20)
        self.assertAlmostEqual(ymin, 0)
        self.assertAlmostEqual(ymax, 10)

    def test_move_to_origin(self):
        s = cadscript.make_sketch()
        s.add_circle(d=10, pos=(10, 20))
        s.move_to_origin()
        (xmin, xmax), (ymin, ymax) = s.get_extent()
        self.assertAlmostEqual(xmin, 0)
        self.assertAlmostEqual(xmax, 10)
        self.assertAlmostEqual(ymin, 0)
        self.assertAlmostEqual(ymax, 10)

        s = cadscript.make_sketch()
        s.add_circle(r=5, pos=(-10, -20))
        s.move_to_origin("X")
        (xmin, xmax), (ymin, ymax) = s.get_extent()
        self.assertAlmostEqual(xmin, 0)
        self.assertAlmostEqual(xmax, 10)
        self.assertAlmostEqual(ymin, -25)
        self.assertAlmostEqual(ymax, -15)

    def test_move_to_origin_y(self):
        s = cadscript.make_sketch()
        s.add_circle(r=5)
        s.move_to_origin("Y")
        (xmin, xmax), (ymin, ymax) = s.get_extent()
        self.assertAlmostEqual(xmin, -5)
        self.assertAlmostEqual(xmax, 5)
        self.assertAlmostEqual(ymin, 0)
        self.assertAlmostEqual(ymax, 10)
        
    def test_move_to_origin_false(self):
        s = cadscript.make_sketch()
        s.add_circle(r=5)
        s.move_to_origin(False)
        (xmin, xmax), (ymin, ymax) = s.get_extent()
        self.assertAlmostEqual(xmin, -5)
        self.assertAlmostEqual(xmax, 5)
        self.assertAlmostEqual(ymin, -5)
        self.assertAlmostEqual(ymax, 5)
    
    def test_center(self):
        s = cadscript.make_sketch()
        s.add_circle(r=5, pos=(10, 10))
        s.center()
        (xmin, xmax), (ymin, ymax) = s.get_extent()
        self.assertAlmostEqual(xmin, -5)
        self.assertAlmostEqual(xmax, 5)
        self.assertAlmostEqual(ymin, -5)
        self.assertAlmostEqual(ymax, 5)


    def test_center_x(self):
        s = cadscript.make_sketch()
        s.add_circle(r=5, pos=(10, 10))
        s.center(center="X")
        (xmin, xmax), (ymin, ymax) = s.get_extent()
        self.assertAlmostEqual(xmin, -5)
        self.assertAlmostEqual(xmax, 5)
        self.assertAlmostEqual(ymin, 5)
        self.assertAlmostEqual(ymax, 15)


    def test_center_y(self):
        s = cadscript.make_sketch()
        s.add_circle(r=5, pos=(10, 10))
        s.center(center="Y")
        (xmin, xmax), (ymin, ymax) = s.get_extent()
        self.assertAlmostEqual(xmin, 5)
        self.assertAlmostEqual(xmax, 15)
        self.assertAlmostEqual(ymin, -5)
        self.assertAlmostEqual(ymax, 5)

    def test_center_false(self):
        s = cadscript.make_sketch()
        s.add_circle(r=5, pos=(10, 10))
        s.center(center=False)
        (xmin, xmax), (ymin, ymax) = s.get_extent()
        self.assertAlmostEqual(xmin, 5)
        self.assertAlmostEqual(xmax, 15)
        self.assertAlmostEqual(ymin, 5)
        self.assertAlmostEqual(ymax, 15)


if __name__ == '__main__':
    unittest.main()
