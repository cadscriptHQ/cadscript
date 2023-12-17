
from typing import Iterable, Iterator, Tuple

from .typedefs import CenterDefinitionType, DimensionDefinitionType


def get_center_flags(center: CenterDefinitionType) -> Tuple[bool, bool, bool]:
    if isinstance(center, str):
        c = center.upper()
        return ('X' in c , 'Y' in c, 'Z' in c)
    else:
        c = (center==True)
        return (c,c,c)

def __handle_size(arg: Tuple[DimensionDefinitionType, bool]) -> Tuple[float, float]:
    size, do_center = arg
    dim1,dim2 = (0,0)
    if isinstance(size, tuple):
        (dim1,dim2) = size
        if dim1 > dim2:
            dim1,dim2 = dim2,dim1
    else:
        dim2 = size
        if do_center: 
            half = (dim2-dim1)/2
            dim1 = -half
            dim2 = half
    return (dim1, dim2)

def get_dimensions(dimensions: Iterable[DimensionDefinitionType], center: CenterDefinitionType) -> Iterator[Tuple[float, float]]:
    """
    Calculate 2D or 3D dimensions based on the given size and center flags.

    Args:
        dimensions (tuple): A tuple of size values or tuple of tuples representing min/max.
        center (bool or string): indicating whether to center the dimensions, either a bool or a string ('X', 'Y', 'Z', 'XY', 'XZ', 'YZ', 'XYZ')

    Returns:
        tuple: A tuple of tuples with min/max values.

    """    
    return map(__handle_size, zip(dimensions, get_center_flags(center)))

def get_dimension(dimension: DimensionDefinitionType, center: bool) -> Tuple[float, float]:
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

