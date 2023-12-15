import unittest
from cadscript.helpers import get_dimensions

class DimensionsTest(unittest.TestCase):

    def assert_equal_tuple_iter(self, iter1, iter2):
        for (a,b) in zip(iter1, iter2):
            self.assertEqual(a, b)

    def test_2d_with_size(self):
        dimensions = [2.0, 3.0]
        center = False
        expected_result = [(0.0, 2.0), (0.0, 3.0)]
        result = get_dimensions(dimensions, center)
        self.assert_equal_tuple_iter(result, expected_result)

    def test_2d_min_max(self):
        dimensions = [(1.0, 2.0), (3.5, 4.0)]
        center = False
        expected_result = [(1.0, 2.0), (3.5, 4.0)]
        result = get_dimensions(dimensions, center)
        self.assert_equal_tuple_iter(result, expected_result)

    def test_2d_min_max_centered(self):
        dimensions = [(1.0, 2.0), (3.5, 4.0)]
        center = True
        expected_result = [(1.0, 2.0), (3.5, 4.0)]
        result = get_dimensions(dimensions, center)
        self.assert_equal_tuple_iter(result, expected_result)

    def test_2d_mixed(self):
        dimensions = [2.0, (3.5, 4.0)]
        center = False
        expected_result = [(0.0, 2.0), (3.5, 4.0)]
        result = get_dimensions(dimensions, center)
        self.assert_equal_tuple_iter(result, expected_result)

    def test_2d_mixed_centered(self):
        dimensions = [2.0, (-3.5, 4.0)]
        center = True
        expected_result = [(-1.0, 1.0), (-3.5, 4.0)]
        result = get_dimensions(dimensions, center)
        self.assert_equal_tuple_iter(result, expected_result)

    def test_2d_single_value(self):
        dimensions = [5.0, 10.0]
        center = True
        expected_result = [(-2.5, 2.5), (-5.0, 5.0)]
        result = get_dimensions(dimensions, center)
        self.assert_equal_tuple_iter(result, expected_result)

    def test_2d_flipped_size(self):
        dimensions = [(2,-2), (-3, -4)]
        center = True
        expected_result = [(-2,2), (-4, -3)]
        result = get_dimensions(dimensions, center)
        self.assert_equal_tuple_iter(result, expected_result)

    def test_2d_tuple(self):
        dimensions = ((2,-2), (-3, -4))
        center = True
        expected_result = [(-2,2), (-4, -3)]
        result = get_dimensions(dimensions, center)
        self.assert_equal_tuple_iter(result, expected_result)

    def test_3d_with_size(self):
        dimensions = [2.0, 3.0, 4.0]
        center = False
        expected_result = [(0.0, 2.0), (0.0, 3.0), (0.0, 4.0)]
        result = get_dimensions(dimensions, center)
        self.assert_equal_tuple_iter(result, expected_result)

    def test_3d_min_max(self):
        dimensions = [(1.0, 2.0), (3.5, 4.0), (10, 20)]
        center = False
        expected_result = [(1.0, 2.0), (3.5, 4.0), (10, 20)]
        result = get_dimensions(dimensions, center)
        self.assert_equal_tuple_iter(result, expected_result)

    def test_3d_centered(self):
        dimensions = [2, 4, 6]
        center = True
        expected_result = [(-1,1), (-2,2), (-3,3)]
        result = get_dimensions(dimensions, center)
        self.assert_equal_tuple_iter(result, expected_result)        
