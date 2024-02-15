# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

from typing import Iterable, Iterator, List, Tuple, Optional, Union

from .interval import Interval1D, Interval2D, Interval3D
from .typedefs import CenterDefinitionType, DimensionDefinitionType, Vector2DType


def get_center_flags(center: CenterDefinitionType) -> Tuple[bool, bool, bool]:
    if isinstance(center, str):
        c = center.upper()
        return ('X' in c, 'Y' in c, 'Z' in c)
    else:
        c = (center is True)
        return (c, c, c)


def __handle_size(arg: Tuple[DimensionDefinitionType, bool]) -> Interval1D:
    size, do_center = arg
    dim1, dim2 = (0, 0)
    if isinstance(size, Interval1D):
        return size
    if isinstance(size, tuple):
        (dim1, dim2) = size
        if dim1 > dim2:
            dim1, dim2 = dim2, dim1
    else:
        dim2 = size
        if do_center:
            half = (dim2 - dim1) / 2
            dim1 = -half
            dim2 = half
    return Interval1D(dim1, dim2)


def __get_dimensions(dimensions: Iterable[DimensionDefinitionType], center: CenterDefinitionType) -> Iterator[Interval1D]:
    return map(__handle_size, zip(dimensions, get_center_flags(center)))


def get_dimension(dimension: DimensionDefinitionType, center: bool) -> Interval1D:
    """
    Calculate dimension based on the given size and center flags.

    Args:
        dimension (float or tuple): size value or tuple representing min/max.
        center (bool): indicating whether to center the dimensions

    Returns:
        interval: An Interval1D object.

    """
    t = (dimension, center)
    return __handle_size(t)


def get_dimensions_2d(dimensions: Iterable[DimensionDefinitionType], center: CenterDefinitionType) -> Interval2D:
    """
    Calculate 2D dimensions based on the given size and center flags.

    Args:
        dimensions (tuple): A tuple of size values or tuple of tuples representing min/max.
        center (bool or string): indicating whether to center the dimensions,
            either a bool or a string ('X', 'Y', 'XY')

    Returns:
        interval: An Interval2D object.

    """
    dim1, dim2 = __get_dimensions(dimensions, center)
    return Interval2D.from_tuples(dim1.tuple(), dim2.tuple())


def get_dimensions_3d(dimensions: Iterable[DimensionDefinitionType], center: CenterDefinitionType) -> Interval3D:
    """
    Calculate 3D dimensions based on the given size and center flags.

    Args:
        dimensions (tuple): A tuple of size values or tuple of tuples representing min/max.
        center (bool or string): indicating whether to center the dimensions,
            either a bool or a string ('X', 'Y', 'XY')

    Returns:
        interval: An Interval2D object.

    """
    dim1, dim2, dim3 = __get_dimensions(dimensions, center)
    return Interval3D.from_tuples(dim1.tuple(), dim2.tuple(), dim3.tuple())


def get_radius(r: Optional[float],
               radius: Optional[float],
               d: Optional[float],
               diameter: Optional[float],
               raise_err_if_none: bool = True
               ) -> float:
    '''
    Helper function to get the radius from the given parameters.
    '''
    # check only one parameter is specified
    if sum(x is not None for x in [r, radius, d, diameter]) > 1:
        raise ValueError("only one of r, radius, d, diameter can be specified")
    if r is not None:
        return r
    elif radius is not None:
        return radius
    elif d is not None:
        return d / 2
    elif diameter is not None:
        return diameter / 2
    if raise_err_if_none:
        raise ValueError("no radius/diameter specified")
    return 0


def get_height(h: Optional[float] = None,
               height: Optional[float] = None
               ) -> float:
    '''
    Helper function to get the height from the given parameters.
    '''
    # check only one parameter is specified
    if sum(x is not None for x in [h, height]) > 1:
        raise ValueError("only one of h and height can be specified")
    if h is not None:
        return h
    if height is not None:
        return height
    raise ValueError("no height specified")


def get_positions(positions: Optional[Union[Vector2DType, Iterable[Vector2DType]]],
                  pos: Optional[Union[Vector2DType, Iterable[Vector2DType]]],
                  default: Optional[List[Vector2DType]] = None
                  ) -> Optional[List[Vector2DType]]:
    if positions is not None and pos is not None:
        raise ValueError("only one of positions and pos can be specified")
    if positions is None and pos is None:
        return default
    p = positions if positions is not None else pos
    pos_list = [p] if isinstance(p, tuple) else p
    return pos_list
