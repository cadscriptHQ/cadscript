# Copyright (C) 2023 Andreas Kahler
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
    dimx,dimy,dimz = get_dimensions([sizex, sizey, sizez], center)
    return __make_box_min_max(dimx[0],dimx[1],dimy[0],dimy[1],dimz[0],dimz[1])

def __make_box_min_max(x1: float, x2: float, y1: float, y2: float, z1: float, z2: float) -> 'Body':
    solid = cq.Solid.makeBox(x2-x1, y2-y1, z2-z1).move(cq.Location(cq.Vector(x1,y1,z1)))
    wp = cq.Workplane(obj = solid)
    return Body(wp)

def make_extrude(sketch: Sketch, amount: float, plane: Optional[Union[ConstructionPlane,str]]=None):
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
    c = cq.Compound.makeText(text, size, height, font=font)
    wp = cq.Workplane(obj = c)
    return Body(wp)

def make_construction_plane(planeStr: str, offset:Optional[float]=None):
    wp = cq.Workplane(planeStr)
    if not offset is None:
        wp = wp.workplane(offset=offset)
    return ConstructionPlane(wp)

def make_sketch():
    sketch = cq.Sketch()
    return Sketch(sketch)

def import_step(path):
    wp = cq.importers.importStep(path)
    return Body(wp)

'''
If inside CQ-Editor, use the show_object function to show the object.
Otherwise, do nothing
'''
def show(item: Union[Body,Sketch,ConstructionPlane,Assembly]):
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
    

    





