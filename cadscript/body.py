# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

from typing import Tuple
import cadquery as cq

from .typedefs import DimensionDefinitionType, CenterDefinitionType, Vector2DType, Vector3DType, AxisType
from .sketch import Sketch


class Body:
    """
    Represents a 3D CAD object. They are typically created using make_* functions, e.g. 
    :func:`cadscript.make_box` or :func:`cadscript.make_extrude`. 
    """
    __wp: cq.Workplane

    def __init__(self, workplane: cq.Workplane):
        self.__wp = workplane

    def fillet(self, edgesStr: str, amount: float) -> 'Body':
        """
        Fillets the specified edges of the body.

        Args:
            edgesStr (str): The edges to fillet.
            amount (float): The radius of the fillet.

        Returns:
            Body: The modified body object.
        """
        result = self.__wp.edges(edgesStr).fillet(amount)
        self.__wp = result
        return self

    def chamfer(self, edgesStr: str, amount: float) -> 'Body':
        """
        Chamfers the specified edges of the body.

        Args:
            edgesStr (str): The edges to chamfer.
            amount (float): The distance of the chamfer.

        Returns:
            Body: The modified body object.
        """
        result = self.__wp.edges(edgesStr).chamfer(amount)
        self.__wp = result
        return self

    def move(self, translationVector: Vector3DType) -> 'Body':
        """
        Moves the body by the specified translation vector.

        Args:
            translationVector (Vector3DType): The translation vector.

        Returns:
            Body: The modified body object.
        """
        loc = cq.Location(cq.Vector(translationVector))
        c = self.__wp.findSolid()
        c.move(loc)
        wp = cq.Workplane(obj=c)
        self.__wp = wp
        return self

    def rotate(self, axis: AxisType, degrees: float) -> 'Body':
        """
        Rotates the body around the specified axis by the specified angle in degrees.

        Args:
            axis (AxisType): The axis to rotate around. Can be one of "X", "Y" or "Z".
            degrees (float): The angle in degrees.

        Returns:
            Body: The modified body object.
        """
        c = self.__wp.findSolid()
        if axis == "X":
            c = c.rotate((0, 0, 0), (1, 0, 0), degrees)
        elif axis == "Y":
            c = c.rotate((0, 0, 0), (0, 1, 0), degrees)
        elif axis == "Z":
            c = c.rotate((0, 0, 0), (0, 0, 1), degrees)
        else:
            raise ValueError("axis unknown")
        wp = cq.Workplane(obj=c)
        self.__wp = wp
        return self

    def cut(self, tool_body: 'Body') -> 'Body':
        """
        Performs a boolean cut operation with another body.

        Args:
            tool_body (Body): The body to cut from this body.
        """
        c1 = self.__wp.findSolid()
        c2 = tool_body.__wp.findSolid()
        c = c1.cut(c2)
        wp = cq.Workplane(obj=c)
        self.__wp = wp
        return self

    def add(self, tool_body: 'Body') -> 'Body':
        """
        Performs a boolean add operation with another body.

        Args:
            tool_body (Body): The body to add to this body.

        Returns:
            Body: The modified body object.
        """
        c1 = self.__wp.findSolid()
        c2 = tool_body.__wp.findSolid()
        c = c1.fuse(c2)
        wp = cq.Workplane(obj=c)
        self.__wp = wp
        return self

    def intersect(self, tool_body: 'Body') -> 'Body':
        """
        Performs a boolean intersect operation with another body.

        Args:
            tool_body (Body): The body to intersect with this body.

        Returns:
            Body: The modified body object.
        """
        c1 = self.__wp.findSolid()
        c2 = tool_body.__wp.findSolid()
        c = c1.intersect(c2)
        wp = cq.Workplane(obj=c)
        self.__wp = wp
        return self

    def add_extrude(self, faceStr: str, sketch: 'Sketch', amount: float) -> 'Body':
        """
        Adds an extrusion to the specified face of the body using a sketch.

        Args:
            faceStr (str): The face to extrude.
            sketch (Sketch): The sketch to extrude.
            amount (float): The amount of extrusion.

        Returns:
            Body: The modified body object.
        """
        result = self.__wp.faces(faceStr).workplane(origin=(0, 0, 0)).placeSketch(sketch.cq()).extrude(amount, "a")
        self.__wp = result
        return self

    def cut_extrude(self, faceStr: str, sketch: 'Sketch', amount: float) -> 'Body':
        """
        Adds a cut extrusion to the specified face of the body using a sketch.

        Args:
            faceStr (str): The face to extrude.
            sketch (Sketch): The sketch to extrude.
            amount (float): The amount of extrusion. For cutting you usually want to use a negative value to cut into the body.

        Returns:
            Body: The modified body object.
        """
        result = self.__wp.faces(faceStr).workplane(origin=(0, 0, 0)).placeSketch(sketch.cq()).extrude(amount, "s")
        self.__wp = result
        return self

    def make_extrude(self, faceStr: str, sketch: 'Sketch', amount: float) -> 'Body':
        """
        Creates a new body by extruding the specified face of the body using a sketch.

        Args:
            faceStr (str): The face to extrude.
            sketch (Sketch): The sketch to extrude.
            amount (float): The amount of extrusion.

        Returns:
            Body: The newly created body object.

        Note:
            This function is different from :meth:`add_extrude` in that it creates a new body instead of modifying the existing one.
        """
        result = self.__wp.faces(faceStr).workplane(origin=(0, 0, 0)).placeSketch(sketch.cq()).extrude(amount, False)
        c = result.findSolid().copy()
        wp = cq.Workplane(obj=c)
        return Body(wp)

    def get_center(self) -> Vector3DType:
        """
        Returns the center of the bounding box of the body.

        Returns:
            Vector3DType: The center of the bounding box.
        """
        bb = self.__wp.findSolid().BoundingBox()
        return ((bb.xmin + bb.xmax) / 2, (bb.ymin + bb.ymax) / 2, (bb.zmin + bb.zmax) / 2)

    def get_extent(self) -> Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]]:
        """
        Returns the extent of the bounding box of the body.

        Returns:
            Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]]: The extent of the bounding box.
        """
        bb = self.__wp.findSolid().BoundingBox()
        return ((bb.xmin, bb.xmax), (bb.ymin, bb.ymax), (bb.zmin, bb.zmax))

    def export_step(self, filename: str) -> None:
        """
        Exports the body to a STEP file.

        Args:   
            filename (str): The filename to export to.
        """
        self.__wp.findSolid().exportStep(filename)

    def export_stl(self, filename: str) -> None:
        """
        Exports the body to an STL file.

        Args:
            filename (str): The filename to export to.
        """
        self.__wp.findSolid().exportStl(filename)

    def render_svg(self, filename: str) -> None:
        """
        Renders the body as an SVG illustration.   

        Args:
            filename (str): The filename to export to.     
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

    def copy(self) -> 'Body':
        """
        Creates a copy of the body.

        Returns:
            Body: The newly created body object.
        """
        c = self.__wp.findSolid().copy()
        wp = cq.Workplane(obj=c)
        return Body(wp)

    def cq(self) -> cq.Workplane:
        """
        Returns the underlying CadQuery workplane object. Useful when mixing CadQuery and Cadscript code.

        Returns:
            cq.Workplane: The underlying CadQuery workplane object.
        """
        return self.__wp
