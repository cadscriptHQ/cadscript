# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

from itertools import product
from typing import Optional

from .typedefs import DimensionDefinitionType, CenterDefinitionType
from .helpers import get_center_flags, get_dimension, get_dimensions


def pattern_rect(sizex: DimensionDefinitionType, sizey: DimensionDefinitionType, center: CenterDefinitionType = True):
    """
    Generate a rectangular pattern.

    Args:
        sizex (float): The width of the rectangle.
        sizey (float): The height of the rectangle.
        center (bool, optional): Whether to center the rectangle. If False, the rectangle will start from the origin.
            Can also be "X" or "Y" to center in only one direction.
            Defaults to True.

    Returns:
        list: A list of tuples representing the vertices of the rectangle in clockwise order.
    """
    dimx, dimy = get_dimensions([sizex, sizey], center)
    return [(dimx[0], dimy[0]), (dimx[0], dimy[1]), (dimx[1], dimy[1]), (dimx[1], dimy[0])]


def pattern_grid(
        count_x: int,
        count_y: int,
        *,
        spacing_x: Optional[float] = None,
        spacing_y: Optional[float] = None,
        size_x: Optional[DimensionDefinitionType] = None,
        size_y: Optional[DimensionDefinitionType] = None,
        center: CenterDefinitionType = True):
    """
    Generate a grid pattern of locations based on the given parameters.

    Args:
        count_x (int): The number of grid points in the x-direction.
            If 1 is passed, the result will be a 1D grid, i.e. points along the y-axis.
        count_y (int): The number of grid points in the y-direction.
            If 1 is passed, the result will be a 1D grid, i.e. points along the x-axis.
        spacing_x (float, optional): The spacing between grid points in the x-direction.
            If not specified, it will be calculated based on the size_x parameter.
        spacing_y (float, optional): The spacing between grid points in the y-direction.
            If not specified, it will be calculated based on the size_y parameter.
        size_x (DimensionDefinitionType, optional): The size of the grid in the x-direction.
            If not specified, it will be calculated based on the spacing_x parameter.
        size_y (DimensionDefinitionType, optional): The size of the grid in the y-direction.
            If not specified, it will be calculated based on the spacing_y parameter.
        center (CenterDefinitionType, optional): Determines whether the grid is centered.
            If True, the grid will be centered.
            If False, the grid will start from the origin. Can also be "X" or "Y" to center in only one direction.
            Defaults to True.

    Returns:
        List[Vector2DType]: A list of (x, y) coordinates representing the locations of the grid points.
    """
    locs = []
    if count_x < 1 or count_y < 1:
        raise ValueError("count_x and count_y must be greater than 0")
    center_x, center_y, _ = get_center_flags(center)
    spacing_x, offset_x = __get_spacing(count_x, spacing_x, size_x, center_x, "_x")
    spacing_y, offset_y = __get_spacing(count_y, spacing_y, size_y, center_y, "_y")

    for i, j in product(range(count_x), range(count_y)):
        locs.append((i * spacing_x + offset_x, j * spacing_y + offset_y))
    return locs


def __get_spacing(count, spacing, size, center, dim_str):
    '''
    Helper function for pattern_grid(). Calculates the spacing and offset based on the given parameters.
    '''
    offset = 0
    if count > 1:
        if spacing is None and size is None:
            raise ValueError(f"Either spacing{dim_str} or size{dim_str} must be specified")
        if size is not None:
            if spacing is not None:
                raise ValueError(f"Only one of spacing{dim_str} or size{dim_str} must be specified")
            min, max = get_dimension(size, center)
            offset = min
            spacing = (max - min) / (count - 1)
        elif spacing is not None:
            if center:
                offset = -spacing * (count - 1) / 2
    else:
        spacing = 0
    return (spacing, offset)
