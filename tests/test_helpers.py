# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

import unittest
import cadscript.helpers as helpers


class DimensionsTest(unittest.TestCase):

    def assert_equal_tuple_iter(self, iter1, iter2):
        self.assertEqual(len(list(iter1)), len(list(iter2)))
        for (a,b) in zip(iter1, iter2):
            self.assertEqual(a, b)

    def test_2d_with_size(self):
        dimensions = [2.0, 3.0]
        center = False
        expected_result = [(0.0, 2.0), (0.0, 3.0)]
        result = helpers.get_dimensions(dimensions, center)
        self.assert_equal_tuple_iter(result, expected_result)

    def test_2d_min_max(self):
        dimensions = [(1.0, 2.0), (3.5, 4.0)]
        center = False
        expected_result = [(1.0, 2.0), (3.5, 4.0)]
        result = helpers.get_dimensions(dimensions, center)
        self.assert_equal_tuple_iter(result, expected_result)

    def test_2d_min_max_centered(self):
        dimensions = [(1.0, 2.0), (3.5, 4.0)]
        center = True
        expected_result = [(1.0, 2.0), (3.5, 4.0)]
        result = helpers.get_dimensions(dimensions, center)
        self.assert_equal_tuple_iter(result, expected_result)

    def test_2d_mixed(self):
        dimensions = [2.0, (3.5, 4.0)]
        center = False
        expected_result = [(0.0, 2.0), (3.5, 4.0)]
        result = helpers.get_dimensions(dimensions, center)
        self.assert_equal_tuple_iter(result, expected_result)

    def test_2d_mixed_centered(self):
        dimensions = [2.0, (-3.5, 4.0)]
        center = True
        expected_result = [(-1.0, 1.0), (-3.5, 4.0)]
        result = helpers.get_dimensions(dimensions, center)
        self.assert_equal_tuple_iter(result, expected_result)

    def test_2d_single_value(self):
        dimensions = [5.0, 10.0]
        center = True
        expected_result = [(-2.5, 2.5), (-5.0, 5.0)]
        result = helpers.get_dimensions(dimensions, center)
        self.assert_equal_tuple_iter(result, expected_result)

    def test_2d_flipped_size(self):
        dimensions = [(2,-2), (-3, -4)]
        center = True
        expected_result = [(-2,2), (-4, -3)]
        result = helpers.get_dimensions(dimensions, center)
        self.assert_equal_tuple_iter(result, expected_result)

    def test_2d_tuple(self):
        dimensions = ((2,-2), (-3, -4))
        center = True
        expected_result = [(-2,2), (-4, -3)]
        result = helpers.get_dimensions(dimensions, center)
        self.assert_equal_tuple_iter(result, expected_result)

    def test_3d_with_size(self):
        dimensions = [2.0, 3.0, 4.0]
        center = False
        expected_result = [(0.0, 2.0), (0.0, 3.0), (0.0, 4.0)]
        result = helpers.get_dimensions(dimensions, center)
        self.assert_equal_tuple_iter(result, expected_result)

    def test_3d_min_max(self):
        dimensions = [(1.0, 2.0), (3.5, 4.0), (10, 20)]
        center = False
        expected_result = [(1.0, 2.0), (3.5, 4.0), (10, 20)]
        result = helpers.get_dimensions(dimensions, center)
        self.assert_equal_tuple_iter(result, expected_result)

    def test_3d_centered(self):
        dimensions = [2, 4, 6]
        center = True
        expected_result = [(-1,1), (-2,2), (-3,3)]
        result = helpers.get_dimensions(dimensions, center)
        self.assert_equal_tuple_iter(result, expected_result)        

class CenterTest(unittest.TestCase):

    def test_string_XYZ(self):
        center = "XYZ"
        expected_result = (True, True, True)
        result = helpers.get_center_flags(center)
        self.assertEqual(result, expected_result)

    def test_string_X(self):
        center = "X"
        expected_result = (True, False, False)
        result = helpers.get_center_flags(center)
        self.assertEqual(result, expected_result)

    def test_string_Y(self):
        center = "Y"
        expected_result = (False, True, False)
        result = helpers.get_center_flags(center)
        self.assertEqual(result, expected_result)

    def test_string_Z(self):
        center = "Z"
        expected_result = (False, False, True)
        result = helpers.get_center_flags(center)
        self.assertEqual(result, expected_result)

    def test_string_XY(self):
        center = "XY"
        expected_result = (True, True, False)
        result = helpers.get_center_flags(center)
        self.assertEqual(result, expected_result)

    def test_string_XZ(self):
        center = "XZ"
        expected_result = (True, False, True)
        result = helpers.get_center_flags(center)
        self.assertEqual(result, expected_result)

    def test_string_YZ(self):
        center = "YZ"
        expected_result = (False, True, True)
        result = helpers.get_center_flags(center)
        self.assertEqual(result, expected_result)

    def test_boolean(self):
        center = True
        expected_result = (True, True, True)
        result = helpers.get_center_flags(center)
        self.assertEqual(result, expected_result)

    def test_boolean_false(self):
        center = False
        expected_result = (False, False, False)
        result = helpers.get_center_flags(center)
        self.assertEqual(result, expected_result)

    def test_wrong_type(self):
        center = 123
        expected_result = (False, False, False)
        result = helpers.get_center_flags(center) # type: ignore
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()        