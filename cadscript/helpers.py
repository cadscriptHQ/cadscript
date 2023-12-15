import re
from typing import Iterable, Iterator, List, Tuple, Union

from .typedefs import CenterDefinitionType, DimensionDefinitionType


def __get_center_flags(center: Union[str, bool]) -> Tuple[bool, bool, bool]:
    if isinstance(center, str):
        center = center.upper()
        if center=="" or not re.match(r'^X?Y?Z?$', center):
            raise ValueError("invalid center string")
        return ('X' in center , 'Y' in center, 'Z' in center)
    else:
        center = (center==True)
        return (center,center,center)

def get_dimensions(dimensions: Iterable[DimensionDefinitionType], center: CenterDefinitionType) -> Iterator[Tuple[float, float]]:
    """
    Calculate 2D or 3D dimensions based on the given size and center flags.

    Args:
        dimensions (tuple): A tuple of size values or tuple of tuples representing min/max.
        center (bool): A flag indicating whether to center the dimensions.

    Returns:
        tuple: A tuple of tuples with min/max values.

    """

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
    
    return map(__handle_size, zip(dimensions, __get_center_flags(center)))

