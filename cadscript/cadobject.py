# Copyright (C) 2023 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

import cadquery as cq

from .typedefs import DimensionDefinitionType, CenterDefinitionType, EdgeQueryType, Vector2DType, Vector3DType, AxisType, FaceQueryType
from .sketchobject import SketchObject


class CadObject:
    """
    Represents a 3D CAD object. They are typically created using make_* functions, e.g. 
    make_box or maker_extrude. 
    """
    __wp: cq.Workplane

    def __init__(self, workplane: cq.Workplane):
        self.__wp = workplane

    def cq(self) -> cq.Workplane:
        return self.__wp

    def fillet(self, edgesStr: EdgeQueryType, amount: float) -> 'CadObject':
        """
        Fillets the specified edges of the CAD object.
        """
        result = self.__wp.edges(edgesStr).fillet(amount)
        self.__wp = result
        return self

    def chamfer(self, edgesStr: EdgeQueryType, amount: float) -> 'CadObject':
        """
        Chamfers the specified edges of the CAD object.
        """
        result = self.__wp.edges(edgesStr).chamfer(amount)
        self.__wp = result
        return self

    def move(self, translationVector: Vector3DType) -> 'CadObject':
        """
        Moves the CAD object by the specified translation vector.
        """
        loc = cq.Location(cq.Vector(translationVector))
        c = self.__wp.findSolid()
        c.move(loc)
        wp = cq.Workplane(obj = c)
        self.__wp = wp
        return self

    def rotate(self, axis: AxisType, degrees: float) -> 'CadObject':
        """
        Rotates the CAD object around the specified axis by the specified angle in degrees.
        """
        c = self.__wp.findSolid()
        if axis == "X":
            c = c.rotate((0,0,0),(1,0,0), degrees)
        elif axis == "Y":
            c = c.rotate((0,0,0),(0,1,0), degrees)
        elif axis == "Z":
            c = c.rotate((0,0,0),(0,0,1), degrees)
        else:
            raise ValueError("axis unknown")
        wp = cq.Workplane(obj = c)
        self.__wp = wp
        return self

    def cut(self, cad2: 'CadObject') -> 'CadObject':
        """
        Performs a boolean cut operation with another CAD object.
        """
        c1 = self.__wp.findSolid()
        c2 = cad2.__wp.findSolid()
        c = c1.cut(c2)
        wp = cq.Workplane(obj = c)
        self.__wp = wp
        return self

    def fuse(self, cad2: 'CadObject') -> 'CadObject':
        """
        Performs a boolean fuse operation with another CAD object.
        """
        c1 = self.__wp.findSolid()
        c2 = cad2.__wp.findSolid()
        c = c1.fuse(c2)
        wp = cq.Workplane(obj = c)
        self.__wp = wp
        return self

    def add_extrude(self, faceStr : FaceQueryType, sketch: 'SketchObject', amount: float) -> 'CadObject':
        """
        Adds an extrusion to the specified face of the CAD object using a sketch.
        """
        result = self.__wp.faces(faceStr).workplane(origin=(0,0,0)).placeSketch(sketch.cq()).extrude(amount, "a")
        self.__wp = result
        return self

    def cut_extrude(self, faceStr : FaceQueryType, sketch: 'SketchObject', amount: float) -> 'CadObject':
        """
        Adds a cut extrusion to the specified face of the CAD object using a sketch.
        """
        result = self.__wp.faces(faceStr).workplane(origin=(0,0,0)).placeSketch(sketch.cq()).extrude(amount, "s")
        self.__wp = result
        return self

    def make_extrude(self, faceStr : FaceQueryType, sketch: 'SketchObject', amount: float) -> 'CadObject':
        """
        Creates a new CAD object by extruding the specified face of the CAD object using a sketch.
        """
        result = self.__wp.faces(faceStr).workplane(origin=(0,0,0)).placeSketch(sketch.cq()).extrude(amount, False)
        c = result.findSolid().copy()
        wp = cq.Workplane(obj = c)
        return CadObject(wp)

    def get_center(self) -> Vector3DType:
        """
        Returns the center of the bounding box of the CAD object.
        """
        c = self.__wp.findSolid()
        shapes = []
        for s in c:
            shapes.append(s)
        return cq.Shape.CombinedCenterOfBoundBox(shapes).toTuple()

    def copy(self) -> 'CadObject':
        """
        Creates a copy of the CAD object.
        """
        c = self.__wp.findSolid().copy()
        wp = cq.Workplane(obj = c)
        return CadObject(wp)    

    def export_step(self, filename: str) -> None:
        """
        Exports the CAD object to a STEP file.
        """
        self.__wp.findSolid().exportStep(filename)

    def export_stl(self, filename: str) -> None:
        """
        Exports the CAD object to an STL file.
        """
        self.__wp.findSolid().exportStl(filename)

    def render_svg(self, filename: str) -> None:
        """
        Renders the CAD object as an SVG illustration.        
        """
        c = self.__wp.findSolid()
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