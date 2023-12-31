# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

import cadquery as cq
from typing import Any
from sys import modules
import inspect

from .typedefs import *

from .body import Body
from .sketch import Sketch
from .construction_plane import ConstructionPlane
from .assembly import Assembly

from .helpers import *
from .patterns import *


def make_box(sizex: DimensionDefinitionType, sizey: DimensionDefinitionType, sizez: DimensionDefinitionType, center: CenterDefinitionType=True) -> 'Body':
    """
    Create a box-shaped body with the given dimensions.

    Args:
        sizex (DimensionDefinitionType): The size of the box along the x-axis.
        sizey (DimensionDefinitionType): The size of the box along the y-axis.
        sizez (DimensionDefinitionType): The size of the box along the z-axis.
        center (CenterDefinitionType, optional): Whether to center the box at the origin. If False, the box will start from the origin.
            Can also be "X", "Y" or "Z" to center in only one direction or "XY", "XZ", "YZ" to center in two directions.
            Defaults to True which centers the box in all directions.

    Returns:
        Body: The created box-shaped body.
    """
    dimx,dimy,dimz = get_dimensions([sizex, sizey, sizez], center)
    return __make_box_min_max(dimx[0],dimx[1],dimy[0],dimy[1],dimz[0],dimz[1])

def __make_box_min_max(x1: float, x2: float, y1: float, y2: float, z1: float, z2: float) -> 'Body':
    solid = cq.Solid.makeBox(x2-x1, y2-y1, z2-z1).move(cq.Location(cq.Vector(x1,y1,z1)))
    wp = cq.Workplane(obj = solid)
    return Body(wp)

def make_extrude(sketch: Sketch, amount: float, plane: Optional[Union[ConstructionPlane,str]]=None):
    """
    Create an extrusion from a sketch.

    Args:
        sketch (Sketch): The sketch to extrude.
        amount (float): The amount of extrusion.
        plane (Optional[Union[ConstructionPlane,str]], optional): The plane to extrude on. Defaults to the XY plane.
            Can be one of the strings "XY", "YZ", "XZ", "front", "back", "top", "bottom", "left" or "right"

    Returns:
        Body: The extruded body.
    """
    if plane is None:
        wp = cq.Workplane()
    elif isinstance(plane, str):
        wp = cq.Workplane(plane)
    else:
        wp = plane.cq
    onj = wp.placeSketch(sketch.cq()).extrude(amount, False)
    return Body(onj)

def make_text(
    text: str,
    size: float,
    height: float,
    font: str = "Arial",
):
    """
    Create a 3D text object.

    Args:
        text (str): The text to be created.
        size (float): The size of the text.
        height (float): The height of the text.
        font (str, optional): The font of the text. Defaults to "Arial".

    Returns:
        Body: The 3D text object.
    """
    c = cq.Compound.makeText(text, size, height, font=font)
    wp = cq.Workplane(obj = c)
    return Body(wp)

def make_construction_plane(planeStr: str, offset:Optional[float]=None):
    wp = cq.Workplane(planeStr)
    if not offset is None:
        wp = wp.workplane(offset=offset)
    return ConstructionPlane(wp)

def make_sketch():
    """
    Creates a new empty sketch object.

    Returns:
        Sketch: The newly created sketch object.
    """
    sketch = cq.Sketch()
    return Sketch(sketch)

def import_step(path):
    """
    Import a STEP file and return a Body object.

    Args:
        path (str): The path to the STEP file.

    Returns:
        Body: The imported body as a Body object.
    """
    wp = cq.importers.importStep(path)
    return Body(wp)

def show(item: Union[Body,Sketch,ConstructionPlane,Assembly]):
    '''
    If inside CQ-Editor, will display the item in the 3D view.
    Otherwise will do nothing.

    Args:
        item: the item to show. Can be a `Body` or a `Sketch`
    '''
    show_fn = __get_show_fn()
    if show_fn:
        show_fn(item.cq())
    else:
        # when cadquery.vis is available
        # show(item)
        pass

#examine the context of the caller. check if there is a function "show_object" available, return a reference to it
def __get_show_fn():
    # Start with the immediate caller's caller frame.
    frame = inspect.currentframe().f_back.f_back
    
    while frame:
        # Check global scope.
        if 'show_object' in frame.f_globals:
            potential_func = frame.f_globals['show_object']
            if callable(potential_func):
                return potential_func
        
        # Move up to the next caller in the stack.
        frame = frame.f_back

    # If function is not found in any ancestor's scope, return None.
    return None
    

    





