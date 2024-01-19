# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

from typing import Iterable, Iterator, Tuple, Optional

from .typedefs import CenterDefinitionType, DimensionDefinitionType, Vector2DType


def get_center_flags(center: CenterDefinitionType) -> Tuple[bool, bool, bool]:
    if isinstance(center, str):
        c = center.upper()
        return ('X' in c, 'Y' in c, 'Z' in c)
    else:
        c = (center is True)
        return (c, c, c)


def __handle_size(arg: Tuple[DimensionDefinitionType, bool]) -> Vector2DType:
    size, do_center = arg
    dim1, dim2 = (0, 0)
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
    return (dim1, dim2)


def get_dimensions(dimensions: Iterable[DimensionDefinitionType], center: CenterDefinitionType) -> Iterator[Vector2DType]:
    """
    Calculate 2D or 3D dimensions based on the given size and center flags.

    Args:
        dimensions (tuple): A tuple of size values or tuple of tuples representing min/max.
        center (bool or string): indicating whether to center the dimensions,
            either a bool or a string ('X', 'Y', 'Z', 'XY', 'XZ', 'YZ', 'XYZ')

    Returns:
        tuple: A tuple of tuples with min/max values.

    """
    return map(__handle_size, zip(dimensions, get_center_flags(center)))


def get_dimension(dimension: DimensionDefinitionType, center: bool) -> Vector2DType:
    """
    Calculate 2D or 3D dimensions based on the given size and center flags.

    Args:
        dimension (float or tuple): size value or tuple representing min/max.
        center (bool): indicating whether to center the dimensions

    Returns:
        tuple: A tuple with min/max values.

    """
    t = (dimension, center)
    return __handle_size(t)


def get_radius(r: Optional[float] = None,
               radius: Optional[float] = None,
               d: Optional[float] = None,
               diameter: Optional[float] = None
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
    else:
        raise ValueError("no radius/diameter specified")

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