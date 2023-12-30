# Copyright (C) 2023 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

import cadquery as cq

from typing import Any, Callable, Iterable, Optional, TypeVar

from .typedefs import DimensionDefinitionType, CenterDefinitionType, EdgeQueryType, Vector2DType, Vector3DType
from .export import export_sketch_DXF
from .helpers import get_dimensions

class SketchObject:
    
    sketch: cq.Sketch
    finalized_sketch: Optional[cq.Sketch]

    def __init__(self, sketch: cq.Sketch) -> None:
      self.sketch = sketch
      self.finalized_sketch = None

    def cq(self) -> Optional[cq.Sketch]:
      return self.sketch

    def copy(self) -> 'SketchObject':
      return SketchObject(self.sketch.copy())

    def finalize(self) -> 'SketchObject':
      self.finalized_sketch = self.sketch
      return self

    def __perform_action(self, action, positions: Optional[Iterable[Vector2DType]]) -> 'SketchObject':
      if positions:
        self.sketch = action(self.sketch.push(positions))
      else:
        self.sketch = action(self.sketch)
      self.sketch.reset()
      return self

    def __rect_helper(self, sketch, size_x: DimensionDefinitionType, size_y: DimensionDefinitionType, center: CenterDefinitionType, mode="a"):
      dim1, dim2 = get_dimensions([size_x, size_y], center)
      x1, x2 = dim1
      y1, y2 = dim2
      return sketch.polygon([cq.Vector(x1, y1), cq.Vector(x1, y2), cq.Vector(x2, y2), cq.Vector(x2, y1), cq.Vector(x1, y1)], mode=mode)

    def add_rect(self, size_x: DimensionDefinitionType, size_y: DimensionDefinitionType, *, center: CenterDefinitionType = True, positions: Optional[Iterable[Vector2DType]] = None) -> 'SketchObject':
      action = lambda x: self.__rect_helper(x, size_x, size_y, center)
      return self.__perform_action(action, positions)

    def cut_rect(self, size_x: DimensionDefinitionType, size_y: DimensionDefinitionType, *, center: CenterDefinitionType = True, positions: Optional[Iterable[Vector2DType]] = None) -> 'SketchObject':
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
      
    def add_circle(self, *, r:Optional[float]=None, radius:Optional[float]=None, d:Optional[float]=None, diameter:Optional[float]=None, positions: Optional[Iterable[Vector2DType]] = None) -> 'SketchObject':
      r = self.__get_radius(r, radius, d, diameter)    
      action = lambda x: x.circle(r)
      return self.__perform_action(action, positions)

    def cut_circle(self, *, r:Optional[float]=None, radius:Optional[float]=None, d:Optional[float]=None, diameter:Optional[float]=None, positions: Optional[Iterable[Vector2DType]] = None) -> 'SketchObject':
      r = self.__get_radius(r, radius, d, diameter)    
      action = lambda x: x.circle(r, mode="s")
      return self.__perform_action(action, positions)

    def add_polygon(self, point_list: Iterable[Vector2DType], *, positions: Optional[Iterable[Vector2DType]] = None) -> 'SketchObject':
      action = lambda x: x.polygon(point_list)
      return self.__perform_action(action, positions)

    def cut_polygon(self, point_list: Iterable[Vector2DType], *, positions: Optional[Iterable[Vector2DType]] = None) -> 'SketchObject':
      action = lambda x: x.polygon(point_list, mode="s")
      return self.__perform_action(action, positions)

    def add_slot(self, w:float, h:float, *, angle:float=0, positions: Optional[Iterable[Vector2DType]] = None) -> 'SketchObject':
      action = lambda x: x.slot(w, h, angle=angle)
      return self.__perform_action(action, positions)

    def cut_slot(self, w:float, h:float, *, angle:float=0, positions: Optional[Iterable[Vector2DType]] = None) -> 'SketchObject':
      action = lambda x: x.slot(w, h, angle=angle, mode="s")
      return self.__perform_action(action, positions)

    def add_import_dxf(self, dxf_filename:str, *, positions: Optional[Iterable[Vector2DType]] = None, tolerance:float = 1e-3) -> 'SketchObject':
      action = lambda x: x.importDXF(dxf_filename, tol=tolerance)
      return self.__perform_action(action, positions)

    def cut_import_dxf(self, dxf_filename:str, *, positions: Optional[Iterable[Vector2DType]] = None, tolerance:float = 1e-3) -> 'SketchObject':
      action = lambda x: x.importDXF(dxf_filename, tol=tolerance, mode="s")
      return self.__perform_action(action, positions)

    def fillet(self, edges_str:EdgeQueryType, amount:float) -> 'SketchObject':
      #todo support edge selector
      if edges_str == "ALL":
        result = self.sketch.reset().vertices().fillet(amount)
      else:
        raise ValueError("unknown edge selector")
      self.sketch = result
      return self

    def chamfer(self, edges_str:EdgeQueryType, amount:float) -> 'SketchObject':
      #todo support edge selector
      if edges_str == "ALL":
        result = self.sketch.reset().vertices().chamfer(amount)
      else:
        raise ValueError("unknown edge selector")
      self.sketch = result
      return self

    def export_dxf(self, filename:str) -> None:
        export_sketch_DXF(self.sketch, filename)

    def move(self, translationVector:Vector2DType) -> 'SketchObject':
        self.sketch = self.sketch.moved(cq.Location(cq.Vector(translationVector)))
        return self

    def rotate(self, degrees) -> 'SketchObject':
        self.sketch = self.sketch.moved(cq.Location(cq.Vector(),cq.Vector(0, 0, 1), degrees))
        return self