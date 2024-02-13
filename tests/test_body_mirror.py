# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

import unittest
import cadscript


class BodyMirrorTest(unittest.TestCase):

    def test_box_mirror_x(self):
        box = cadscript.make_box(2, 2, 2, center=False)
        box.mirror("X")
        self.assertEqual(box.get_extent(), ((-2, 2), (0, 2), (0, 2)))

    def test_box_mirror_y(self):
        box = cadscript.make_box(2, 2, 2, center=False)
        box.mirror("Y")
        self.assertEqual(box.get_extent(), ((0, 2), (-2, 2), (0, 2)))

    def test_box_mirror_z(self):
        box = cadscript.make_box(2, 2, 2, center=False)
        box.mirror("Z")
        self.assertEqual(box.get_extent(), ((0, 2), (0, 2), (-2, 2)))

    def test_box_mirror_x_no_copy(self):
        box = cadscript.make_box(2, 2, 2, center=False)
        box.mirror("X", copy_and_merge=False)
        self.assertEqual(box.get_extent(), ((-2, 0), (0, 2), (0, 2)))

    def test_box_mirror_y_no_copy(self):
        box = cadscript.make_box(2, 2, 2, center=False)
        box.mirror("Y", copy_and_merge=False)
        self.assertEqual(box.get_extent(), ((0, 2), (-2, 0), (0, 2)))

    def test_box_mirror_z_no_copy(self):
        box = cadscript.make_box(2, 2, 2, center=False)
        box.mirror("Z", copy_and_merge=False)
        self.assertEqual(box.get_extent(), ((0, 2), (0, 2), (-2, 0)))

    def test_invalid_axis(self):
        box = cadscript.make_box(2, 2, 2, center=False)
        with self.assertRaises(ValueError):
            box.mirror("A")  # invalid axis

if __name__ == '__main__':
    unittest.main()
