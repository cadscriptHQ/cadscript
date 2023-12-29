'''
Copyright (C) 2023 Andreas Kahler
This file is part of Cadscript
SPDX-License-Identifier: Apache-2.0
'''

import cadquery as cq

from .typedefs import DimensionDefinitionType, CenterDefinitionType, EdgeQueryType, Vector2DType, Vector3DType, AxisType, FaceQueryType
from .sketchobject import SketchObject


class CadObject:
    """
    Represents a 3D CAD object. They are typically created using make_* functions, e.g. 
    make_box or maker_extrude. 

    Methods:
      cq(): Returns the cadquery workplane object associated with the CAD object.
      fillet(edgesStr, amount): Fillets the specified edges of the CAD object.
      chamfer(edgesStr, amount): Chamfers the specified edges of the CAD object.
      move(translationVector): Moves the CAD object by the specified translation vector.
      rotate(axis, degrees): Rotates the CAD object around the specified axis by the specified angle in degrees.
      cut(cad2): Performs a boolean cut operation with another CAD object.
      fuse(cad2): Performs a boolean fuse operation with another CAD object.
      add_extrude(faceStr, sketch, amount): Adds an extrusion to the specified face of the CAD object using a sketch.
      cut_extrude(faceStr, sketch, amount): Adds a cut extrusion to the specified face of the CAD object using a sketch.
      make_extrude(faceStr, sketch, amount): Creates a new CAD object by extruding the specified face of the CAD object using a sketch.
      CenterOfBoundBox(): Returns the center of the bounding box of the CAD object.
      copy(): Creates a copy of the CAD object.
      export_step(filename): Exports the CAD object to a STEP file.
      export_stl(filename): Exports the CAD object to an STL file.
      render_svg(filename): Renders the CAD object as an SVG image.

    """
    def __init__(self, workplane):
        self.wp = workplane

    def cq(self) -> cq.Workplane:
        return self.wp

    def fillet(self, edgesStr: EdgeQueryType, amount: float) -> 'CadObject':
      result = self.wp.edges(edgesStr).fillet(amount)
      self.wp = result
      return self

    def chamfer(self, edgesStr: EdgeQueryType, amount: float) -> 'CadObject':
        result = self.wp.edges(edgesStr).chamfer(amount)
        self.wp = result
        return self

    def move(self, translationVector: Vector3DType) -> 'CadObject':
        loc = cq.Location(cq.Vector(translationVector))
        c = self.wp.findSolid()
        c.move(loc)
        wp = cq.Workplane(obj = c)
        self.wp = wp
        return self

    def rotate(self, axis: AxisType, degrees: float) -> 'CadObject':
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

    def cut(self, cad2: 'CadObject') -> 'CadObject':
        c1 = self.wp.findSolid()
        c2 = cad2.wp.findSolid()
        c = c1.cut(c2)
        wp = cq.Workplane(obj = c)
        self.wp = wp
        return self

    def fuse(self, cad2: 'CadObject') -> 'CadObject':
        c1 = self.wp.findSolid()
        c2 = cad2.wp.findSolid()
        c = c1.fuse(c2)
        wp = cq.Workplane(obj = c)
        self.wp = wp
        return self

    def add_extrude(self, faceStr : FaceQueryType, sketch: 'SketchObject', amount: float) -> 'CadObject':
        result = self.wp.faces(faceStr).workplane(origin=(0,0,0)).placeSketch(sketch.cq()).extrude(amount, "a")
        self.wp = result
        return self

    def cut_extrude(self, faceStr : FaceQueryType, sketch: 'SketchObject', amount: float) -> 'CadObject':
        result = self.wp.faces(faceStr).workplane(origin=(0,0,0)).placeSketch(sketch.cq()).extrude(amount, "s")
        self.wp = result
        return self

    def make_extrude(self, faceStr : FaceQueryType, sketch: 'SketchObject', amount: float) -> 'CadObject':
        result = self.wp.faces(faceStr).workplane(origin=(0,0,0)).placeSketch(sketch.cq()).extrude(amount, False)
        c = result.findSolid().copy()
        wp = cq.Workplane(obj = c)
        return CadObject(wp)

    def get_center(self) -> Vector3DType:
        c = self.wp.findSolid()
        shapes = []
        for s in c:
            shapes.append(s)
        return cq.Shape.CombinedCenterOfBoundBox(shapes).toTuple()

    def copy(self) -> 'CadObject':
        c = self.wp.findSolid().copy()
        wp = cq.Workplane(obj = c)
        return CadObject(wp)

    def export_step(self, filename: str) -> None:
        self.wp.findSolid().exportStep(filename)

    def export_stl(self, filename: str) -> None:
        self.wp.findSolid().exportStl(filename)

    def render_svg(self, filename: str) -> None:
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