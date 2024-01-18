# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

import cadquery as cq

from typing import Iterable, List, Optional, Union, Tuple

from .typedefs import DimensionDefinitionType, CenterDefinitionType, Vector2DType
from .export import export_sketch_DXF
from .helpers import get_dimensions
from .cqselectors import NearestToPointListSelector


class Sketch:
    """
    Represents a 2D sketch. Sketch instances are typically created using :func:`cadscript.make_sketch`.
    """
    __sketch: cq.Sketch

    def __init__(self, sketch: cq.Sketch) -> None:
        self.__sketch = sketch

    def __perform_action(self,
                         action,
                         positions: Optional[Iterable[Vector2DType]]
                         ) -> 'Sketch':
        if positions:
            self.__sketch = action(self.__sketch.push(positions))
        else:
            self.__sketch = action(self.__sketch)
        self.__sketch.reset().clean()
        return self

    def __rect_helper(self,
                      sketch,
                      size_x: DimensionDefinitionType,
                      size_y: DimensionDefinitionType,
                      center: CenterDefinitionType,
                      mode="a"
                      ):
        (x1, x2), (y1, y2) = get_dimensions([size_x, size_y], center)
        p0 = cq.Vector(x1, y1)
        p1 = cq.Vector(x2, y1)
        p2 = cq.Vector(x2, y2)
        p3 = cq.Vector(x1, y2)
        return sketch.polygon([p0, p1, p2, p3, p0], mode=mode)

    def __get_positions(self,
                        positions: Optional[Union[Vector2DType, Iterable[Vector2DType]]],
                        pos: Optional[Union[Vector2DType, Iterable[Vector2DType]]],
                        default: Optional[List[Vector2DType]] = None
                        ) -> Optional[List[Vector2DType]]:
        if positions is not None and pos is not None:
            raise ValueError("only one of positions and pos can be specified")
        if positions is None and pos is None:
            return default
        p = positions if positions is not None else pos
        pos_list = [p] if isinstance(p, tuple) else p
        return pos_list

    def add_rect(self,
                 size_x: DimensionDefinitionType,
                 size_y: DimensionDefinitionType,
                 *,
                 center: CenterDefinitionType = True,
                 positions: Optional[Union[Vector2DType, Iterable[Vector2DType]]] = None,
                 pos: Optional[Union[Vector2DType, Iterable[Vector2DType]]] = None
                 ) -> 'Sketch':
        """
        Adds a rectangle to the sketch object.

        Args:
            size_x (DimensionDefinitionType): The size of the rectangle along the x-axis.
            size_y (DimensionDefinitionType): The size of the rectangle along the y-axis.
            center (CenterDefinitionType, optional): Determines whether the rectangle is centered.
                If False, the rectangle will start from the origin.
                Can also be "X" or "Y" to center in only one direction. Defaults to True.
            positions (Vector2DType | Iterable[Vector2DType], optional): If given, a rectangle is added for each of the entries,
                specifying the offset as (x,y) tuple.
                Defaults to None, which results in a single rectangle added with no offset.
            pos: Shorthand for positions parameter, only use one of them.

        Returns:
            Sketch: The updated sketch object.
        """
        action = lambda x: self.__rect_helper(x, size_x, size_y, center)
        return self.__perform_action(action, self.__get_positions(positions, pos))

    def cut_rect(self,
                 size_x: DimensionDefinitionType,
                 size_y: DimensionDefinitionType,
                 *,
                 center: CenterDefinitionType = True,
                 positions: Optional[Union[Vector2DType, Iterable[Vector2DType]]] = None,
                 pos: Optional[Union[Vector2DType, Iterable[Vector2DType]]] = None
                 ) -> 'Sketch':
        """
        Cuts a rectangle from the sketch object.

        Args:
            size_x (DimensionDefinitionType): The size of the rectangle along the x-axis.
            size_y (DimensionDefinitionType): The size of the rectangle along the y-axis.
            center (CenterDefinitionType, optional): Determines whether the rectangle is centered.
                If False, the rectangle will start from the origin.
                Can also be "X" or "Y" to center in only one direction. Defaults to True.
            positions (Vector2DType | Iterable[Vector2DType], optional): If given, a rectangle is cut for each of the entries,
                specifying the offset as (x,y) tuple.
                Defaults to None, which results in a single rectangle cut with no offset.
            pos: Shorthand for positions parameter, only use one of them.

        Returns:
            Sketch: The updated sketch object.
        """
        action = lambda x: self.__rect_helper(x, size_x, size_y, center, mode="s")
        return self.__perform_action(action, self.__get_positions(positions, pos))

    def __get_radius(self,
                     r: Optional[float] = None,
                     radius: Optional[float] = None,
                     d: Optional[float] = None,
                     diameter: Optional[float] = None
                     ) -> float:
        '''
        Helper function to get the radius from the given parameters.
        '''
        # check only one parameter is specified
        if sum(x is not None for x in [r, radius, d, diameter]) > 1:
            raise ValueError("only one of r, radius, d, diameter can be specified")
        if r is not None:
            return r
        elif radius is not None:
            return radius
        elif d is not None:
            return d / 2
        elif diameter is not None:
            return diameter / 2
        else:
            raise ValueError("no radius/diameter specified")

    def add_circle(self,
                   *,
                   r: Optional[float] = None,
                   radius: Optional[float] = None,
                   d: Optional[float] = None,
                   diameter: Optional[float] = None,
                   positions: Optional[Union[Vector2DType, Iterable[Vector2DType]]] = None,
                   pos: Optional[Union[Vector2DType, Iterable[Vector2DType]]] = None
                   ) -> 'Sketch':
        """
        Adds a circle to the sketch. One of the parameters 'r', 'radius', 'd' or 'diameter' must be specified.

        Parameters:
            r (float, optional): The radius of the circle.
            radius (float, optional): The radius of the circle (alternative to 'r').
            d (float, optional): The diameter of the circle.
            diameter (float, optional): The diameter of the circle (alternative to 'd').
            positions (Vector2DType | Iterable[Vector2DType], optional): If given, a circle is added for each of the entries,
                specifying the center as (x,y) tuple.  If None, a single circle will be added at the origin.
            pos: Shorthand for positions parameter, only use one of them.

        Returns:
            Sketch: The updated sketch object.
        """
        r = self.__get_radius(r, radius, d, diameter)
        action = lambda x: x.circle(r)
        return self.__perform_action(action, self.__get_positions(positions, pos))

    def cut_circle(self,
                   *,
                   r: Optional[float] = None,
                   radius: Optional[float] = None,
                   d: Optional[float] = None,
                   diameter: Optional[float] = None,
                   positions: Optional[Union[Vector2DType, Iterable[Vector2DType]]] = None,
                   pos: Optional[Union[Vector2DType, Iterable[Vector2DType]]] = None
                   ) -> 'Sketch':
        """
        Cuts a circle from the sketch. One of the parameters 'r', 'radius', 'd' or 'diameter' must be specified.

        Parameters:
            r (float, optional): The radius of the circle.
            radius (float, optional): The radius of the circle (alternative to 'r').
            d (float, optional): The diameter of the circle.
            diameter (float, optional): The diameter of the circle (alternative to 'd').
            positions (Vector2DType | Iterable[Vector2DType], optional): If given, a circle is cut for each of the entries,
                specifying the center as (x,y) tuple.  If None, a single circle will be cut at the origin.
            pos: Shorthand for positions parameter, only use one of them.

        Returns:
            Sketch: The updated sketch object.
        """
        r = self.__get_radius(r, radius, d, diameter)
        action = lambda x: x.circle(r, mode="s")
        return self.__perform_action(action, self.__get_positions(positions, pos))

    def add_ellipse(self,
                    size_x: DimensionDefinitionType,
                    size_y: DimensionDefinitionType,
                    *,
                    angle: float = 0,
                    center: CenterDefinitionType = True,
                    positions: Optional[Union[Vector2DType, Iterable[Vector2DType]]] = None,
                    pos: Optional[Union[Vector2DType, Iterable[Vector2DType]]] = None
                    ) -> 'Sketch':
        """
        Adds an ellipse to the sketch object.

        Args:
            size_x (DimensionDefinitionType): The size of the ellipse along the x-axis.
            size_y (DimensionDefinitionType): The size of the ellipse along the y-axis.
            angle (float, optional): The angle of rotation. Defaults to 0.
            center (CenterDefinitionType, optional): Determines whether the ellipse is centered.
                If False, the ellipse will start from the origin.
                Can also be "X" or "Y" to center in only one direction. Defaults to True.
            positions (Vector2DType | Iterable[Vector2DType], optional): If given, a ellipse is added for each of the entries,
                specifying the offset as (x,y) tuple.
                Defaults to None, which results in a single ellipse added with no offset.
            pos: Shorthand for positions parameter, only use one of them.

        Returns:
            Sketch: The updated sketch object.
        """
        return self.__ellipse(size_x, size_y, "a", angle, center, positions, pos)

    def cut_ellipse(self,
                    size_x: DimensionDefinitionType,
                    size_y: DimensionDefinitionType,
                    *,
                    angle: float = 0,
                    center: CenterDefinitionType = True,
                    positions: Optional[Union[Vector2DType, Iterable[Vector2DType]]] = None,
                    pos: Optional[Union[Vector2DType, Iterable[Vector2DType]]] = None
                    ) -> 'Sketch':
        """
        Cuts an ellipse from the sketch object.

        Args:
            size_x (DimensionDefinitionType): The size of the ellipse along the x-axis.
            size_y (DimensionDefinitionType): The size of the ellipse along the y-axis.
            angle (float, optional): The angle of rotation. Defaults to 0.
            center (CenterDefinitionType, optional): Determines whether the ellipse is centered.
                If False, the ellipse will start from the origin.
                Can also be "X" or "Y" to center in only one direction. Defaults to True.
            positions (Vector2DType | Iterable[Vector2DType], optional): If given, a ellipse is cuts for each of the entries,
                specifying the offset as (x,y) tuple.
                Defaults to None, which results in a single ellipse cut with no offset.
            pos: Shorthand for positions parameter, only use one of them.

        Returns:
            Sketch: The updated sketch object.
        """
        return self.__ellipse(size_x, size_y, "s", angle, center, positions, pos)

    def __ellipse(self,
                  size_x: DimensionDefinitionType,
                  size_y: DimensionDefinitionType,
                  mode: str,
                  angle: float = 0,
                  center: CenterDefinitionType = True,
                  positions: Optional[Union[Vector2DType, Iterable[Vector2DType]]] = None,
                  pos: Optional[Union[Vector2DType, Iterable[Vector2DType]]] = None
                  ) -> 'Sketch':
        (x1, x2), (y1, y2) = get_dimensions([size_x, size_y], center)
        action = lambda x: x.ellipse((x2 - x1) / 2.0, (y2 - y1) / 2.0, angle=angle, mode=mode)
        pos_list = self.__get_positions(positions, pos, [(0, 0)])
        return self.__perform_action(action, [(x + (x1 + x2) / 2.0, y + (y1 + y2) / 2.0) for (x, y) in pos_list])

    def add_polygon(self,
                    point_list: Iterable[Vector2DType],
                    *,
                    positions: Optional[Union[Vector2DType, Iterable[Vector2DType]]] = None,
                    pos: Optional[Union[Vector2DType, Iterable[Vector2DType]]] = None
                    ) -> 'Sketch':
        """
        Adds a polygon to the sketch.

        Args:
            point_list (Iterable[Vector2DType]): A list of points defining the polygon.
                The points must be given in counter-clockwise order.
            positions (Vector2DType | Iterable[Vector2DType], optional): If given, a polygon
                is added for each of the entries, specifying the offset as (x,y) tuple.
                Defaults to None, which results in a single polygon added with no offset.
            pos: Shorthand for positions parameter, only use one of them.

        Returns:
            Sketch: The modified sketch object.

        """
        action = lambda x: x.polygon(point_list)
        return self.__perform_action(action, self.__get_positions(positions, pos))

    def cut_polygon(self,
                    point_list: Iterable[Vector2DType],
                    *,
                    positions: Optional[Union[Vector2DType, Iterable[Vector2DType]]] = None,
                    pos: Optional[Union[Vector2DType, Iterable[Vector2DType]]] = None
                    ) -> 'Sketch':
        """
        Cuts a polygon from the sketch.

        Args:
            point_list (Iterable[Vector2DType]): A list of points defining the polygon.
                The points must be given in counter-clockwise order.
            positions (Vector2DType | Iterable[Vector2DType], optional): If given, a polygon is added for each of the entries,
                specifying the offset as (x,y) tuple.
                Defaults to None, which results in a single polygon added with no offset.
            pos: Shorthand for positions parameter, only use one of them.

        Returns:
            Sketch: The modified sketch object.

        """
        action = lambda x: x.polygon(point_list, mode="s")
        return self.__perform_action(action, self.__get_positions(positions, pos))

    def add_slot(self,
                 w: float,
                 h: float,
                 *,
                 angle: float = 0,
                 positions: Optional[Union[Vector2DType, Iterable[Vector2DType]]] = None,
                 pos: Optional[Union[Vector2DType, Iterable[Vector2DType]]] = None
                 ) -> 'Sketch':
        """
        Adds a slot to the sketch. The slot is defined by a width and height, and an angle of rotation. By default (rotation is 0),
        the slot is parallel to the x-axis. The width is the non-rounded part along the x-axis and the height is
        the extent along the y-axis. The part is centered at the origin unless the positions paramter is specified.

        Args:
            w (float): The width of the slot, the part without the rounded sides.
            h (float): The height of the slot.
            angle (float, optional): The angle of rotation for the slot. Defaults to 0, which means the slot is parallel to the x-axis.
            positions (Vector2DType | Iterable[Vector2DType], optional): If given, a slot is added for each of the entries, specifying the
                its respective center as (x,y) tuple. Defaults to None, which results in a single slot added at the origin.
            pos: Shorthand for positions parameter, only use one of them.

        Returns:
            Sketch: The updated sketch object.
        """
        action = lambda x: x.slot(w, h, angle=angle)
        return self.__perform_action(action, self.__get_positions(positions, pos))

    def cut_slot(self,
                 w: float,
                 h: float,
                 *,
                 angle: float = 0,
                 positions: Optional[Union[Vector2DType, Iterable[Vector2DType]]] = None,
                 pos: Optional[Union[Vector2DType, Iterable[Vector2DType]]] = None
                 ) -> 'Sketch':
        """
        Cuts a slot from sketch. The slot is defined by a width and height, and an angle of rotation. By default (rotation is 0),
        the slot is parallel to the x-axis. The width is the non-rounded part along the x-axis and the height is the extent
        along the y-axis.
        The part is centered at the origin unless the positions paramter is specified.

        Args:
            w (float): The width of the slot, the part without the rounded sides.
            h (float): The height of the slot.
            angle (float, optional): The angle of rotation for the slot. Defaults to 0, which means the slot is parallel to the x-axis.
            positions (Vector2DType | Iterable[Vector2DType], optional): If given, a slot is added for each of the entries, specifying the
                its respective center as (x,y) tuple. Defaults to None, which results in a single slot added at the origin.
            pos: Shorthand for positions parameter, only use one of them.

        Returns:
            Sketch: The updated sketch object.
        """
        action = lambda x: x.slot(w, h, angle=angle, mode="s")
        return self.__perform_action(action, self.__get_positions(positions, pos))

    def add_import_dxf(self,
                       dxf_filename: str,
                       *,
                       positions: Optional[Union[Vector2DType, Iterable[Vector2DType]]] = None,
                       pos: Optional[Union[Vector2DType, Iterable[Vector2DType]]] = None,
                       tolerance: float = 1e-3
                       ) -> 'Sketch':
        """
        Imports a DXF file and adds it to the sketch object. The DXF mus contain one or more closed loops from lines and curves.

        Args:
            dxf_filename (str): The filename of the DXF file to import.
            positions (Vector2DType | Iterable[Vector2DType], optional): Optional positions to place the imported objects.
                If not provided, the objects will be placed at the origin.
            pos: Shorthand for positions parameter, only use one of them.
            tolerance (float): The tolerance to use for the import. Defaults to 1e-3.

        Returns:
            Sketch: The updated sketch object.

        """
        action = lambda x: x.importDXF(dxf_filename, tol=tolerance)
        return self.__perform_action(action, self.__get_positions(positions, pos))

    def cut_import_dxf(self,
                       dxf_filename: str,
                       *,
                       positions: Optional[Union[Vector2DType, Iterable[Vector2DType]]] = None,
                       pos: Optional[Union[Vector2DType, Iterable[Vector2DType]]] = None,
                       tolerance: float = 1e-3
                       ) -> 'Sketch':
        """
        Imports a DXF file and cuts it from the sketch object. The DXF mus contain one or more closed loops from lines and curves.

        Args:
            dxf_filename (str): The filename of the DXF file to import.
            positions (Vector2DType | Iterable[Vector2DType], optional): Optional positions to place the imported objects.
                If not provided, the objects will be placed at the origin.
            pos: Shorthand for positions parameter, only use one of them.
            tolerance (float): The tolerance to use for the import. Defaults to 1e-3.

        Returns:
            Sketch: The updated sketch object.
        """
        action = lambda x: x.importDXF(dxf_filename, tol=tolerance, mode="s")
        return self.__perform_action(action, self.__get_positions(positions, pos))

    def _select_vertices(self,
                         query: Union[str, Vector2DType, Iterable[Vector2DType]]
                         ) -> bool:
        '''
        Selects vertices in the sketch. The query can be a search string, a point or a point list.
        '''
        if isinstance(query, str):
            if query == "ALL" or query == "*":
                self.__sketch.reset().vertices()
                return True
            else:
                self.__sketch.reset().vertices(query)
                return True

        if isinstance(query, tuple):
            vertex = (query[0], query[1], 0)
            vertices = [vertex]
        else:  # list
            vertices = [(v[0], v[1], 0) for v in query]
        self.__sketch.reset().vertices(NearestToPointListSelector(vertices))
        return True

    def fillet(self,
               query: Union[str, Vector2DType, Iterable[Vector2DType]],
               radius: float
               ) -> 'Sketch':
        """
        Fillets corners of the sketch.

        Args:
            query (str | Vector2DType | Iterable[Vector2DType]): The vertices to fillet.
                Can be "ALL" or "*" to fillet all vertices.
                You can also pass a point or a list of points to fillet the nearest vertices.
            radius (float): The fillet radius.

        Returns:
            Sketch: The modified sketch object.
        """
        success = self._select_vertices(query)
        if success:
            self.__sketch.fillet(radius).clean().reset()
        return self

    def chamfer(self,
                query: Union[str, Vector2DType, Iterable[Vector2DType]],
                amount: float
                ) -> 'Sketch':
        """
        Chamfers corners of the sketch.

        Args:
            query (str | Vector2DType | Iterable[Vector2DType]): The vertices to chamfer.
                Can be "ALL" or "*" to chamfer all vertices.
                You can also pass a point or a list of points to chamfer the nearest vertices.
            amount (float): The chamfer amount.

        Returns:
            Sketch: The modified sketch object.
        """
        success = self._select_vertices(query)
        if success:
            self.__sketch.chamfer(amount).clean().reset()
        return self

    def export_dxf(self,
                   filepath: str
                   ) -> None:
        """
        Export the sketch to a DXF file.

        Args:
            filename (str): The name of the DXF file to export to. If passing a path, the parent directory must exist.
        """
        export_sketch_DXF(self.__sketch, filepath)

    def move(self,
             translationVector: Vector2DType
             ) -> 'Sketch':
        """
        Moves the Sketch by the specified translation vector.

        Args:
            translationVector (Vector2DType): The translation vector specifying the amount and direction of the movement.

        Returns:
            Sketch: The updated Sketch after the movement.
        """
        self.__sketch = self.__sketch.moved(cq.Location(cq.Vector(translationVector)))
        return self

    def rotate(self,
               degrees
               ) -> 'Sketch':
        """
        Rotates the sketch object by the specified number of degrees.

        Args:
            degrees (float): The number of degrees to rotate the sketch object.

        Returns:
            Sketch: The rotated sketch object.
        """
        self.__sketch = self.__sketch.moved(cq.Location(cq.Vector(), cq.Vector(0, 0, 1), degrees))
        return self

    def cq(self) -> cq.Sketch:
        """
        Returns the underlying CadQuery sketch object. Useful when mixing CadQuery and Cadscript code.
        """
        return self.__sketch

    def copy(self) -> 'Sketch':
        """
        Returns a copy of the sketch.

        Returns:
            Sketch: The copied sketch.
        """
        return Sketch(self.__sketch.copy())

    def find_vertices(self,
                      search: Optional[str] = None
                      ) -> List[Vector2DType]:
        if search is None or str == "ALL" or str == "*":
            self.__sketch.vertices()  # select all vertices
        else:
            self.__sketch.vertices(search)  # select vertices matching search
        pos_list = [(v.X, v.Y) for v in self.__sketch._selection if isinstance(v, cq.Vertex)]
        self.__sketch.reset()  # delete selection again
        return pos_list
    
    def get_extent(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """
        Returns the extent of the bounding box of the sketch.
        """
        faces = [s for s in self.__sketch.faces() if isinstance(s, cq.Shape)]
        if not faces:
            return ((0, 0), (0, 0))

        bb = faces[0].BoundingBox()
        for s in faces[1:]:
            bb.add(s.BoundingBox())
        return ((bb.xmin, bb.xmax), (bb.ymin, bb.ymax))
