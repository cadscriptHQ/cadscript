# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

from typing import Tuple
import unittest

from cadscript.patterns import pattern_grid, pattern_rect, pattern_distribute, pattern_distribute_stretch


class PatternTuple:
    """
    result and expected are lists of tuples floats, so we need to compare the sets of tuples
    each tuple is compared with an epsilon
    """
    _epsilon = 1e-5

    def __init__(self, data: Tuple[float, float]):
        self.data = data

    def __eq__(self, other):
        return abs(self.data[0] - other.data[0]) < self._epsilon and abs(self.data[1] - other.data[1]) < self._epsilon


class PatternSet:
    def __init__(self, data: list[Tuple[float, float]]):
        self.data = [PatternTuple(data) for data in data]

    def __eq__(self, other):
        if len(self.data) != len(other.data):
            return False
        if len(self.data) == 0 and len(other.data) == 0:
            return True
        for item in self.data:
            for other_item in other.data:
                if item == other_item:
                    return True
        return False


class PatternSet2:
    def __init__(self, data: list[Tuple[Tuple[float, float], Tuple[float, float]]]):
        self.data = [(PatternTuple(data1), PatternTuple(data2)) for data1, data2 in data]

    def __eq__(self, other):
        if len(self.data) != len(other.data):
            return False
        if len(self.data) == 0 and len(other.data) == 0:
            return True
        for item in self.data:
            for other_item in other.data:
                if item[0] == other_item[0] and item[1] == other_item[1]:
                    return True
        return False


class PatternTestBase(unittest.TestCase):

    def assertPatternEqual(self, result, expected):
        result_set = PatternSet(result)
        expected_set = PatternSet(expected)
        self.assertEqual(result_set, expected_set, f"Expected {expected},\ngot {result}")

    def assertPattern2Equal(self, result, expected):
        result_set = PatternSet2(result)
        expected_set = PatternSet2(expected)
        self.assertEqual(result_set, expected_set, f"Expected {expected},\ngot {result}")


class PatternRectTest(PatternTestBase):
    def test_2x1_uncentered(self):
        nx = 2
        ny = 1
        expected_result = [
            (0, 0), (0, 1), (2, 1), (2, 0)
        ]
        result = pattern_rect(nx, ny, center=False)
        self.assertPatternEqual(result, expected_result)

    def test_2x4_centered(self):
        nx = 2
        ny = 4
        expected_result = [
            (-1, -2), (-1, 2), (1, 2), (1, -2)
        ]
        result = pattern_rect(nx, ny, center=True)
        self.assertPatternEqual(result, expected_result)

    def test_2x999_centered_x(self):
        nx = 2
        ny = 999
        expected_result = [
            (-1, 0), (-1, 999), (1, 999), (1, 0)
        ]
        result = pattern_rect(nx, ny, center="X")
        self.assertPatternEqual(result, expected_result)

    def test_2x4_centered_y(self):
        nx = 2
        ny = 4
        expected_result = [
            (0, -2), (0, 2), (2, 2), (2, -2)
        ]
        result = pattern_rect(nx, ny, center="Y")
        self.assertPatternEqual(result, expected_result)


class PatternGridTest(PatternTestBase):
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

    def test_3x1_size_centered(self):
        nx = 3
        ny = 1
        expected_result = [(-1.0, 0.0), (0.0, 0.0), (1.0, 0.0)]
        result = pattern_grid(nx, ny, size_x=2.0)
        self.assertPatternEqual(result, expected_result)

    def test_1x5_size_centered(self):
        nx = 1
        ny = 5
        expected_result = [(0.0, -1.0), (0.0, -0.5), (0.0, 0.0), (0.0, 0.5), (0.0, 1.0)]
        result = pattern_grid(nx, ny, size_y=2.0)
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

    def test_3x1_spacing_centered(self):
        nx = 3
        ny = 1
        expected_result = [(-1.0, 0.0), (0.0, 0.0), (1.0, 0.0)]
        result = pattern_grid(nx, ny, spacing_x=1.0)
        self.assertPatternEqual(result, expected_result)

    def test_1x6_spacing_centered(self):
        nx = 1
        ny = 6
        expected_result = [(0.0, -2.5), (0.0, -1.5), (0.0, -0.5), (0.0, 0.5), (0.0, 1.5), (0.0, 2.5)]
        result = pattern_grid(nx, ny, spacing_y=1.0)
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

    def test_1x1_size_uncentered(self):
        nx = 1
        ny = 1
        expected_result = [(0.0, 0.0)]
        result = pattern_grid(nx, ny, size_x=1.0, size_y=1.0, center=False)
        self.assertPatternEqual(result, expected_result)

    def test_2x2_size_uncentered_zero_dimension(self):
        nx = 2
        ny = 2
        expected_result = [(0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0)]
        result = pattern_grid(nx, ny, size_x=0.0, size_y=0.0, center=False)
        self.assertPatternEqual(result, expected_result)

    def test_1x1_spacing_uncentered(self):
        nx = 1
        ny = 1
        expected_result = [(0.0, 0.0)]
        result = pattern_grid(nx, ny, spacing_x=1.0, spacing_y=1.0, center=False)
        self.assertPatternEqual(result, expected_result)

    def test_1x5_size_uncentered(self):
        nx = 1
        ny = 5
        expected_result = [(0.0, 0.0), (0.0, 0.5), (0.0, 1.0), (0.0, 1.5), (0.0, 2.0)]
        result = pattern_grid(nx, ny, size_y=2.0, center=False)
        self.assertPatternEqual(result, expected_result)

    def test_1x6_spacing_uncentered(self):
        nx = 1
        ny = 6
        expected_result = [(0.0, 0.0), (0.0, 1.0), (0.0, 2.0), (0.0, 3.0), (0.0, 4.0), (0.0, 5.0)]
        result = pattern_grid(nx, ny, spacing_y=1.0, center=False)
        self.assertPatternEqual(result, expected_result)

    def test_3x1_size_uncentered(self):
        nx = 3
        ny = 1
        expected_result = [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0)]
        result = pattern_grid(nx, ny, size_x=2.0, center=False)
        self.assertPatternEqual(result, expected_result)

    def test_3x1_spacing_uncentered(self):
        nx = 3
        ny = 1
        expected_result = [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0)]
        result = pattern_grid(nx, ny, spacing_x=1.0, center=False)
        self.assertPatternEqual(result, expected_result)

    def test_3x3_size_uncentered(self):
        nx = 3
        ny = 3
        expected_result = [
            (0.0, 0.0), (1.0, 0.0), (2.0, 0.0),
            (0.0, 1.0), (1.0, 1.0), (2.0, 1.0),
            (0.0, 2.0), (1.0, 2.0), (2.0, 2.0)
        ]
        result = pattern_grid(nx, ny, size_x=2.0, size_y=2.0, center=False)
        self.assertPatternEqual(result, expected_result)

    def test_3x3_spacing_uncentered(self):
        nx = 3
        ny = 3
        expected_result = [
            (0.0, 0.0), (1.0, 0.0), (2.0, 0.0),
            (0.0, 1.0), (1.0, 1.0), (2.0, 1.0),
            (0.0, 2.0), (1.0, 2.0), (2.0, 2.0)
        ]
        result = pattern_grid(nx, ny, spacing_x=1.0, spacing_y=1.0, center=False)
        self.assertPatternEqual(result, expected_result)

    def test_3x3_spacing_uncentered_zero_spacing(self):
        nx = 3
        ny = 3
        expected_result = [
            (0, 0), (0, 0), (0, 0),
            (0, 0), (0, 0), (0, 0),
            (0, 0), (0, 0), (0, 0)
        ]
        result = pattern_grid(nx, ny, spacing_x=0.0, spacing_y=0.0, center=False)
        self.assertPatternEqual(result, expected_result)

    def test_4x4_size_uncentered(self):
        nx = 4
        ny = 4
        expected_result = [
            (0.0, 0.0), (0.5, 0.0), (1.0, 0.0), (1.5, 0.0),
            (0.0, 0.5), (0.5, 0.5), (1.0, 0.5), (1.5, 0.5),
            (0.0, 1.0), (0.5, 1.0), (1.0, 1.0), (1.5, 1.0),
            (0.0, 1.5), (0.5, 1.5), (1.0, 1.5), (1.5, 1.5)
        ]
        result = pattern_grid(nx, ny, size_x=1.5, size_y=1.5, center=False)
        self.assertPatternEqual(result, expected_result)

    def test_3x2_spacing_uncentered(self):
        nx = 3
        ny = 2
        expected_result = [
            (0.0, 0.0), (0.5, 0.0), (1.0, 0.0),
            (0.0, 1.0), (0.5, 1.0), (1.0, 1.0)
        ]
        result = pattern_grid(nx, ny, spacing_x=0.5, spacing_y=1.0, center=False)
        self.assertPatternEqual(result, expected_result)

    def test_3x2_spacing_center_x(self):
        nx = 3
        ny = 2
        expected_result = [
            (-0.5, 0.0), (0.0, 0.0), (0.5, 0.0),
            (-0.5, 1.0), (0.0, 1.0), (0.5, 1.0)
        ]
        result = pattern_grid(nx, ny, spacing_x=0.5, spacing_y=1.0, center="X")
        self.assertPatternEqual(result, expected_result)

    def test_3x2_spacing_center_y(self):
        nx = 3
        ny = 2
        expected_result = [
            (0.0, -0.5), (0.5, -0.5), (1.0, -0.5),
            (0.0, 0.5), (0.5, 0.5), (1.0, 0.5)
        ]
        result = pattern_grid(nx, ny, spacing_x=0.5, spacing_y=1.0, center="Y")
        self.assertPatternEqual(result, expected_result)

    def test_3x2_size_center_x(self):
        nx = 3
        ny = 2
        expected_result = [
            (-0.5, 0.0), (0.0, 0.0), (0.5, 0.0),
            (-0.5, 1.0), (0.0, 1.0), (0.5, 1.0)
        ]
        result = pattern_grid(nx, ny, size_x=1.0, size_y=1.0, center="X")
        self.assertPatternEqual(result, expected_result)

    def test_3x1_size_center_x(self):
        nx = 3
        ny = 1
        expected_result = [
            (-0.5, 0.0), (0.0, 0.0), (0.5, 0.0)
        ]
        result = pattern_grid(nx, ny, size_x=1.0, center="X")
        self.assertPatternEqual(result, expected_result)

    def test_3x2_size_center_y(self):
        nx = 3
        ny = 2
        expected_result = [
            (0.0, -0.5), (0.5, -0.5), (1.0, -0.5),
            (0.0, 0.5), (0.5, 0.5), (1.0, 0.5)
        ]
        result = pattern_grid(nx, ny, size_x=1.0, size_y=1.0, center="Y")
        self.assertPatternEqual(result, expected_result)

    def test_3x2_mixed_size_and_spacing(self):
        nx = 3
        ny = 2
        expected_result = [
            (-0.5, -0.5), (0.0, -0.5), (0.5, -0.5),
            (-0.5, 0.5), (0.0, 0.5), (0.5, 0.5)
        ]
        result = pattern_grid(nx, ny, size_x=1.0, spacing_y=1.0, center=True)
        self.assertPatternEqual(result, expected_result)

    def test_3x2_mixed_size_and_spacing2(self):
        nx = 3
        ny = 2
        expected_result = [
            (-0.5, -0.5), (0.0, -0.5), (0.5, -0.5),
            (-0.5, 0.5), (0.0, 0.5), (0.5, 0.5)
        ]
        result = pattern_grid(nx, ny, spacing_x=0.5, size_y=1.0, center=True)
        self.assertPatternEqual(result, expected_result)

    # test for exception when both size and spacing are specified
    def test_exception_both_size_spacing(self):
        with self.assertRaises(ValueError):
            pattern_grid(3, 3, size_x=1.0, size_y=1.0, spacing_x=1.0, spacing_y=1.0)

    # test for exception when neither size nor spacing are specified
    def test_exception_neither_size_spacing(self):
        with self.assertRaises(ValueError):
            pattern_grid(3, 3)

    # test for exception when size is specified for x axis but not y
    def test_exception_size_one_axis_x(self):
        with self.assertRaises(ValueError):
            pattern_grid(3, 3, size_x=1.0)

    # test for exception when size is specified for y axis but not x
    def test_exception_size_one_axis_y(self):
        with self.assertRaises(ValueError):
            pattern_grid(3, 3, size_y=1.0)

    # test for exception when spacing is specified for x axis but not y
    def test_exception_spacing_one_axis_x(self):
        with self.assertRaises(ValueError):
            pattern_grid(3, 3, spacing_x=1.0)

    # test for exception when spacing is specified for y axis but not x
    def test_exception_spacing_one_axis_y(self):
        with self.assertRaises(ValueError):
            pattern_grid(3, 3, spacing_y=1.0)

    # test for exception when count_x is less than 1
    def test_exception_count_x_less_than_one(self):
        with self.assertRaises(ValueError):
            pattern_grid(0, 3, size_x=1.0, size_y=1.0)

    # test for exception when count_y is less than 1
    def test_exception_count_y_less_than_one(self):
        with self.assertRaises(ValueError):
            pattern_grid(3, -1, size_x=1.0, size_y=1.0)


class PatternDistributeTest(PatternTestBase):
    def test_3x3_exact_fit(self):
        size_x = 3
        size_y = 3
        tile_x = 1
        tile_y = 1
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=False)
        expected_result = [
            (0.5, 0.5), (1.5, 0.5), (2.5, 0.5),
            (0.5, 1.5), (1.5, 1.5), (2.5, 1.5),
            (0.5, 2.5), (1.5, 2.5), (2.5, 2.5)
        ]
        self.assertPatternEqual(result, expected_result)

    def test_3x3_exact_fit_origin(self):
        size_x = 3
        size_y = 3
        tile_x = 1
        tile_y = 1
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=False, result_pos="origin")
        expected_result = [
            (0.0, 0.0), (1.0, 0.0), (2.0, 0.0),
            (0.0, 1.0), (1.0, 1.0), (2.0, 1.0),
            (0.0, 2.0), (1.0, 2.0), (2.0, 2.0)
        ]
        self.assertPatternEqual(result, expected_result)

    def test_3x3_loose_fit_origin(self):
        size_x = 3.2
        size_y = 3.2
        tile_x = 1
        tile_y = 1
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=False, result_pos="origin")
        expected_result = [
            (0.0, 0.0), (1.1, 0.0), (2.2, 0.0),
            (0.0, 1.1), (1.1, 1.1), (2.2, 1.1),
            (0.0, 2.2), (1.1, 2.2), (2.2, 2.2)
        ]
        self.assertPatternEqual(result, expected_result)

    def test_3x3_exact_fit_center(self):
        size_x = 3
        size_y = 3
        tile_x = 1
        tile_y = 1
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=True)
        expected_result = [
            (-1.0, -1.0), (0.0, -1.0), (1.0, -1.0),
            (-1.0, 0.0), (0.0, 0.0), (1.0, 0.0),
            (-1.0, 1.0), (0.0, 1.0), (1.0, 1.0)
        ]
        self.assertPatternEqual(result, expected_result)

    def test_3x3_loose_fit_center(self):
        size_x = 3.2
        size_y = 3.2
        tile_x = 1
        tile_y = 1
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=True)
        expected_result = [
            (-1.1, -1.1), (-0.0, -1.1), (1.1, -1.1),
            (-1.1, 0.0), (-0.0, 0.0), (1.1, 0.0),
            (-1.1, 1.1), (-0.0, 1.1), (1.1, 1.1)
        ]
        self.assertPatternEqual(result, expected_result)

    def test_3x1_exact_fit(self):
        size_x = 3
        size_y = 1
        tile_x = 1
        tile_y = 1
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=False)
        expected_result = [
            (0.5, 0.5), (1.5, 0.5), (2.5, 0.5)
        ]
        self.assertPatternEqual(result, expected_result)

    def test_3x1_exact_fit_origin(self):
        size_x = 3
        size_y = 1
        tile_x = 1
        tile_y = 1
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=False, result_pos="origin")
        expected_result = [
            (0.0, 0.0), (1.0, 0.0), (2.0, 0.0)
        ]
        self.assertPatternEqual(result, expected_result)

    def test_3x1_loose_fit_origin(self):
        size_x = 3.2
        size_y = 1
        tile_x = 1
        tile_y = 1
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=False, result_pos="origin")
        expected_result = [
            (0.0, 0.0), (1.1, 0.0), (2.2, 0.0)
        ]
        self.assertPatternEqual(result, expected_result)

    def test_3x1_exact_fit_center(self):
        size_x = 3
        size_y = 1
        tile_x = 1
        tile_y = 1
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=True)
        expected_result = [
            (-1.0, 0.0), (0.0, 0.0), (1.0, 0.0)
        ]
        self.assertPatternEqual(result, expected_result)

    def test_3x1_loose_fit_center(self):
        size_x = 3.2
        size_y = 1
        tile_x = 1
        tile_y = 1
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=True)
        expected_result = [
            (-1.1, 0.0), (-0.0, 0.0), (1.1, 0.0)
        ]
        self.assertPatternEqual(result, expected_result)

    def test_1x3_exact_fit(self):
        size_x = 1
        size_y = 3
        tile_x = 1
        tile_y = 1
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=False)
        expected_result = [
            (0.5, 0.5), (0.5, 1.5), (0.5, 2.5)
        ]
        self.assertPatternEqual(result, expected_result)

    def test_1x3_exact_fit_origin(self):
        size_x = 1
        size_y = 3
        tile_x = 1
        tile_y = 1
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=False, result_pos="origin")
        expected_result = [
            (0.0, 0.0), (0.0, 1.0), (0.0, 2.0)
        ]
        self.assertPatternEqual(result, expected_result)

    def test_1x3_loose_fit_origin(self):
        size_x = 1
        size_y = 3.2
        tile_x = 1
        tile_y = 1
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=False, result_pos="origin")
        expected_result = [
            (0.0, 0.0), (0.0, 1.1), (0.0, 2.2)
        ]
        self.assertPatternEqual(result, expected_result)

    def test_1x3_exact_fit_center(self):
        size_x = 1
        size_y = 3
        tile_x = 1
        tile_y = 1
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=True)
        expected_result = [
            (0.0, -1.0), (0.0, 0.0), (0.0, 1.0)
        ]
        self.assertPatternEqual(result, expected_result)

    def test_1x3_loose_fit_center(self):
        size_x = 1
        size_y = 3.2
        tile_x = 1
        tile_y = 1
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=True)
        expected_result = [
            (0.0, -1.1), (0.0, -0.0), (0.0, 1.1)
        ]
        self.assertPatternEqual(result, expected_result)

    def test_1x1_exact_fit(self):
        size_x = 1
        size_y = 1
        tile_x = 1
        tile_y = 1
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=False)
        expected_result = [
            (0.5, 0.5)
        ]
        self.assertPatternEqual(result, expected_result)

    def test_1x1_exact_fit_origin(self):
        size_x = 1
        size_y = 1
        tile_x = 1
        tile_y = 1
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=False, result_pos="origin")
        expected_result = [
            (0.0, 0.0)
        ]
        self.assertPatternEqual(result, expected_result)

    def test_1x1_loose_fit_x_origin(self):
        size_x = 1.2
        size_y = 1
        tile_x = 1
        tile_y = 1
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=False, result_pos="origin")
        expected_result = [
            (0.1, 0.0)
        ]
        self.assertPatternEqual(result, expected_result)

    def test_1x1_loose_fit_y_origin(self):
        size_x = 1
        size_y = 1.2
        tile_x = 1
        tile_y = 1
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=False, result_pos="origin")
        expected_result = [
            (0.0, 0.1)
        ]
        self.assertPatternEqual(result, expected_result)

    def test_1x1_exact_fit_center(self):
        size_x = 1
        size_y = 1
        tile_x = 1
        tile_y = 1
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=True)
        expected_result = [
            (0.0, 0.0)
        ]
        self.assertPatternEqual(result, expected_result)

    def test_1x1_too_small_x(self):
        size_x = 0.5
        size_y = 1
        tile_x = 1
        tile_y = 1
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=False)
        expected_result = []
        self.assertPatternEqual(result, expected_result)

    def test_1x1_too_small_y(self):
        size_x = 1
        size_y = 0.5
        tile_x = 1
        tile_y = 1
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=False)
        expected_result = []
        self.assertPatternEqual(result, expected_result)

    def test_6x2_tile_3x1_origin(self):
        size_x = 6
        size_y = 2
        tile_x = 3
        tile_y = 1
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=False, result_pos="origin")
        expected_result = [
            (0.0, 0.0), (3.0, 0.0),
            (0.0, 1.0), (3.0, 1.0)
        ]
        self.assertPatternEqual(result, expected_result)

    def test_6x2_tile_3x1_center_origin(self):
        size_x = 6
        size_y = 2
        tile_x = 3
        tile_y = 1
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=True, result_pos="origin")
        expected_result = [
            (-3.0, -1.0), (-3.0, 0.0),
            (0.0, -1.0), (0.0, 0.0)
        ]
        self.assertPatternEqual(result, expected_result)

    def test_6x2_tile_3x1_center(self):
        size_x = 6
        size_y = 2
        tile_x = 3
        tile_y = 1
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=True)
        expected_result = [
            (-1.5, -0.5), (1.5, -0.5),
            (-1.5, 0.5), (1.5, 0.5)
        ]
        self.assertPatternEqual(result, expected_result)

    def test_2x6_tile_1x3(self):
        size_x = 2
        size_y = 6
        tile_x = 1
        tile_y = 3
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=False, result_pos="origin")
        expected_result = [
            (0.0, 0.0), (0.0, 3.0),
            (1.0, 0.0), (1.0, 3.0)
        ]
        self.assertPatternEqual(result, expected_result)

    def test_3x3_min_spacing_x_1(self):
        size_x = 3
        size_y = 3
        tile_x = 1
        tile_y = 1
        min_spacing = 1
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=False, min_spacing_x=min_spacing)
        expected_result = [
            (0.5, 0.5), (2.5, 0.5),
            (0.5, 1.5), (2.5, 1.5),
            (0.5, 2.5), (2.5, 2.5)
        ]
        self.assertPatternEqual(result, expected_result)

    def test_3x3_min_spacing_y_1(self):
        size_x = 3
        size_y = 3
        tile_x = 1
        tile_y = 1
        min_spacing = 1
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=False, min_spacing_y=min_spacing)
        expected_result = [
            (0.5, 0.5), (1.5, 0.5), (2.5, 0.5),
            (0.5, 2.5), (1.5, 2.5), (2.5, 2.5)
        ]
        self.assertPatternEqual(result, expected_result)

    def test_3x3_min_spacing_xy_1(self):
        size_x = 3
        size_y = 3
        tile_x = 1
        tile_y = 1
        min_spacing = 1
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=False, min_spacing_x=min_spacing, min_spacing_y=min_spacing)
        expected_result = [
            (0.5, 0.5), (2.5, 0.5),
            (0.5, 2.5), (2.5, 2.5)
        ]
        self.assertPatternEqual(result, expected_result)

    def test_3x3_min_spacing_xy_1_center(self):
        size_x = 3
        size_y = 3
        tile_x = 1
        tile_y = 1
        min_spacing = 1
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=True, min_spacing_x=min_spacing, min_spacing_y=min_spacing)
        expected_result = [
            (-1.0, -1.0), (1.0, -1.0),
            (-1.0, 1.0), (1.0, 1.0)
        ]
        self.assertPatternEqual(result, expected_result)

    def test_3x3_min_spacing_xy_2_center(self):
        size_x = 3
        size_y = 3
        tile_x = 1
        tile_y = 1
        min_spacing = 2
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=True, min_spacing_x=min_spacing, min_spacing_y=min_spacing)
        expected_result = [
            (0, 0)
        ]
        self.assertPatternEqual(result, expected_result)

    def test_1x1_min_spacing_xy_2_center(self):
        size_x = 1
        size_y = 1
        tile_x = 1
        tile_y = 1
        min_spacing = 2
        result = pattern_distribute(size_x, size_y, tile_x, tile_y, center=True, min_spacing_x=min_spacing, min_spacing_y=min_spacing)
        expected_result = [
            (0, 0)
        ]
        self.assertPatternEqual(result, expected_result)


class PatternDistributeStretchTest(PatternTestBase):

    def test_1x1_into_2x2_centered(self):
        count_x = 1
        count_y = 1
        size_x = 2
        size_y = 2
        result = pattern_distribute_stretch(size_x, size_y, count_x=count_x, count_y=count_y)
        expected_result = [
            ((-1, 1), (-1, 1))
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_1x1_into_6x4_centered(self):
        count_x = 1
        count_y = 1
        size_x = 6
        size_y = 4
        result = pattern_distribute_stretch(size_x, size_y, count_x=count_x, count_y=count_y)
        expected_result = [
            ((-3, 3), (-2, 2))
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_1x1_into_1x10_uncentered(self):
        count_x = 1
        count_y = 1
        size_x = 1
        size_y = 10
        result = pattern_distribute_stretch(size_x, size_y, count_x=count_x, count_y=count_y, center=False)
        expected_result = [
            ((0, 1), (0, 10))
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_2x1_into_2x2_centered(self):
        count_x = 2
        count_y = 1
        size_x = 2
        size_y = 2
        result = pattern_distribute_stretch(size_x, size_y, count_x=count_x, count_y=count_y)
        expected_result = [
            ((-1, 0), (-1, 1)),
            ((0, 1), (-1, 1))
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_3x1_into_6x4_centered(self):
        count_x = 3
        count_y = 1
        size_x = 6
        size_y = 4
        result = pattern_distribute_stretch(size_x, size_y, count_x=count_x, count_y=count_y)
        expected_result = [
            ((-3, -1), (-2, 2)),
            ((-1, 1), (-2, 2)),
            ((1, 3), (-2, 2))
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_1x2_into_6x4_centered(self):
        count_x = 1
        count_y = 2
        size_x = 6
        size_y = 4
        result = pattern_distribute_stretch(size_x, size_y, count_x=count_x, count_y=count_y)
        expected_result = [
            ((-3, 3), (-2, 0)),
            ((-3, 3), (0, 2))
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_1x4_into_6x4_centered(self):
        count_x = 1
        count_y = 4
        size_x = 6
        size_y = 4
        result = pattern_distribute_stretch(size_x, size_y, count_x=count_x, count_y=count_y)
        expected_result = [
            ((-3, 3), (-2, -1)),
            ((-3, 3), (-1, 0)),
            ((-3, 3), (0, 1)),
            ((-3, 3), (1, 2))
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_2x2_into_6x4_centered(self):
        count_x = 2
        count_y = 2
        size_x = 6
        size_y = 4
        result = pattern_distribute_stretch(size_x, size_y, count_x=count_x, count_y=count_y)
        expected_result = [
            ((-3, 0), (-2, 0)),
            ((0, 3), (-2, 0)),
            ((-3, 0), (0, 2)),
            ((0, 3), (0, 2))
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_2x1_into_6x2_spacing_2(self):
        count_x = 2
        count_y = 1
        size_x = 6
        size_y = 2
        spacing_x = 2
        spacing_y = 2
        result = pattern_distribute_stretch(size_x, size_y, count_x=count_x, count_y=count_y, spacing_x=spacing_x, spacing_y=spacing_y)
        expected_result = [
            ((-3, -1), (-1, 1)),
            ((1, 3), (-1, 1))
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_1x2_into_6x6_spacing_2(self):
        count_x = 1
        count_y = 2
        size_x = 6
        size_y = 6
        spacing_x = 2
        spacing_y = 2
        result = pattern_distribute_stretch(size_x, size_y, count_x=count_x, count_y=count_y, spacing_x=spacing_x, spacing_y=spacing_y)
        expected_result = [
            ((-3, 3), (-3, -1)),
            ((-3, 3), (1, 3))
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_2x2_into_6x6_spacing_2(self):
        count_x = 2
        count_y = 2
        size_x = 6
        size_y = 6
        spacing_x = 2
        spacing_y = 2
        result = pattern_distribute_stretch(size_x, size_y, count_x=count_x, count_y=count_y, spacing_x=spacing_x, spacing_y=spacing_y)
        expected_result = [
            ((-3, -1), (-3, -1)),
            ((1, 3), (-3, -1)),
            ((-3, -1), (1, 3)),
            ((1, 3), (1, 3))
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_3x5_into_5x9_spacing_1_uncentered(self):
        count_x = 3
        count_y = 5
        size_x = 5
        size_y = 9
        spacing_x = 1
        spacing_y = 1
        result = pattern_distribute_stretch(size_x, size_y, count_x=count_x, count_y=count_y,
                                            spacing_x=spacing_x, spacing_y=spacing_y, center=False)
        expected_result = [
            ((0, 1), (0, 1)),
            ((2, 3), (0, 1)),
            ((4, 5), (0, 1)),
            ((0, 1), (2, 3)),
            ((2, 3), (2, 3)),
            ((4, 5), (2, 3)),
            ((0, 1), (4, 5)),
            ((2, 3), (4, 5)),
            ((4, 5), (4, 5)),
            ((0, 1), (6, 7)),
            ((2, 3), (6, 7)),
            ((4, 5), (6, 7)),
            ((0, 1), (8, 9)),
            ((2, 3), (8, 9)),
            ((4, 5), (8, 9))
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_3x1_minx1_miny1(self):
        size_x = 3
        size_y = 1
        min_tile_size_x = 1
        min_tile_size_y = 1
        result = pattern_distribute_stretch(size_x, size_y, min_tile_size_x=min_tile_size_x, min_tile_size_y=min_tile_size_y, center=False)
        expected_result = [
            ((0, 1), (0, 1)),
            ((1, 2), (0, 1)),
            ((2, 3), (0, 1))
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_3x1_minx2_miny1(self):
        size_x = 3
        size_y = 1
        min_tile_size_x = 2
        min_tile_size_y = 1
        result = pattern_distribute_stretch(size_x, size_y, min_tile_size_x=min_tile_size_x, min_tile_size_y=min_tile_size_y, center=False)
        expected_result = [
            ((0, 3), (0, 1))
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_3x1_minx1_miny2(self):
        size_x = 3
        size_y = 1
        min_tile_size_x = 1
        min_tile_size_y = 2
        result = pattern_distribute_stretch(size_x, size_y, min_tile_size_x=min_tile_size_x, min_tile_size_y=min_tile_size_y, center=False)
        expected_result = [
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_1x3_minx1_miny1(self):
        size_x = 1
        size_y = 3
        min_tile_size_x = 1
        min_tile_size_y = 1
        result = pattern_distribute_stretch(size_x, size_y, min_tile_size_x=min_tile_size_x, min_tile_size_y=min_tile_size_y, center=False)
        expected_result = [
            ((0, 1), (0, 1)),
            ((0, 1), (1, 2)),
            ((0, 1), (2, 3))
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_1x3_minx1_miny2(self):
        size_x = 1
        size_y = 3
        min_tile_size_x = 1
        min_tile_size_y = 2
        result = pattern_distribute_stretch(size_x, size_y, min_tile_size_x=min_tile_size_x, min_tile_size_y=min_tile_size_y, center=False)
        expected_result = [
            ((0, 1), (0, 3))
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_1x3_minx2_miny1(self):
        size_x = 1
        size_y = 3
        min_tile_size_x = 2
        min_tile_size_y = 1
        result = pattern_distribute_stretch(size_x, size_y, min_tile_size_x=min_tile_size_x, min_tile_size_y=min_tile_size_y, center=False)
        expected_result = [
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_3x3_minx1_miny1(self):
        size_x = 3
        size_y = 3
        min_tile_size_x = 1
        min_tile_size_y = 1
        result = pattern_distribute_stretch(size_x, size_y, min_tile_size_x=min_tile_size_x, min_tile_size_y=min_tile_size_y, center=False)
        expected_result = [
            ((0, 1), (0, 1)), ((1, 2), (0, 1)), ((2, 3), (0, 1)),
            ((0, 1), (1, 2)), ((1, 2), (1, 2)), ((2, 3), (1, 2)),
            ((0, 1), (2, 3)), ((1, 2), (2, 3)), ((2, 3), (2, 3))
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_3x3_minx1_miny1_spacingx1(self):
        size_x = 3
        size_y = 3
        min_tile_size_x = 1
        min_tile_size_y = 1
        spacing_x = 1
        result = pattern_distribute_stretch(size_x, size_y, min_tile_size_x=min_tile_size_x, min_tile_size_y=min_tile_size_y,
                                            spacing_x=spacing_x, center=False)
        expected_result = [
            ((0, 1), (0, 1)), ((2, 3), (0, 1)),
            ((0, 1), (1, 2)), ((2, 3), (1, 2)),
            ((0, 1), (2, 3)), ((2, 3), (2, 3))
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_3x3_minx1_miny1_spacingy1(self):
        size_x = 3
        size_y = 3
        min_tile_size_x = 1
        min_tile_size_y = 1
        spacing_y = 1
        result = pattern_distribute_stretch(size_x, size_y, min_tile_size_x=min_tile_size_x, min_tile_size_y=min_tile_size_y,
                                            spacing_y=spacing_y, center=False)
        expected_result = [
            ((0, 1), (0, 1)), ((1, 2), (0, 1)), ((2, 3), (0, 1)),
            ((0, 1), (2, 3)), ((1, 2), (2, 3)), ((2, 3), (2, 3))
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_3x3_minx1_miny1_spacingx1_spacingy1(self):
        size_x = 3
        size_y = 3
        min_tile_size_x = 1
        min_tile_size_y = 1
        spacing_x = 1
        spacing_y = 1
        result = pattern_distribute_stretch(size_x, size_y, min_tile_size_x=min_tile_size_x, min_tile_size_y=min_tile_size_y,
                                            spacing_x=spacing_x, spacing_y=spacing_y, center=False)
        expected_result = [
            ((0, 1), (0, 1)), ((2, 3), (0, 1)),
            ((0, 1), (2, 3)), ((2, 3), (2, 3))
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_3x1_maxx1_maxy1(self):
        size_x = 3
        size_y = 1
        max_tile_size_x = 1
        max_tile_size_y = 1
        result = pattern_distribute_stretch(size_x, size_y, max_tile_size_x=max_tile_size_x, max_tile_size_y=max_tile_size_y, center=False)
        expected_result = [
            ((0, 1), (0, 1)),
            ((1, 2), (0, 1)),
            ((2, 3), (0, 1))
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_3x1_maxx2_maxy1(self):
        size_x = 3
        size_y = 1
        max_tile_size_x = 2
        max_tile_size_y = 1
        result = pattern_distribute_stretch(size_x, size_y, max_tile_size_x=max_tile_size_x, max_tile_size_y=max_tile_size_y, center=False)
        expected_result = [
            ((0, 1.5), (0, 1)),
            ((1.5, 3), (0, 1))
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_3x1_maxx1_maxy2(self):
        size_x = 3
        size_y = 1
        max_tile_size_x = 1
        max_tile_size_y = 2
        result = pattern_distribute_stretch(size_x, size_y, max_tile_size_x=max_tile_size_x, max_tile_size_y=max_tile_size_y, center=False)
        expected_result = [
            ((0, 1), (0, 1)),
            ((1, 2), (0, 1)),
            ((2, 3), (0, 1))
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_1x3_maxx1_maxy1(self):
        size_x = 1
        size_y = 3
        max_tile_size_x = 1
        max_tile_size_y = 1
        result = pattern_distribute_stretch(size_x, size_y, max_tile_size_x=max_tile_size_x, max_tile_size_y=max_tile_size_y, center=False)
        expected_result = [
            ((0, 1), (0, 1)),
            ((0, 1), (1, 2)),
            ((0, 1), (2, 3))
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_1x3_maxx1_maxy2(self):
        size_x = 1
        size_y = 3
        max_tile_size_x = 1
        max_tile_size_y = 2
        result = pattern_distribute_stretch(size_x, size_y, max_tile_size_x=max_tile_size_x, max_tile_size_y=max_tile_size_y, center=False)
        expected_result = [
            ((0, 1), (0, 1.5)),
            ((0, 1), (1.5, 3))
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_1x3_maxx1_maxy1_spacing1(self):
        size_x = 1
        size_y = 3
        max_tile_size_x = 1
        max_tile_size_y = 1
        spacing_x = 1
        spacing_y = 1
        result = pattern_distribute_stretch(size_x, size_y, max_tile_size_x=max_tile_size_x, max_tile_size_y=max_tile_size_y,
                                            spacing_x=spacing_x, spacing_y=spacing_y, center=False)
        expected_result = [
            ((0, 1), (0, 1)),
            ((0, 1), (2, 3))
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_3x1_maxx1_maxy1_spacing1(self):
        size_x = 3
        size_y = 1
        max_tile_size_x = 1
        max_tile_size_y = 1
        spacing_x = 1
        spacing_y = 1
        result = pattern_distribute_stretch(size_x, size_y, max_tile_size_x=max_tile_size_x, max_tile_size_y=max_tile_size_y,
                                            spacing_x=spacing_x, spacing_y=spacing_y, center=False)
        expected_result = [
            ((0, 1), (0, 1)),
            ((2, 3), (0, 1))
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_2x2_minx1_minx1_spacing1(self):
        size_x = 2
        size_y = 2
        min_tile_size_x = 1
        min_tile_size_y = 1
        spacing_x = 1
        spacing_y = 1
        result = pattern_distribute_stretch(size_x, size_y, min_tile_size_x=min_tile_size_x, min_tile_size_y=min_tile_size_y,
                                            spacing_x=spacing_x, spacing_y=spacing_y, center=False)
        expected_result = [
            ((0, 2), (0, 2))
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_1x1_minx1_miny1_spacing10(self):
        size_x = 1
        size_y = 1
        min_tile_size_x = 1
        min_tile_size_y = 1
        spacing_x = 10
        spacing_y = 10
        result = pattern_distribute_stretch(size_x, size_y, min_tile_size_x=min_tile_size_x, min_tile_size_y=min_tile_size_y,
                                            spacing_x=spacing_x, spacing_y=spacing_y, center=False)
        expected_result = [
            ((0, 1), (0, 1))
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_2x2_maxx5_maxy5_minx3(self):
        size_x = 2
        size_y = 2
        max_tile_size_x = 5
        max_tile_size_y = 5
        min_tile_size_x = 3
        min_tile_size_y = 3
        result = pattern_distribute_stretch(size_x, size_y, max_tile_size_x=max_tile_size_x, max_tile_size_y=max_tile_size_y,
                                            min_tile_size_x=min_tile_size_x, min_tile_size_y=min_tile_size_y, center=False)
        expected_result = [
        ]
        self.assertPattern2Equal(result, expected_result)

    def test_2x2_maxx5_maxy5_miny3(self):
        size_x = 2
        size_y = 2
        max_tile_size_x = 5
        max_tile_size_y = 5
        min_tile_size_x = 1
        min_tile_size_y = 3
        result = pattern_distribute_stretch(size_x, size_y, max_tile_size_x=max_tile_size_x, max_tile_size_y=max_tile_size_y,
                                            min_tile_size_x=min_tile_size_x, min_tile_size_y=min_tile_size_y, center=False)
        expected_result = [
        ]
        self.assertPattern2Equal(result, expected_result)


if __name__ == '__main__':
    unittest.main()
