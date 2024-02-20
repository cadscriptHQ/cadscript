# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

import unittest

from cadscript.interval import Interval1D, Interval2D, Interval3D


class Interval1DTest(unittest.TestCase):

    def test_interval1d_properties(self):
        interval = Interval1D(1, 3)
        self.assertEqual(interval.min, 1)
        self.assertEqual(interval.max, 3)
        self.assertEqual(interval.x1, 1)
        self.assertEqual(interval.x2, 3)
        self.assertEqual(interval.size, 2)
        self.assertEqual(interval.center, 2)
        self.assertEqual(interval.tuple, (1, 3))

    def test_interval1d_from_tuple(self):
        interval = Interval1D.from_tuple((1, 3))
        self.assertEqual(interval.min, 1)
        self.assertEqual(interval.max, 3)

    def test_interval1d_set(self):
        interval = Interval1D(10, 20)
        interval.set(1, 3)
        self.assertEqual(interval.min, 1)
        self.assertEqual(interval.max, 3)

    def test_interval1d_copy(self):
        interval = Interval1D(10, 20)
        interval2 = interval.copy()
        interval2.set(1, 3)
        self.assertNotEqual(interval.min, interval2.min)
        self.assertNotEqual(interval.max, interval2.max)

    def test_interval1d_eq(self):
        self.assertTrue(Interval1D(10, 20) == Interval1D(10, 20))
        self.assertTrue(Interval1D(10, 20) != Interval1D(11, 20))
        self.assertTrue(Interval1D(10, 20) != Interval1D(10, 21))

    def test_interval1d_expand(self):
        interval = Interval1D(10, 20)
        interval.expand(1)
        self.assertEqual(interval.min, 9)
        self.assertEqual(interval.max, 21)

    def test_interval1d_shrink(self):
        interval = Interval1D(10, 20)
        interval.shrink(1)
        self.assertEqual(interval.min, 11)
        self.assertEqual(interval.max, 19)

    def test_interval1d_move(self):
        interval = Interval1D(10, 20)
        interval.move(1)
        self.assertEqual(interval.min, 11)
        self.assertEqual(interval.max, 21)


class Interval2DTest(unittest.TestCase):

    def test_interval2d_properties(self):
        interval = Interval2D(1, 3, 4, 5)
        self.assertEqual(interval.x1, 1)
        self.assertEqual(interval.x2, 3)
        self.assertEqual(interval.y1, 4)
        self.assertEqual(interval.y2, 5)
        self.assertEqual(interval.min_x, 1)
        self.assertEqual(interval.max_x, 3)
        self.assertEqual(interval.min_y, 4)
        self.assertEqual(interval.max_y, 5)
        self.assertEqual(interval.min_corner, (1, 4))
        self.assertEqual(interval.max_corner, (3, 5))
        self.assertEqual(interval.size_x, 2)
        self.assertEqual(interval.size_y, 1)
        self.assertEqual(interval.extent_x, Interval1D(1, 3))
        self.assertEqual(interval.extent_y, Interval1D(4, 5))
        self.assertEqual(interval.center_x, 2)
        self.assertEqual(interval.center_y, 4.5)
        self.assertEqual(interval.tuple_x, (1, 3))
        self.assertEqual(interval.tuple_y, (4, 5))
        self.assertEqual(interval.tuple_xy, ((1, 3), (4, 5)))

    def test_interval2d_from_tuple(self):
        interval = Interval2D.from_tuples((1, 3), (4, 5))
        self.assertEqual(interval.x1, 1)
        self.assertEqual(interval.x2, 3)
        self.assertEqual(interval.y1, 4)
        self.assertEqual(interval.y2, 5)

    def test_interval2d_set(self):
        interval = Interval2D(10, 20, 30, 40)
        interval.set(1, 3, 4, 5)
        self.assertEqual(interval.x1, 1)
        self.assertEqual(interval.x2, 3)
        self.assertEqual(interval.y1, 4)
        self.assertEqual(interval.y2, 5)

    def test_interval2d_copy(self):
        interval = Interval2D(10, 20, 30, 40)
        interval2 = interval.copy()
        interval2.set(1, 3, 4, 5)
        self.assertNotEqual(interval.x1, interval2.x1)
        self.assertNotEqual(interval.x2, interval2.x2)
        self.assertNotEqual(interval.y1, interval2.y1)
        self.assertNotEqual(interval.y2, interval2.y2)

    def test_interval2d_eq(self):
        self.assertTrue(Interval2D(10, 20, 30, 40) == Interval2D(10, 20, 30, 40))
        self.assertTrue(Interval2D(10, 20, 30, 40) != Interval2D(11, 20, 30, 40))
        self.assertTrue(Interval2D(10, 20, 30, 40) != Interval2D(10, 21, 30, 40))
        self.assertTrue(Interval2D(10, 20, 30, 40) != Interval2D(10, 20, 31, 40))

    def test_interval2d_expand(self):
        interval = Interval2D(10, 20, 30, 40)
        interval.expand(1)
        self.assertEqual(interval.x1, 9)
        self.assertEqual(interval.x2, 21)
        self.assertEqual(interval.y1, 29)
        self.assertEqual(interval.y2, 41)

    def test_interval2d_expand_x(self):
        interval = Interval2D(10, 20, 30, 40)
        interval.expand_x(1)
        self.assertEqual(interval.x1, 9)
        self.assertEqual(interval.x2, 21)
        self.assertEqual(interval.y1, 30)
        self.assertEqual(interval.y2, 40)

    def test_interval2d_expand_y(self):
        interval = Interval2D(10, 20, 30, 40)
        interval.expand_y(1)
        self.assertEqual(interval.x1, 10)
        self.assertEqual(interval.x2, 20)
        self.assertEqual(interval.y1, 29)
        self.assertEqual(interval.y2, 41)

    def test_interval2d_shrink(self):
        interval = Interval2D(10, 20, 30, 40)
        interval.shrink(1)
        self.assertEqual(interval.x1, 11)
        self.assertEqual(interval.x2, 19)
        self.assertEqual(interval.y1, 31)
        self.assertEqual(interval.y2, 39)

    def test_interval2d_shrink_x(self):
        interval = Interval2D(10, 20, 30, 40)
        interval.shrink_x(1)
        self.assertEqual(interval.x1, 11)
        self.assertEqual(interval.x2, 19)
        self.assertEqual(interval.y1, 30)
        self.assertEqual(interval.y2, 40)

    def test_interval2d_shrink_y(self):
        interval = Interval2D(10, 20, 30, 40)
        interval.shrink_y(1)
        self.assertEqual(interval.x1, 10)
        self.assertEqual(interval.x2, 20)
        self.assertEqual(interval.y1, 31)
        self.assertEqual(interval.y2, 39)

    def test_interval2d_move(self):
        interval = Interval2D(10, 20, 30, 40)
        interval.move((1, 2))
        self.assertEqual(interval.x1, 11)
        self.assertEqual(interval.x2, 21)
        self.assertEqual(interval.y1, 32)
        self.assertEqual(interval.y2, 42)


class Interval3DTest(unittest.TestCase):

    def test_interval3d_properties(self):
        interval = Interval3D(1, 3, 4, 5, 10, 20)
        self.assertEqual(interval.x1, 1)
        self.assertEqual(interval.x2, 3)
        self.assertEqual(interval.y1, 4)
        self.assertEqual(interval.y2, 5)
        self.assertEqual(interval.z1, 10)
        self.assertEqual(interval.z2, 20)
        self.assertEqual(interval.min_x, 1)
        self.assertEqual(interval.max_x, 3)
        self.assertEqual(interval.min_y, 4)
        self.assertEqual(interval.max_y, 5)
        self.assertEqual(interval.min_z, 10)
        self.assertEqual(interval.max_z, 20)
        self.assertEqual(interval.min_corner, (1, 4, 10))
        self.assertEqual(interval.max_corner, (3, 5, 20))
        self.assertEqual(interval.size_x, 2)
        self.assertEqual(interval.size_y, 1)
        self.assertEqual(interval.size_z, 10)
        self.assertEqual(interval.extent_x, Interval1D(1, 3))
        self.assertEqual(interval.extent_y, Interval1D(4, 5))
        self.assertEqual(interval.extent_z, Interval1D(10, 20))
        self.assertEqual(interval.center_x, 2)
        self.assertEqual(interval.center_y, 4.5)
        self.assertEqual(interval.center_z, 15)
        self.assertEqual(interval.tuple_x, (1, 3))
        self.assertEqual(interval.tuple_y, (4, 5))
        self.assertEqual(interval.tuple_z, (10, 20))
        self.assertEqual(interval.tuple_xyz, ((1, 3), (4, 5), (10, 20)))

    def test_interval3d_from_tuple(self):
        interval = Interval3D.from_tuples((1, 3), (4, 5), (10, 20))
        self.assertEqual(interval.x1, 1)
        self.assertEqual(interval.x2, 3)
        self.assertEqual(interval.y1, 4)
        self.assertEqual(interval.y2, 5)
        self.assertEqual(interval.z1, 10)
        self.assertEqual(interval.z2, 20)

    def test_interval3d_set(self):
        interval = Interval3D(10, 20, 30, 40, 50, 60)
        interval.set(1, 3, 4, 5, 10, 20)
        self.assertEqual(interval.x1, 1)
        self.assertEqual(interval.x2, 3)
        self.assertEqual(interval.y1, 4)
        self.assertEqual(interval.y2, 5)
        self.assertEqual(interval.z1, 10)
        self.assertEqual(interval.z2, 20)

    def test_interval3d_copy(self):
        interval = Interval3D(10, 20, 30, 40, 50, 60)
        interval2 = interval.copy()
        interval2.set(1, 3, 4, 5, 10, 20)
        self.assertNotEqual(interval.x1, interval2.x1)
        self.assertNotEqual(interval.x2, interval2.x2)
        self.assertNotEqual(interval.y1, interval2.y1)
        self.assertNotEqual(interval.y2, interval2.y2)
        self.assertNotEqual(interval.z1, interval2.z1)
        self.assertNotEqual(interval.z2, interval2.z2)

    def test_interval3d_eq(self):
        self.assertTrue(Interval3D(10, 20, 30, 40, 50, 60) == Interval3D(10, 20, 30, 40, 50, 60))
        self.assertTrue(Interval3D(10, 20, 30, 40, 50, 60) != Interval3D(11, 20, 30, 40, 50, 60))
        self.assertTrue(Interval3D(10, 20, 30, 40, 50, 60) != Interval3D(10, 21, 30, 40, 50, 60))
        self.assertTrue(Interval3D(10, 20, 30, 40, 50, 60) != Interval3D(10, 20, 31, 40, 50, 60))
        self.assertTrue(Interval3D(10, 20, 30, 40, 50, 60) != Interval3D(10, 20, 30, 41, 50, 60))
        self.assertTrue(Interval3D(10, 20, 30, 40, 50, 60) != Interval3D(10, 20, 30, 40, 51, 60))
        self.assertTrue(Interval3D(10, 20, 30, 40, 50, 60) != Interval3D(10, 20, 30, 40, 50, 61))

    def test_interval3d_expand(self):
        interval = Interval3D(10, 20, 30, 40, 50, 60)
        interval.expand(1)
        self.assertEqual(interval, Interval3D(9, 21, 29, 41, 49, 61))

    def test_interval3d_expand_x(self):
        interval = Interval3D(10, 20, 30, 40, 50, 60)
        interval.expand_x(1)
        self.assertEqual(interval, Interval3D(9, 21, 30, 40, 50, 60))

    def test_interval3d_expand_y(self):
        interval = Interval3D(10, 20, 30, 40, 50, 60)
        interval.expand_y(1)
        self.assertEqual(interval, Interval3D(10, 20, 29, 41, 50, 60))

    def test_interval3d_expand_z(self):
        interval = Interval3D(10, 20, 30, 40, 50, 60)
        interval.expand_z(1)
        self.assertEqual(interval, Interval3D(10, 20, 30, 40, 49, 61))

    def test_interval3d_shrink(self):
        interval = Interval3D(10, 20, 30, 40, 50, 60)
        interval.shrink(1)
        self.assertEqual(interval, Interval3D(11, 19, 31, 39, 51, 59))

    def test_interval3d_shrink_x(self):
        interval = Interval3D(10, 20, 30, 40, 50, 60)
        interval.shrink_x(1)
        self.assertEqual(interval, Interval3D(11, 19, 30, 40, 50, 60))

    def test_interval3d_shrink_y(self):
        interval = Interval3D(10, 20, 30, 40, 50, 60)
        interval.shrink_y(1)
        self.assertEqual(interval, Interval3D(10, 20, 31, 39, 50, 60))

    def test_interval3d_shrink_z(self):
        interval = Interval3D(10, 20, 30, 40, 50, 60)
        interval.shrink_z(1)
        self.assertEqual(interval, Interval3D(10, 20, 30, 40, 51, 59))

    def test_interval3d_move(self):
        interval = Interval3D(10, 20, 30, 40, 50, 60)
        interval.move((1, 2, 3))
        self.assertEqual(interval, Interval3D(11, 21, 32, 42, 53, 63))



if __name__ == '__main__':
    unittest.main()
