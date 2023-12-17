import cadquery as cq
from typing import Optional, Literal, Any, Optional, Union, Tuple
from itertools import product
import re
from sys import modules

from .typedefs import *

from .cadobject import CadObject
from .sketchobject import SketchObject
from .assembly import Assembly

from .helpers import *

# this is a pointer to the module object instance itself.
this = modules[__name__]
this.debugtxt = ""




def make_box(sizex: DimensionDefinitionType, sizey: DimensionDefinitionType, sizez: DimensionDefinitionType, center: CenterDefinitionType=True) -> Any:
    dimx,dimy,dimz = get_dimensions([sizex, sizey, sizez], center)
    return __make_box_min_max(dimx[0],dimx[1],dimy[0],dimy[1],dimz[0],dimz[1])

def __make_box_min_max(x1: float, x2: float, y1: float, y2: float, z1: float, z2: float) -> Any:
    solid = cq.Solid.makeBox(x2-x1, y2-y1, z2-z1).move(cq.Location(cq.Vector(x1,y1,z1)))
    wp = cq.Workplane(obj = solid)
    return CadObject(wp)


def make_extrude(sketch, amount, workplane=None):
    if workplane is None:
        wp = cq.Workplane()
    elif isinstance(workplane, str):
        wp = cq.Workplane(workplane)
    else:
        wp = workplane
    onj = wp.placeSketch(sketch.cq()).extrude(amount, False)
    return CadObject(onj)

def make_text(
    text: str,
    size: float,
    height: float,
    font: str = "Arial",
):
    c = cq.Compound.makeText(text, size, height, font=font)
    wp = cq.Workplane(obj = c)
    return CadObject(wp)

def make_workplane(planeStr, offset=None):
    wp = cq.Workplane(planeStr)
    if not offset is None:
        wp = wp.workplane(offset=offset)
    return wp


def make_sketch():
    sketch = cq.Sketch()
    return SketchObject(sketch)

def import_step(path):
    wp = cq.importers.importStep(path)
    return CadObject(wp)

def pattern_rect(sizex, sizey, center=True):
    dimx,dimy = get_dimensions([sizex, sizey], center)
    return [(dimx[0],dimy[0]),(dimx[0],dimy[1]),(dimx[1],dimy[1]),(dimx[1],dimy[0])]

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
    Generate a 2D grid of points with a given spacing.

    Args:
        xs (float): The spacing between points along the x-axis.
        ys (float): The spacing between points along the y-axis.
        nx (int): The number of points along the x-axis.
        ny (int): The number of points along the y-axis.

    Returns:
        list: A list of tuples representing the coordinates of the points in the grid.
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









