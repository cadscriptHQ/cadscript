# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

import unittest
import cadscript
from cadscript.interval import Interval3D


class BodyMoveTest(unittest.TestCase):

    def test_box_move_to_origin_x(self):
        box = cadscript.make_box(2, 2, 2, center=True)
        box.move_to_origin("X")
        self.assertEqual(box.get_extent(), Interval3D(0, 2, -1, 1, -1, 1))

    def test_box_move_to_origin_y(self):
        box = cadscript.make_box(2, 2, 2, center=True)
        box.move_to_origin("Y")
        self.assertEqual(box.get_extent(), Interval3D(-1, 1, 0, 2, -1, 1))

    def test_box_move_to_origin_z(self):
        box = cadscript.make_box(2, 2, 2, center=True)
        box.move_to_origin("Z")
        self.assertEqual(box.get_extent(), Interval3D(-1, 1, -1, 1, 0, 2))

    def test_box_move_to_origin_xy(self):
        box = cadscript.make_box(2, 2, 2, center=True)
        box.move_to_origin("XY")
        self.assertEqual(box.get_extent(), Interval3D(0, 2, 0, 2, -1, 1))

    def test_box_move_to_origin_xz(self):
        box = cadscript.make_box(2, 2, 2, center=True)
        box.move_to_origin("XZ")
        self.assertEqual(box.get_extent(), Interval3D(0, 2, -1, 1, 0, 2))

    def test_box_move_to_origin_yz(self):
        box = cadscript.make_box(2, 2, 2, center=True)
        box.move_to_origin("YZ")
        self.assertEqual(box.get_extent(), Interval3D(-1, 1, 0, 2, 0, 2))

    def test_box_move_to_origin_xyz(self):
        box = cadscript.make_box(2, 2, 2, center=True)
        box.move_to_origin("XYZ")
        self.assertEqual(box.get_extent(), Interval3D(0, 2, 0, 2, 0, 2))

    def test_box_move_to_origin_true(self):
        box = cadscript.make_box(2, 2, 2, center=True)
        box.move_to_origin(True)
        self.assertEqual(box.get_extent(), Interval3D(0, 2, 0, 2, 0, 2))

    def test_box_move_to_origin(self):
        box = cadscript.make_box(2, 2, 2, center=True)
        box.move_to_origin()
        self.assertEqual(box.get_extent(), Interval3D(0, 2, 0, 2, 0, 2))

    def test_box_move_to_origin_false(self):
        box = cadscript.make_box(2, 2, 2, center=True)
        box.move_to_origin(False)
        self.assertEqual(box.get_extent(), Interval3D(-1, 1, -1, 1, -1, 1))

    def test_return_type_move_to_origin(self):
        box = cadscript.make_box(1, 1, 1, center=True)
        test_obj = box.move_to_origin()
        self.assertIsInstance(test_obj, cadscript.Body)


    def test_box_move(self):
        box = cadscript.make_box(2, 2, 2, center=False)
        box.move((1, 2, 3))
        self.assertEqual(box.get_extent(), Interval3D(1, 3, 2, 4, 3, 5))

    def test_return_type_move(self):
        box = cadscript.make_box(1, 1, 1, center=True)
        test_obj = box.move((1, 1, 1))
        self.assertIsInstance(test_obj, cadscript.Body)


    def test_box_center_x(self):
        box = cadscript.make_box(2, 4, 6, center=False)
        box.center("X")
        self.assertEqual(box.get_extent(), Interval3D(-1, 1, 0, 4, 0, 6))

    def test_box_center_y(self):
        box = cadscript.make_box(2, 4, 6, center=False)
        box.center("Y")
        self.assertEqual(box.get_extent(), Interval3D(0, 2, -2, 2, 0, 6))

    def test_box_center_z(self):
        box = cadscript.make_box(2, 4, 6, center=False)
        box.center("Z")
        self.assertEqual(box.get_extent(), Interval3D(0, 2, 0, 4, -3, 3))

    def test_box_center_xy(self):
        box = cadscript.make_box(2, 4, 6, center=False)
        box.center("XY")
        self.assertEqual(box.get_extent(), Interval3D(-1, 1, -2, 2, 0, 6))

    def test_box_center_xz(self):
        box = cadscript.make_box(2, 4, 6, center=False)
        box.center("XZ")
        self.assertEqual(box.get_extent(), Interval3D(-1, 1, 0, 4, -3, 3))

    def test_box_center_yz(self):
        box = cadscript.make_box(2, 4, 6, center=False)
        box.center("YZ")
        self.assertEqual(box.get_extent(), Interval3D(0, 2, -2, 2, -3, 3))

    def test_box_center_xyz(self):
        box = cadscript.make_box(2, 4, 6, center=False)
        box.center("XYZ")
        self.assertEqual(box.get_extent(), Interval3D(-1, 1, -2, 2, -3, 3))

    def test_box_center_true(self):
        box = cadscript.make_box((2, 4), (2, 6), (-10, -4), center=False)
        box.center(True)
        self.assertEqual(box.get_extent(), Interval3D(-1, 1, -2, 2, -3, 3))

    def test_box_center(self):
        box = cadscript.make_box(2, 4, 6, center=False)
        box.center()
        self.assertEqual(box.get_extent(), Interval3D(-1, 1, -2, 2, -3, 3))

    def test_box_center_false(self):
        box = cadscript.make_box(2, 4, 6, center=False)
        box.center(False)
        self.assertEqual(box.get_extent(), Interval3D(0, 2, 0, 4, 0, 6))

    def test_return_type_center(self):
        box = cadscript.make_box(1, 1, 1, center=True)
        test_obj = box.center()
        self.assertIsInstance(test_obj, cadscript.Body)


if __name__ == '__main__':
    unittest.main()
