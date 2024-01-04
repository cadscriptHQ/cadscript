# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

import cadquery as cq

from typing import Any, Callable, Iterable, Optional, TypeVar

from .typedefs import DimensionDefinitionType, CenterDefinitionType, EdgeQueryType, Vector2DType, Vector3DType
from .export import export_sketch_DXF
from .helpers import get_dimensions

class Sketch:
    """
    Represents a 2D sketch. Sketch instances are typically created using :func:`cadscript.make_sketch`.
    """
    __sketch: cq.Sketch
    __finalized_sketch: Optional[cq.Sketch]

    def __init__(self, sketch: cq.Sketch) -> None:
      self.__sketch = sketch
      self.__finalized_sketch = None


    def finalize(self) -> 'Sketch':
      self.__finalized_sketch = self.__sketch
      return self

    def __perform_action(self, action, positions: Optional[Iterable[Vector2DType]]) -> 'Sketch':
      if positions:
        self.__sketch = action(self.__sketch.push(positions))
      else:
        self.__sketch = action(self.__sketch)
      self.__sketch.reset().clean()
      return self

    def __rect_helper(self, sketch, size_x: DimensionDefinitionType, size_y: DimensionDefinitionType, center: CenterDefinitionType, mode="a"):
      dim1, dim2 = get_dimensions([size_x, size_y], center)
      x1, x2 = dim1
      y1, y2 = dim2
      return sketch.polygon([cq.Vector(x1, y1), cq.Vector(x1, y2), cq.Vector(x2, y2), cq.Vector(x2, y1), cq.Vector(x1, y1)], mode=mode)

    def add_rect(self, size_x: DimensionDefinitionType, size_y: DimensionDefinitionType, *, center: CenterDefinitionType = True, positions: Optional[Iterable[Vector2DType]] = None) -> 'Sketch':
      """
      Adds a rectangle to the sketch object.

      Args:
        size_x (DimensionDefinitionType): The size of the rectangle along the x-axis.
        size_y (DimensionDefinitionType): The size of the rectangle along the y-axis.
        center (CenterDefinitionType, optional): Determines whether the rectangle is centered. If False, the rectangle will start from the origin.
            Can also be "X" or "Y" to center in only one direction. Defaults to True.
        positions (Optional[Iterable[Vector2DType]], optional): If given, a rectangle is added for each of the entries, specifying the offset as (x,y) tuple. 
            Defaults to None, which results in a single rectangle added with no offset.

      Returns:
        Sketch: The updated sketch object.
      """
      action = lambda x: x.rect(size_x, size_y)
      #action = lambda x: self.__rect_helper(x, size_x, size_y, center)
      return self.__perform_action(action, positions)

    def cut_rect(self, size_x: DimensionDefinitionType, size_y: DimensionDefinitionType, *, center: CenterDefinitionType = True, positions: Optional[Iterable[Vector2DType]] = None) -> 'Sketch':
      """
      Cuts a rectangle from the sketch object.

      Args:
        size_x (DimensionDefinitionType): The size of the rectangle along the x-axis.
        size_y (DimensionDefinitionType): The size of the rectangle along the y-axis.
        center (CenterDefinitionType, optional): Determines whether the rectangle is centered. If False, the rectangle will start from the origin.
            Can also be "X" or "Y" to center in only one direction. Defaults to True.
        positions (Optional[Iterable[Vector2DType]], optional): If given, a rectangle is cut for each of the entries, specifying the offset as (x,y) tuple. 
            Defaults to None, which results in a single rectangle cut with no offset.

      Returns:
        Sketch: The updated sketch object.
      """
      action = lambda x: self.__rect_helper(x, size_x, size_y, center, mode="s")
      return self.__perform_action(action, positions)

    def __get_radius(self, r:Optional[float]=None, radius:Optional[float]=None, d:Optional[float]=None, diameter:Optional[float]=None) -> float:
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
      
    def add_circle(self, *, r:Optional[float]=None, radius:Optional[float]=None, d:Optional[float]=None, diameter:Optional[float]=None, positions: Optional[Iterable[Vector2DType]] = None) -> 'Sketch':
      """
      Adds a circle to the sketch. One of the parameters 'r', 'radius', 'd' or 'diameter' must be specified.

      Parameters:
        r (Optional[float]): The radius of the circle.
        radius (Optional[float]): The radius of the circle (alternative to 'r').
        d (Optional[float]): The diameter of the circle.
        diameter (Optional[float]): The diameter of the circle (alternative to 'd').
        positions (Optional[Iterable[Vector2DType]]): If given, a circle is added for each of the entries, specifying the center as (x,y) tuple.  If None, a single circle will be added at the origin.

      Returns:
        Sketch: The updated sketch object.
      """
      r = self.__get_radius(r, radius, d, diameter)    
      action = lambda x: x.circle(r)
      return self.__perform_action(action, positions)

    def cut_circle(self, *, r:Optional[float]=None, radius:Optional[float]=None, d:Optional[float]=None, diameter:Optional[float]=None, positions: Optional[Iterable[Vector2DType]] = None) -> 'Sketch':
      """
      Cuts a circle from the sketch. One of the parameters 'r', 'radius', 'd' or 'diameter' must be specified.

      Parameters:
        r (Optional[float]): The radius of the circle.
        radius (Optional[float]): The radius of the circle (alternative to 'r').
        d (Optional[float]): The diameter of the circle.
        diameter (Optional[float]): The diameter of the circle (alternative to 'd').
        positions (Optional[Iterable[Vector2DType]]): If given, a circle is cut for each of the entries, specifying the center as (x,y) tuple.  If None, a single circle will be cut at the origin.

      Returns:
        Sketch: The updated sketch object.
      """
      r = self.__get_radius(r, radius, d, diameter)    
      action = lambda x: x.circle(r, mode="s")
      return self.__perform_action(action, positions)

    def add_polygon(self, point_list: Iterable[Vector2DType], *, positions: Optional[Iterable[Vector2DType]] = None) -> 'Sketch':
      """
      Adds a polygon to the sketch.

      Args:
        point_list (Iterable[Vector2DType]): A list of points defining the polygon.
        positions (Optional[Iterable[Vector2DType]], optional): If given, a polygon is added for each of the entries, specifying the offset as (x,y) tuple. 
            Defaults to None, which results in a single polygon added with no offset.

      Returns:
        Sketch: The modified sketch object.

      """
      action = lambda x: x.polygon(point_list)
      return self.__perform_action(action, positions)

    def cut_polygon(self, point_list: Iterable[Vector2DType], *, positions: Optional[Iterable[Vector2DType]] = None) -> 'Sketch':
      """
      Cuts a polygon from the sketch.

      Args:
        point_list (Iterable[Vector2DType]): A list of points defining the polygon.
        positions (Optional[Iterable[Vector2DType]], optional): If given, a polygon is added for each of the entries, specifying the offset as (x,y) tuple. 
            Defaults to None, which results in a single polygon added with no offset.

      Returns:
        Sketch: The modified sketch object.

      """
      action = lambda x: x.polygon(point_list, mode="s")
      return self.__perform_action(action, positions)

    def add_slot(self, w: float, h: float, *, angle: float = 0, positions: Optional[Iterable[Vector2DType]] = None) -> 'Sketch':
      """
      Adds a slot to the sketch. The slot is defined by a width and height, and an angle of rotation. By default (rotation is 0), 
      the slot is parallel to the x-axis. The width is the non-rounded part along the x-axis and the height is the extent along the y-axis.
      The part is centered at the origin unless the positions paramter is specified.

      Args:
        w (float): The width of the slot, the part without the rounded sides.
        h (float): The height of the slot.
        angle (float, optional): The angle of rotation for the slot. Defaults to 0, which means the slot is parallel to the x-axis.
        positions (Optional[Iterable[Vector2DType]], optional): If given, a slot is added for each of the entries, specifying the 
            its respective center as (x,y) tuple. Defaults to None, which results in a single slot added at the origin.

      Returns:
        Sketch: The updated sketch object.
      """
      action = lambda x: x.slot(w, h, angle=angle)
      return self.__perform_action(action, positions)    

    def cut_slot(self, w:float, h:float, *, angle:float=0, positions: Optional[Iterable[Vector2DType]] = None) -> 'Sketch':
      """
      Cuts a slot from sketch. The slot is defined by a width and height, and an angle of rotation. By default (rotation is 0), 
      the slot is parallel to the x-axis. The width is the non-rounded part along the x-axis and the height is the extent along the y-axis.
      The part is centered at the origin unless the positions paramter is specified.

      Args:
        w (float): The width of the slot, the part without the rounded sides.
        h (float): The height of the slot.
        angle (float, optional): The angle of rotation for the slot. Defaults to 0, which means the slot is parallel to the x-axis.
        positions (Optional[Iterable[Vector2DType]], optional): If given, a slot is added for each of the entries, specifying the 
            its respective center as (x,y) tuple. Defaults to None, which results in a single slot added at the origin.

      Returns:
        Sketch: The updated sketch object.
      """
      action = lambda x: x.slot(w, h, angle=angle, mode="s")
      return self.__perform_action(action, positions)

    def add_import_dxf(self, dxf_filename:str, *, positions: Optional[Iterable[Vector2DType]] = None, tolerance:float = 1e-3) -> 'Sketch':
      """
      Imports a DXF file and adds it to the sketch object. The DXF mus contain one or more closed loops from lines and curves.

      Args:
        dxf_filename (str): The filename of the DXF file to import.
        positions (Optional[Iterable[Vector2DType]]): Optional positions to place the imported objects. If not provided, the objects will be placed at the origin.
        tolerance (float): The tolerance to use for the import. Defaults to 1e-3.

      Returns:
        Sketch: The updated sketch object.

      """
      action = lambda x: x.importDXF(dxf_filename, tol=tolerance)
      return self.__perform_action(action, positions)

    def cut_import_dxf(self, dxf_filename:str, *, positions: Optional[Iterable[Vector2DType]] = None, tolerance:float = 1e-3) -> 'Sketch':
      """
      Imports a DXF file and cuts it from the sketch object. The DXF mus contain one or more closed loops from lines and curves.

      Args:
        dxf_filename (str): The filename of the DXF file to import.
        positions (Optional[Iterable[Vector2DType]]): Optional positions to place the imported objects. If not provided, the objects will be placed at the origin.
        tolerance (float): The tolerance to use for the import. Defaults to 1e-3.

      Returns:
        Sketch: The updated sketch object.

      """
      action = lambda x: x.importDXF(dxf_filename, tol=tolerance, mode="s")
      return self.__perform_action(action, positions)

    def fillet(self, edges_str:EdgeQueryType, amount:float) -> 'Sketch':
      """
      Fillets the edges of the sketch.

      Args:
        edges_str (EdgeQueryType): The edges to fillet. Can be "ALL" to fillet all edges.
        amount (float): The fillet amount.

      Returns:
        Sketch: The modified sketch object.
      """
      #todo support edge selector
      if edges_str == "ALL":
        result = self.__sketch.reset().vertices().fillet(amount)
      else:
        raise ValueError("unknown edge selector")
      self.__sketch = result
      return self

    def chamfer(self, edges_str:EdgeQueryType, amount:float) -> 'Sketch':
      """
      Chamfers the edges of the sketch.

      Args:
        edges_str (EdgeQueryType): The edges to chamfer. Can be "ALL" to chamfer all edges.
        amount (float): The chamfer amount.

      Returns:
        Sketch: The modified sketch object.
      """
      #todo support edge selector
      if edges_str == "ALL":
        result = self.__sketch.reset().vertices().chamfer(amount)
      else:
        raise ValueError("unknown edge selector")
      self.__sketch = result
      return self

    def export_dxf(self, filepath:str) -> None:
      """
      Export the sketch to a DXF file.

      Args:
        filename (str): The name of the DXF file to export to. If passing a path, the parent directory must exist.
      """
      export_sketch_DXF(self.__sketch, filepath)

    def move(self, translationVector:Vector2DType) -> 'Sketch':
      """
      Moves the Sketch by the specified translation vector.

      Args:
        translationVector (Vector2DType): The translation vector specifying the amount and direction of the movement.

      Returns:
        Sketch: The updated Sketch after the movement.

      """
      self.__sketch = self.__sketch.moved(cq.Location(cq.Vector(translationVector)))
      return self

    def rotate(self, degrees) -> 'Sketch':
      """
      Rotates the sketch object by the specified number of degrees.

      Args:
        degrees (float): The number of degrees to rotate the sketch object.

      Returns:
        Sketch: The rotated sketch object.
      """
      self.__sketch = self.__sketch.moved(cq.Location(cq.Vector(),cq.Vector(0, 0, 1), degrees))
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
