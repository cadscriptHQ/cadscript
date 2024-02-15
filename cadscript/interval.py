# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

from typing import Tuple
from .typedefs import Vector2DType, Vector3DType


class Interval1D:
    """
    A class to represent a 1D interval.
    """
    x1: float
    x2: float

    def __init__(self, x1: float, x2: float):
        self.set(x1, x2)

    def set(self, x1: float, x2: float) -> 'Interval1D':
        if x1 > x2:
            raise ValueError("x1 must be less than or equal to x2")
        self.x1 = x1
        self.x2 = x2
        return self

    @staticmethod
    def from_tuple(extent: Tuple[float, float]) -> 'Interval1D':
        return Interval1D(extent[0], extent[1])

    def __repr__(self):
        return f"Interval1D({self.x1}, {self.x2})"

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Interval1D):
            return False
        return self.x1 == __value.x1 and self.x2 == __value.x2

    def copy(self) -> 'Interval1D':
        return Interval1D(self.x1, self.x2)

    @property
    def min(self) -> float:
        return self.x1

    @property
    def max(self) -> float:
        return self.x1

    def size(self) -> float:
        return self.x2 - self.x1

    def tuple(self) -> Tuple[float, float]:
        return (self.x1, self.x2)

    def center(self) -> float:
        return (self.x1 + self.x2) / 2

    def expand(self, offset: float) -> 'Interval1D':
        return self.set(self.x1 - offset, self.x2 + offset)

    def shrink(self, offset: float, raise_if_zero: bool = True) -> 'Interval1D':
        if raise_if_zero and (self.x2 - self.x1) < 2 * offset:
            raise ValueError("Interval is too small to shrink")
        return self.set(self.x1 + offset, self.x2 - offset)


class Interval2D:
    """
    A class to represent a 2D interval or a 2D bounding box.
    """

    x1: float
    x2: float
    y1: float
    y2: float

    def __init__(self, x1: float, x2: float, y1: float, y2: float):
        self.set(x1, x2, y1, y2)

    def set(self, x1: float, x2: float, y1: float, y2: float) -> 'Interval2D':
        if x1 > x2:
            raise ValueError("x1 must be less than or equal to x2")
        if y1 > y2:
            raise ValueError("y1 must be less than or equal to y2")
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        return self

    @staticmethod
    def from_tuples(x: Tuple[float, float], y: Tuple[float, float]) -> 'Interval2D':
        return Interval2D(x[0], x[1], y[0], y[1])

    def __repr__(self):
        return f"Interval2D({self.x1}, {self.x2}), ({self.y1}, {self.y2})"

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Interval2D):
            return False
        return self.x1 == __value.x1 and self.x2 == __value.x2 and self.y1 == __value.y1 and self.y2 == __value.y2

    def copy(self) -> 'Interval2D':
        return Interval2D(self.x1, self.x2, self.y1, self.y2)

    @property
    def min_x(self) -> float:
        return self.x1

    @property
    def max_x(self) -> float:
        return self.x2

    @property
    def min_y(self) -> float:
        return self.y1

    @property
    def max_y(self) -> float:
        return self.y2

    def size_x(self) -> float:
        return self.x2 - self.x1

    def size_y(self) -> float:
        return self.y2 - self.y1

    def extent_x(self) -> Interval1D:
        return Interval1D(self.x1, self.x2)

    def extent_y(self) -> Interval1D:
        return Interval1D(self.y1, self.y2)

    def tuple_x(self) -> Tuple[float, float]:
        return (self.x1, self.x2)

    def tuple_y(self) -> Tuple[float, float]:
        return (self.y1, self.y2)

    def tuple_xy(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        return (self.tuple_x(), self.tuple_y())

    def min_corner(self) -> Vector2DType:
        return (self.x1, self.y1)

    def max_corner(self) -> Vector2DType:
        return (self.x2, self.y2)

    def center(self) -> Vector2DType:
        return ((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)

    def center_x(self) -> float:
        return (self.x1 + self.x2) / 2

    def center_y(self) -> float:
        return (self.y1 + self.y2) / 2

    def expand_x(self, offset: float) -> 'Interval2D':
        return self.set(self.x1 - offset, self.x2 + offset, self.y1, self.y2)

    def expand_y(self, offset: float) -> 'Interval2D':
        return self.set(self.x1, self.x2, self.y1 - offset, self.y2 + offset)

    def expand(self, offset: float) -> 'Interval2D':
        return self.set(self.x1 - offset, self.x2 + offset, self.y1 - offset, self.y2 + offset)

    def shrink_x(self, offset: float, raise_if_zero: bool = True) -> 'Interval2D':
        if raise_if_zero and (self.x2 - self.x1) < 2 * offset:
            raise ValueError("Interval is too small to shrink")
        return self.set(self.x1 + offset, self.x2 - offset, self.y1, self.y2)

    def shrink_y(self, offset: float, raise_if_zero: bool = True) -> 'Interval2D':
        if raise_if_zero and (self.y2 - self.y1) < 2 * offset:
            raise ValueError("Interval is too small to shrink")
        return self.set(self.x1, self.x2, self.y1 + offset, self.y2 - offset)

    def shrink(self, offset: float, raise_if_zero: bool = True) -> 'Interval2D':
        return self.shrink_x(offset, raise_if_zero).shrink_y(offset, raise_if_zero)


class Interval3D:
    """
    A class to represent a 3D interval or a 3D bounding box.
    """
    x1: float
    x2: float
    y1: float
    y2: float
    z1: float
    z2: float

    def __init__(self, x1: float, x2: float, y1: float, y2: float, z1: float, z2: float):
        self.set(x1, x2, y1, y2, z1, z2)

    def set(self, x1: float, x2: float, y1: float, y2: float, z1: float, z2: float) -> 'Interval3D':
        if x1 > x2:
            raise ValueError("x1 must be less than or equal to x2")
        if y1 > y2:
            raise ValueError("y1 must be less than or equal to y2")
        if z1 > z2:
            raise ValueError("z1 must be less than or equal to z2")
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2
        return self

    @staticmethod
    def from_tuples(x: Tuple[float, float], y: Tuple[float, float], z: Tuple[float, float]) -> 'Interval3D':
        return Interval3D(x[0], x[1], y[0], y[1], z[0], z[1])

    def __repr__(self):
        return f"Interval3D({self.x1}, {self.x2}), ({self.y1}, {self.y2}), ({self.z1}, {self.z2})"

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Interval3D):
            return False
        return (self.x1 == __value.x1 and self.x2 == __value.x2 and self.y1 == __value.y1 and
                self.y2 == __value.y2 and self.z1 == __value.z1 and self.z2 == __value.z2)

    def copy(self) -> 'Interval3D':
        return Interval3D(self.x1, self.x2, self.y1, self.y2, self.z1, self.z2)

    @property
    def min_x(self) -> float:
        return self.x1

    @property
    def max_x(self) -> float:
        return self.x2

    @property
    def min_y(self) -> float:
        return self.y1

    @property
    def max_y(self) -> float:
        return self.y2

    @property
    def min_z(self) -> float:
        return self.z1

    @property
    def max_z(self) -> float:
        return self.z2

    def size_x(self) -> float:
        return self.x2 - self.x1

    def size_y(self) -> float:
        return self.y2 - self.y1

    def size_z(self) -> float:
        return self.z2 - self.z1

    def extent_x(self) -> Interval1D:
        return Interval1D(self.x1, self.x2)

    def extent_y(self) -> Interval1D:
        return Interval1D(self.y1, self.y2)

    def extent_z(self) -> Interval1D:
        return Interval1D(self.z1, self.z2)

    def tuple_x(self) -> Tuple[float, float]:
        return (self.x1, self.x2)

    def tuple_y(self) -> Tuple[float, float]:
        return (self.y1, self.y2)

    def tuple_z(self) -> Tuple[float, float]:
        return (self.z1, self.z2)

    def tuple_xyz(self) -> Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]]:
        return (self.tuple_x(), self.tuple_y(), self.tuple_z())

    def min_corner(self) -> Vector3DType:
        return (self.x1, self.y1, self.z1)

    def max_corner(self) -> Vector3DType:
        return (self.x2, self.y2, self.z2)

    def center(self) -> Vector3DType:
        return ((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2, (self.z1 + self.z2) / 2)

    def center_x(self) -> float:
        return (self.x1 + self.x2) / 2

    def center_y(self) -> float:
        return (self.y1 + self.y2) / 2

    def center_z(self) -> float:
        return (self.z1 + self.z2) / 2

    def expand_x(self, offset: float) -> 'Interval3D':
        return self.set(self.x1 - offset, self.x2 + offset, self.y1, self.y2, self.z1, self.z2)

    def expand_y(self, offset: float) -> 'Interval3D':
        return self.set(self.x1, self.x2, self.y1 - offset, self.y2 + offset, self.z1, self.z2)

    def expand_z(self, offset: float) -> 'Interval3D':
        return self.set(self.x1, self.x2, self.y1, self.y2, self.z1 - offset, self.z2 + offset)

    def expand(self, offset: float) -> 'Interval3D':
        return self.set(self.x1 - offset, self.x2 + offset, self.y1 - offset, self.y2 + offset, self.z1 - offset, self.z2 + offset)

    def shrink_x(self, offset: float, raise_if_zero: bool = True) -> 'Interval3D':
        if raise_if_zero and (self.x2 - self.x1) < 2 * offset:
            raise ValueError("Interval is too small to shrink")
        return self.set(self.x1 + offset, self.x2 - offset, self.y1, self.y2, self.z1, self.z2)

    def shrink_y(self, offset: float, raise_if_zero: bool = True) -> 'Interval3D':
        if raise_if_zero and (self.y2 - self.y1) < 2 * offset:
            raise ValueError("Interval is too small to shrink")
        return self.set(self.x1, self.x2, self.y1 + offset, self.y2 - offset, self.z1, self.z2)

    def shrink_z(self, offset: float, raise_if_zero: bool = True) -> 'Interval3D':
        if raise_if_zero and (self.z2 - self.z1) < 2 * offset:
            raise ValueError("Interval is too small to shrink")
        return self.set(self.x1, self.x2, self.y1, self.y2, self.z1 + offset, self.z2 - offset)

    def shrink(self, offset: float, raise_if_zero: bool = True) -> 'Interval3D':
        return self.shrink_x(offset, raise_if_zero).shrink_y(offset, raise_if_zero).shrink_z(offset, raise_if_zero)
