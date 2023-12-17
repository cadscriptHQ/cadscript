import unittest
from cadscript import pattern_grid

class PatternGrid2DTest(unittest.TestCase):
    def assertPatternEqual(self, result, expected):
        self.assertEqual(set(result), set(expected))

    def test_3x3_size_centered(self):
        nx = 3
        ny = 3
        expected_result = [
            (-1.0, -1.0), (0.0, -1.0), (1.0, -1.0),
            (-1.0, 0.0), (0.0, 0.0), (1.0, 0.0),
            (-1.0, 1.0), (0.0, 1.0), (1.0, 1.0)
        ]
        result = pattern_grid(nx, ny, size_x=2.0, size_y=2.0)
        self.assertPatternEqual(result, expected_result)

    def test_4x4_size_centered(self):
        nx = 4
        ny = 4
        expected_result = [
            (-0.75, -0.75), (-0.25, -0.75), (0.25, -0.75), (0.75, -0.75),
            (-0.75, -0.25), (-0.25, -0.25), (0.25, -0.25), (0.75, -0.25),
            (-0.75, 0.25), (-0.25, 0.25), (0.25, 0.25), (0.75, 0.25),
            (-0.75, 0.75), (-0.25, 0.75), (0.25, 0.75), (0.75, 0.75)
        ]
        result = pattern_grid(nx, ny, size_x=1.5, size_y=1.5)
        self.assertPatternEqual(result, expected_result)

    def test_1x1_size_centered(self):
        nx = 1
        ny = 1
        expected_result = [(0.0, 0.0)]
        result = pattern_grid(nx, ny, size_x=1.0, size_y=1.0)
        self.assertPatternEqual(result, expected_result)

    def test_1x1_size_centered_zero_dimension(self):
        nx = 3
        ny = 3
        expected_result = [
            (0.0, 0.0), (0.0, 0.0), (0.0, 0.0),
            (0.0, 0.0), (0.0, 0.0), (0.0, 0.0),
            (0.0, 0.0), (0.0, 0.0), (0.0, 0.0)
        ]
        result = pattern_grid(nx, ny, size_x=0.0, size_y=0.0)
        self.assertPatternEqual(result, expected_result)

    def test_3x3_spacing_centered(self):
        nx = 3
        ny = 3
        expected_result = [
            (-1.0, -1.0), (0.0, -1.0), (1.0, -1.0),
            (-1.0, 0.0), (0.0, 0.0), (1.0, 0.0),
            (-1.0, 1.0), (0.0, 1.0), (1.0, 1.0)
        ]
        result = pattern_grid(nx, ny, spacing_x=1.0, spacing_y=1.0)
        self.assertPatternEqual(result, expected_result)

    def test_4x4_spacing_centered(self):
        nx = 4
        ny = 4
        expected_result = [
            (-0.75, -0.75), (-0.25, -0.75), (0.25, -0.75), (0.75, -0.75),
            (-0.75, -0.25), (-0.25, -0.25), (0.25, -0.25), (0.75, -0.25),
            (-0.75, 0.25), (-0.25, 0.25), (0.25, 0.25), (0.75, 0.25),
            (-0.75, 0.75), (-0.25, 0.75), (0.25, 0.75), (0.75, 0.75)
        ]
        result = pattern_grid(nx, ny, spacing_x=0.5, spacing_y=0.5)
        self.assertPatternEqual(result, expected_result)

    def test_1x1_spacing_centered(self):
        nx = 1
        ny = 1
        expected_result = [(0.0, 0.0)]
        result = pattern_grid(nx, ny, spacing_x=1.0, spacing_y=1.0)
        self.assertPatternEqual(result, expected_result)

    def test_3x3_spacing_centered_zero_spacing(self):
        nx = 3
        ny = 3
        expected_result = [
            (0.0, 0.0), (0.0, 0.0), (0.0, 0.0),
            (0.0, 0.0), (0.0, 0.0), (0.0, 0.0),
            (0.0, 0.0), (0.0, 0.0), (0.0, 0.0)
        ]
        result = pattern_grid(nx, ny, spacing_x=0.0, spacing_y=0.0)
        self.assertPatternEqual(result, expected_result)

    # test for exception when both size and spacing are specified
    def test_exception_both_size_spacing(self):
        with self.assertRaises(ValueError):
            result = pattern_grid(3, 3, size_x=1.0, size_y=1.0, spacing_x=1.0, spacing_y=1.0)

    # test for exception when neither size nor spacing are specified
    def test_exception_neither_size_spacing(self):
        with self.assertRaises(ValueError):
            result = pattern_grid(3, 3)

    # test for exception when size is specified for x axis but not y
    def test_exception_size_one_axis_x(self):
        with self.assertRaises(ValueError):
            result = pattern_grid(3, 3, size_x=1.0)

    # test for exception when size is specified for y axis but not x
    def test_exception_size_one_axis_y(self):
        with self.assertRaises(ValueError):
            result = pattern_grid(3, 3, size_y=1.0)

    # test for exception when spacing is specified for x axis but not y
    def test_exception_spacing_one_axis_x(self):
        with self.assertRaises(ValueError):
            result = pattern_grid(3, 3, spacing_x=1.0)

    # test for exception when spacing is specified for y axis but not x
    def test_exception_spacing_one_axis_y(self):
        with self.assertRaises(ValueError):
            result = pattern_grid(3, 3, spacing_y=1.0)

    # test for exception when count_x is less than 1
    def test_exception_count_x_less_than_one(self):
        with self.assertRaises(ValueError):
            result = pattern_grid(0, 3, size_x=1.0, size_y=1.0)

    # test for exception when count_y is less than 1
    def test_exception_count_y_less_than_one(self):
        with self.assertRaises(ValueError):
            result = pattern_grid(3, -1, size_x=1.0, size_y=1.0)

if __name__ == '__main__':
    unittest.main()