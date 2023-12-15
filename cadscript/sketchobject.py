import cadquery as cq

from typing import Any, Optional, Tuple, Union

from .export import export_sketch_DXF
from .helpers import get_dimensions



class SketchObject:
    
    def __init__(self, sketch: cq.Sketch) -> None:
      self.sketch = sketch
      self.finalized_sketch = None

    def cq(self):
      return self.sketch if self.sketch else self.finalized_sketch

    def copy(self):
      return SketchObject(self.sketch.copy())

    def finalize(self):
      self.finalized_sketch = self.sketch
      return self

    def perform_action(self, action, positions):
      if positions:
        self.sketch = action(self.sketch.push(positions))
      else:
        self.sketch = action(self.sketch)
      self.sketch.reset()
      return self

    def rect_helper(self, sketch, size_x, size_y, center: Any, mode="a"):
      dim1, dim2 = get_dimensions([size_x, size_y], center)
      x1, x2 = dim1
      y1, y2 = dim2
      return sketch.polygon([cq.Vector(x1, y1), cq.Vector(x1, y2), cq.Vector(x2, y2), cq.Vector(x2, y1), cq.Vector(x1, y1)], mode=mode)

    def add_rect(self, size_x: Union[float, Tuple[float, float]], size_y: Union[float, Tuple[float, float]], center: Any = True, positions: Any = None):
      action = lambda x: self.rect_helper(x, size_x, size_y, center)
      return self.perform_action(action, positions)

    def cut_rect(self, size_x: Union[float, Tuple[float, float]], size_y: Union[float, Tuple[float, float]], center: Any = True, positions: Any = None):
      action = lambda x: self.rect_helper(x, size_x, size_y, center, mode="s")
      return self.perform_action(action, positions)

    def add_circle(self, r, positions=None):
      action = lambda x: x.circle(r)
      return self.perform_action(action, positions)

    def cut_circle(self, r, positions=None):
      action = lambda x: x.circle(r, mode="s")
      return self.perform_action(action, positions)

    def add_polygon(self, point_list, positions=None):
      action = lambda x: x.polygon(point_list)
      return self.perform_action(action, positions)

    def cut_polygon(self, point_list, positions=None):
      action = lambda x: x.polygon(point_list, mode="s")
      return self.perform_action(action, positions)

    def add_slot(self, w, h, angle=0, positions=None):
      action = lambda x: x.slot(w, h, angle=angle)
      return self.perform_action(action, positions)

    def cut_slot(self, w, h, angle=0, positions=None):
      action = lambda x: x.slot(w, h, angle=angle, mode="s")
      return self.perform_action(action, positions)

    def add_import_dxf(self, dxf_filename, positions=None):
      action = lambda x: x.importDXF(dxf_filename)
      return self.perform_action(action, positions)

    def cut_import_dxf(self, dxf_filename, positions=None):
      action = lambda x: x.importDXF(dxf_filename, mode="s")
      return self.perform_action(action, positions)

    def fillet(self, edges_str, amount):
      if edges_str == "ALL":
        result = self.sketch.reset().vertices().fillet(amount)
      else:
        raise ValueError("unknown edge selector")
      self.sketch = result
      return self

    def chamfer(self, edges_str, amount):
      if edges_str == "ALL":
        result = self.sketch.reset().vertices().chamfer(amount)
      else:
        raise ValueError("unknown edge selector")
      self.sketch = result
      return self

    def export_dxf(self, filename):
        export_sketch_DXF(self.sketch, filename)

    def move(self, translationVector):
        self.sketch = self.sketch.moved(cq.Location(cq.Vector(translationVector)))
        return self

    def rotate(self, degrees):
        self.sketch = self.sketch.moved(cq.Location(cq.Vector(),cq.Vector(0, 0, 1), degrees))
        return self