# Copyright (C) 2023 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

import string
import cadquery as cq
from typing import Any
from sys import modules

from .typedefs import *

from .body import Body
from .sketch import Sketch
from .construction_plane import ConstructionPlane
from .assembly import Assembly

from .helpers import *
from .patterns import *

# this is a pointer to the module object instance itself
this = modules[__name__]
this.debugtxt = ""


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










