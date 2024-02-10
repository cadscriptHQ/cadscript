# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

from typing import Iterable, Optional, Tuple, Union
import cadquery as cq

from .helpers import get_center_flags, get_positions, get_radius

from .typedefs import CenterDefinitionType, Vector2DType, Vector3DType, AxisType
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

    def cut_hole(self,
                 faceStr: str,
                 *,
                 r: Optional[float] = None,
                 radius: Optional[float] = None,
                 d: Optional[float] = None,
                 diameter: Optional[float] = None,
                 depth: Optional[float] = None,
                 positions: Optional[Union[Vector2DType, Iterable[Vector2DType]]] = None,
                 pos: Optional[Union[Vector2DType, Iterable[Vector2DType]]] = None,
                 countersink_angle: Optional[float] = None,
                 counterbore_depth: Optional[float] = None,
                 r2: Optional[float] = None,
                 radius2: Optional[float] = None,
                 d2: Optional[float] = None,
                 diameter2: Optional[float] = None,
                 ) -> 'Body':
        """
        Cuts a hole into the body. It can be a regular hole, a countersink hole or a counterbore hole.
        For all types of holes, you can specify the diameter of the hole using one of the `r`, `radius`, `d` or `diameter` parameters.
        To create a countersink hole, specify the `countersink_angle` parameter and also give the diameter of the countersink 
        using one of the `r2`, `radius2`, `d2` or `diameter2` parameters.
        To create a counterbore hole, specify the `counterbore_depth` parameter. Specify the counterbore by giving 
        the diameter of the counterbore using one of the `r2`, `radius2`, `d2` or `diameter2` parameters and the depth 
        of the counterbore using the `counterbore_depth` parameter.

        Args:
            faceStr (str): The face to cut the hole into.
            r (Optional[float]): The radius of the hole.
            radius (Optional[float]): The radius of the hole (alternative to 'r').
            d (Optional[float]): The diameter of the hole.
            diameter (Optional[float]): The diameter of the hole (alternative to 'd').
            depth (Optional[float]): The depth of the hole. If not specified, the hole will go through the entire body.
            positions (Optional[Union[Vector2DType, Iterable[Vector2DType]]]): If given, a hole is cut for each of the entries,
                specifying the center as (x,y) tuple.  If None, a single hole will be cut at the origin.
            pos (Optional[Union[Vector2DType, Iterable[Vector2DType]]]): Shorthand for positions parameter, only use one of them.
            countersink_angle (Optional[float]): The angle of the countersink. A typical value is 90 or 82 degrees.
            counterbore_depth (Optional[float]): The depth of the counterbore.
            r2 (Optional[float]): The radius of the countersink or counterbore.
            radius2 (Optional[float]): The radius of the countersink or counterbore (alternative to 'r2').
            d2 (Optional[float]): The diameter of the countersink or counterbore.
            diameter2 (Optional[float]): The diameter of the countersink or counterbore (alternative to 'd2').
        """
        r = get_radius(r, radius, d, diameter)
        r2 = get_radius(r2, radius2, d2, diameter2, False)
        pos_list = get_positions(positions, pos, default=[(0, 0)])

        if pos_list is None:
            raise Exception("pos_list not set, should not happen")

        wp: cq.Workplane = self.__wp.faces(faceStr).workplane(origin=(0, 0, 0)).pushPoints(pos_list)

        if countersink_angle is not None:
            # countersink hole
            if counterbore_depth is not None:
                raise ValueError("counterbore_depth must not be specified if countersink_angle is specified")
            if r2 == 0:
                raise ValueError("r2 must be specified if countersink_angle is specified")
            wp = wp.cskHole(diameter=r * 2, cskDiameter=r2 * 2, cskAngle=countersink_angle, depth=depth)
        elif counterbore_depth is not None:
            # counterbore hole
            if r2 == 0:
                raise ValueError("r2 must be specified if counterbore_depth is specified")
            wp = wp.cboreHole(diameter=r * 2, cboreDiameter=r2 * 2, cboreDepth=counterbore_depth, depth=depth)
        else:
            # regular hole
            wp = wp.hole(diameter=r * 2, depth=depth)
        self.__wp = wp
        return self



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

    def center(self, center: CenterDefinitionType = True) -> 'Body':
        """
        Centers the body at the origin.

        Args:
            center (CenterDefinitionType, optional): Whether to center the object. If False, the object will be not moved
                Can also be "X", "Y" or "Z" to center in only one direction or "XY", "XZ", "YZ" to center in two directions.
                The other directions will be unchanged.
                Defaults to True which centers the box in all directions.
        """
        dim = self.get_extent()
        center_flags = get_center_flags(center)

        def get_translate_value(entry) -> float:
            (dim_min, dim_max), centered = entry
            return -(dim_max - dim_min) / 2 if centered else 0

        move_vector = tuple(map(get_translate_value, zip(dim, center_flags)))
        return self.move(move_vector)


    def move_to_origin(self, axis: CenterDefinitionType = True) -> 'Body':
        """
        Moves the body to the origin, i.e. that the lower corner of the bounding box is at the origin.

        Args:
            axis (CenterDefinitionType, optional): 
                Can be "X", "Y" or "Z" to move the object in only one direction or "XY", "XZ", "YZ" to move
                it in two directions. The other directions will be unchanged.
                Defaults to True which moves the box in all directions.
                If False, the object will be not moved at all.
        """
        dim = self.get_extent()
        axis_flags = get_center_flags(axis)

        def get_translate_value(entry) -> float:
            (dim_min, _), _axis = entry
            return -dim_min if _axis else 0

        move_vector = tuple(map(get_translate_value, zip(dim, axis_flags)))
        return self.move(move_vector)



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
