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
from .patterns import *

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










