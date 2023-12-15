import cadquery as cq
from typing import Optional, Literal, Any, Optional, Union, Tuple
from itertools import product
import re
from sys import modules

from .typedefs import *





from .sketchobject import SketchObject
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

def pattern_rect_array(xs, ys, nx, ny):
    locs = []
    offsetx = (nx - 1) * xs * 0.5
    offsety = (ny - 1) * ys * 0.5
    for i, j in product(range(nx), range(ny)):
        locs.append((i * xs - offsetx, j * ys - offsety))
    return locs

def export_svg(part, filename, width=300, height=300, strokeWidth=0.6, projectionDir=(1, 1, 1)):
  cq.exporters.export(part,
                      filename,
                      opt={
                          "width": width,
                          "height": height,
                          "marginLeft": 5,
                          "marginTop": 5,
                          "showAxes": False,
                          "projectionDir": projectionDir,
                          "strokeWidth": strokeWidth,
                          "strokeColor": (0, 0, 0),
                          "hiddenColor": (0, 0, 255),
                          "showHidden": False,
                      },)




class CadObject:
    
    def __init__(self):
        self.wp = None

    def __init__(self, workplane):
        self.wp = workplane
        
    def cq(self):
        return self.wp
        
    def fillet(self, edgesStr, amount):
        result = self.wp.edges(edgesStr).fillet(amount)
        self.wp = result
        return self
    
    def chamfer(self, edgesStr, amount):
        result = self.wp.edges(edgesStr).chamfer(amount)
        self.wp = result
        return self
    
    def move(self, translationVector):
        loc = cq.Location(cq.Vector(translationVector))
        c = self.wp.findSolid()
        c.move(loc)
        wp = cq.Workplane(obj = c)
        self.wp = wp
        return self

    def rotate(self, axis, degrees):
        c = self.wp.findSolid()
        if axis == "X":
            c = c.rotate((0,0,0),(1,0,0), degrees)
        elif axis == "Y":
            c = c.rotate((0,0,0),(0,1,0), degrees)
        elif axis == "Z":
            c = c.rotate((0,0,0),(0,0,1), degrees)
        else:
            raise ValueError("axis unknown")
        wp = cq.Workplane(obj = c)
        self.wp = wp
        return self

    def cut(self, cad2):
        c1 = self.wp.findSolid()
        c2 = cad2.wp.findSolid()
        c = c1.cut(c2)
        wp = cq.Workplane(obj = c)
        self.wp = wp
        return self
    
    def fuse(self, cad2):
        c1 = self.wp.findSolid()
        c2 = cad2.wp.findSolid()
        c = c1.fuse(c2)
        wp = cq.Workplane(obj = c)
        self.wp = wp
        return self

    def addExtrude(self, faceStr, sketch, amount):
        result = self.wp.faces(faceStr).workplane(origin=(0,0,0)).placeSketch(sketch.cq()).extrude(amount, "a")
        self.wp = result
        return self

    def cutExtrude(self, faceStr, sketch, amount):
        result = self.wp.faces(faceStr).workplane(origin=(0,0,0)).placeSketch(sketch.cq()).extrude(amount, "s")
        self.wp = result
        return self

    def makeExtrude(self, faceStr, sketch, amount):
        result = self.wp.faces(faceStr).workplane(origin=(0,0,0)).placeSketch(sketch.cq()).extrude(amount, False)
        c = result.findSolid().copy()
        wp = cq.Workplane(obj = c)
        return CadObject(wp)        

    def CenterOfBoundBox(self):
        c = self.wp.findSolid()
        shapes = []
        for s in c:
            shapes.append(s)
        return cq.Shape.CombinedCenterOfBoundBox(shapes)

    def copy(self):
        c = self.wp.findSolid().copy()
        wp = cq.Workplane(obj = c)
        return CadObject(wp)
            
    def exportStep(self, filename):
        self.wp.findSolid().exportStep(filename)
        
    def exportStl(self, filename):
        self.wp.findSolid().exportStl(filename)

    def renderSvg(self, filename):
        c = self.wp.findSolid()
        cq.exporters.export(c,
                            filename,
                            opt={
                                "width": 300,
                                "height": 300,
                                "marginLeft": 10,
                                "marginTop": 10,
                                "showAxes": False,
                                "projectionDir": (1, 1, 1),
                                "strokeWidth": 0.8,
                                "strokeColor": (0, 0, 0),
                                "hiddenColor": (0, 0, 255),
                                "showHidden": False,
                            },)        

class Assembly:
    
    def __init__(self):
        self.assy = cq.Assembly()
        
    def cq(self):
        return self.assy

    def add(self, part: CadObject):
        self.assy.add(part.cq())
        return self.assy


class M3Helper:

    dia = 3
    diaHole = 3.2
    diaCoreHole = 2.5
    diaThreadInsert = 3.9

    r = dia/2
    rHole = diaHole/2
    rCoreHole = diaCoreHole/2
    rThreadInsert = diaThreadInsert/2

M3 = M3Helper()
