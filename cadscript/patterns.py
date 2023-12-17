from itertools import product
from typing import Optional, Tuple, Union

from .typedefs import *
from .helpers import *

def pattern_rect(sizex:float, sizey:float, center:CenterDefinitionType=True):
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
        spacing_x: Optional[float]=None, 
        spacing_y: Optional[float]=None, 
        size_x: Optional[DimensionDefinitionType]=None, 
        size_y: Optional[DimensionDefinitionType]=None, 
        center: CenterDefinitionType=True):
    """
    Generate a grid pattern of locations based on the given parameters.

    Args:
        count_x (int): The number of grid points in the x-direction. If 1 is passed, the result will be a 1D grid, i.e. points along the y-axis.
        count_y (int): The number of grid points in the y-direction. If 1 is passed, the result will be a 1D grid, i.e. points along the x-axis.
        spacing_x (float, optional): The spacing between grid points in the x-direction. If not specified, it will be calculated based on the size_x parameter.
        spacing_y (float, optional): The spacing between grid points in the y-direction. If not specified, it will be calculated based on the size_y parameter.
        size_x (DimensionDefinitionType, optional): The size of the grid in the x-direction. If not specified, it will be calculated based on the spacing_x parameter.
        size_y (DimensionDefinitionType, optional): The size of the grid in the y-direction. If not specified, it will be calculated based on the spacing_y parameter.
        center (CenterDefinitionType, optional): Determines whether the grid is centered. If True, the grid will be centered. 
            If False, the grid will start from the origin. Can also be "X" or "Y" to center in only one direction.
            Defaults to True. 

    Returns:
        List[Tuple[float, float]]: A list of (x, y) coordinates representing the locations of the grid points.
    """
    locs = []
    if count_x < 1 or count_y < 1:
        raise ValueError("count_x and count_y must be greater than 0")
    center_x, center_y, _ = get_center_flags(center)
    offset_x = 0
    offset_y = 0

    if count_x > 1:
        if spacing_x is None and size_x is None:
            raise ValueError("Either spacing_x or size_x must be specified")
        if size_x is not None:
            if spacing_x is not None:
                raise ValueError("Only one of spacing_x or size_x must be specified")
            (min_x,max_x) = get_dimension(size_x, center_x)
            offset_x = min_x
            spacing_x = (max_x-min_x)/(count_x-1)
        elif spacing_x is not None:
            if center_x: 
                offset_x = -spacing_x*(count_x-1)/2 
    else:
        spacing_x = 0
        
    if count_y > 1:
        if spacing_y is None and size_y is None:
            raise ValueError("Either spacing_y or size_y must be specified")
        if size_y is not None:
            if spacing_y is not None:
                raise ValueError("Only one of spacing_y or size_y must be specified")
            (min_y,max_y) = get_dimension(size_y, center_y)
            offset_y = min_y
            spacing_y = (max_y-min_y)/(count_y-1)
        elif spacing_y is not None:
            if center_y: 
                offset_y = -spacing_y*(count_y-1)/2 
    else:
        spacing_y = 0
        
    for i, j in product(range(count_x), range(count_y)):
        locs.append((i * spacing_x + offset_x, j * spacing_y + offset_y))
    return locs
