# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

from itertools import product
from math import ceil, floor
from typing import Literal, Optional, List, Tuple

from .interval import Interval2D
from .typedefs import DimensionDefinitionType, CenterDefinitionType, Vector2DType
from .helpers import get_center_flags, get_dimension, get_dimensions_2d


def pattern_rect(sizex: DimensionDefinitionType,
                 sizey: DimensionDefinitionType,
                 center: CenterDefinitionType = True) -> List[Vector2DType]:
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
    dim = get_dimensions_2d([sizex, sizey], center)
    return [(dim.min_x, dim.min_y), (dim.min_x, dim.max_y), (dim.max_x, dim.max_y), (dim.max_x, dim.min_y)]


def pattern_distribute(
        size_x: DimensionDefinitionType,
        size_y: DimensionDefinitionType,
        tile_size_x: float,
        tile_size_y: float,
        *,
        count_x: Optional[int] = None,
        count_y: Optional[int] = None,
        center: CenterDefinitionType = True,
        result_pos: Literal["center", "origin"] = "center",
        min_spacing_x: float = 0.0,
        min_spacing_y: float = 0.0) -> List[Vector2DType]:
    """
    Generate a grid pattern that evenly distributes tiles of fixed size on a rectangle.

    Args:
        size_x (DimensionDefinitionType): The width of the rectangle.
        size_y (DimensionDefinitionType): The height of the rectangle.
        tile_size_x (float): The width of the tiles.
        tile_size_y (float): The height of the tiles.
        count_x (int, optional): The number of tiles in the x-direction.
            If not specified, the maximum number of tiles that fit will be used.
        count_y (int, optional): The number of tiles in the y-direction.
            If not specified, the maximum number of tiles that fit will be used.
        center (CenterDefinitionType, optional): Determines whether the rectangle is centered around the origin.
            If True, the rectangle will be centered. Can also be "X" or "Y" to center in only one direction.
            If False, the rectangle will start from the origin. Defaults to True.
        result_pos (Literal["center", "origin"], optional): Determines the position of the points in the resulting list.
            If "center", the points will be denote the center of the tiles.
            If "origin", the points will denote the bottom-left corner of the tiles. Defaults to "center".
        min_spacing_x (float, optional): The minimum spacing between tiles in the x-direction.
            Defaults to 0. Only used if count_x is not specified.
        min_spacing_y (float, optional): The minimum spacing between tiles in the y-direction.
            Defaults to 0. Only used if count_y is not specified.

    Returns:
        List[Vector2DType]: A list of (x, y) coordinates representing the locations of the tiles.

    Remarks:
        - If count_x or count_y is not specified, the maximum number of tiles that fit will be used.
        - if tile_size_x is greater than size_x or tile_size_y is greater than size_y, no tiles will be generated.
        - If count_x or count_y is 1, the result with be centered in the corresponding direction.

    """
    if tile_size_x <= 0 or tile_size_y <= 0:
        raise ValueError("tile_size must be greater than 0")
    center_x, center_y, _ = get_center_flags(center)
    use_center = result_pos == "center"
    locations_x = __distribute_tile(size_x, tile_size_x, count_x, center_x, use_center, min_spacing_x)
    locations_y = __distribute_tile(size_y, tile_size_y, count_y, center_y, use_center, min_spacing_y)

    return list(product(locations_x, locations_y))


def __distribute_tile(size: DimensionDefinitionType,
                      tile_size: float,
                      count: Optional[int],
                      center: bool,
                      use_center: bool,
                      min_spacing: float) -> List[float]:
    """
    Helper function for pattern_tile(). Distributes tiles in one direction.
    """
    dim = get_dimension(size, center)
    if count is None:
        count = floor((dim.size() + min_spacing) / (tile_size + min_spacing))
    if count < 1:
        # no tiles fit
        return []
    if count == 1:
        # only one tile fits, return the center
        tile_offset = 0 if use_center else -tile_size / 2
        return [dim.center() + tile_offset]
    # distribute
    delta = (dim.size() - tile_size) / (count - 1)
    tile_offset = tile_size / 2 if use_center else 0
    return [dim.min + i * delta + tile_offset for i in range(count)]


def pattern_distribute_stretch(size_x: DimensionDefinitionType,
                               size_y: DimensionDefinitionType,
                               *,
                               count_x: Optional[int] = None,
                               count_y: Optional[int] = None,
                               min_tile_size_x: Optional[int] = None,
                               max_tile_size_x: Optional[int] = None,
                               min_tile_size_y: Optional[int] = None,
                               max_tile_size_y: Optional[int] = None,
                               spacing_x: float = 0.0,
                               spacing_y: float = 0.0,
                               center: CenterDefinitionType = True
                               ) -> List[Interval2D]:
    """
    Generate a grid pattern that evenly distributes tiles of variable size on a rectangle.

    Args:
        size_x (DimensionDefinitionType): The width of the rectangle.
        size_y (DimensionDefinitionType): The height of the rectangle.
        count_x (int, optional): The number of tiles in the x-direction.
            If not specified, the values of min_tile_size_x and max_tile_size_x will be used
            to calculate the number of tiles that fit.
        count_y (int, optional): The number of tiles in the y-direction.
            If not specified, the values of min_tile_size_y and max_tile_size_y will be used
            to calculate the number of tiles that fit.
        min_tile_size_x (int, optional): The minimum size of the tiles in the x-direction.
        max_tile_size_x (int, optional): The maximum size of the tiles in the x-direction.
        min_tile_size_y (int, optional): The minimum size of the tiles in the y-direction.
        max_tile_size_y (int, optional): The maximum size of the tiles in the y-direction.
        spacing_x (float, optional): The spacing between tiles in the x-direction.
            Defaults to 0.
        spacing_y (float, optional): The spacing between tiles in the y-direction.
            Defaults to 0.
        center (CenterDefinitionType, optional): Determines whether the rectangle is centered around the origin.
            If True, the rectangle will be centered. Can also be "X" or "Y" to center in only one direction.
            If False, the rectangle will start from the origin. Defaults to True.

    Returns:
        List[Interval2D]: A list of Interval2D objects representing the tiles.

    Remarks:
        - If count_x or is not specified, the values of min_tile_size_x and max_tile_size_x
          will be used to calculate the number of tiles that fit.
        - If min_tile_size_x is given, the algorithm will use as many tiles as possible to fit the size.
          If min_tile_size_x is greater than the rectangle size, no tiles will be generated.
        - If max_tile_size_x is given, the algorithm will only use as few tiles as possible to fit the size.
        - If both min_tile_size_x and max_tile_size_x are given, the algorithm will use as few tiles as possible,
          but will return no tiles if the size is less than min_tile_size_x.
        - All the remarks for the x-direction also apply to the y-direction with the corresponding parameters.
    """
    center_x, center_y, _ = get_center_flags(center)
    if count_x is None and min_tile_size_x is None and max_tile_size_x is None:
        raise ValueError("Either count_x or min_tile_size_x and max_tile_size_x must be specified")

    count_x, tile_size_x = __get_ditribute_stretch_count(size_x, count_x, min_tile_size_x, max_tile_size_x, spacing_x, center_x)
    count_y, tile_size_y = __get_ditribute_stretch_count(size_y, count_y, min_tile_size_y, max_tile_size_y, spacing_y, center_y)
    if count_x == 0 or count_y == 0:
        return []
    pos_list = pattern_distribute(size_x, size_y, tile_size_x, tile_size_y, count_x=count_x,
                                  count_y=count_y, center=center, result_pos="origin")
    return [Interval2D(x, x + tile_size_x, y, y + tile_size_y) for x, y in pos_list]


def __get_ditribute_stretch_count(size, count, min_tile_size, max_tile_size, spacing, center):
    """
    Helper function for pattern_distribute_strech().
    Calculates the count and tile size based on the given parameters.
    """
    dim = get_dimension(size, center)
    extent = dim.size()
    calc_size = lambda _count: (spacing + extent) / _count - spacing
    if count is not None:
        return (count, calc_size(count))
    if min_tile_size is not None and extent < min_tile_size:
        # no tiles fit
        return (0, 0)
    elif max_tile_size is not None:
        # minimize the number of tiles
        _count = ceil((extent + spacing) / (max_tile_size + spacing))
        return (_count, calc_size(_count))
    elif min_tile_size is not None:
        # maximize the number of tiles
        _count = floor((extent + spacing) / (min_tile_size + spacing))
        return (_count, calc_size(_count))
    raise Exception("cadscript internal error - should not reach this point")




def pattern_grid(
        count_x: int,
        count_y: int,
        *,
        spacing_x: Optional[float] = None,
        spacing_y: Optional[float] = None,
        size_x: Optional[DimensionDefinitionType] = None,
        size_y: Optional[DimensionDefinitionType] = None,
        center: CenterDefinitionType = True) -> List[Vector2DType]:
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


def __get_spacing(count, spacing, size, center, dim_str) -> Tuple[float, float]:
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
            dim = get_dimension(size, center)
            offset = dim.min
            spacing = dim.size() / (count - 1)
        elif spacing is not None:
            if center:
                offset = -spacing * (count - 1) / 2
    else:
        spacing = 0
    return (spacing, offset)
