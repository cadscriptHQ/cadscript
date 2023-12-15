
import ezdxf
import cadquery as cq
from typing import Optional, Literal


def export_sketch_DXF(
    s: cq.Sketch,
    fname: str,
    approx: Optional[Literal["spline", "arc"]] = None,
    tolerance: float = 1e-3,
):
    """
    Export Sketch content to DXF. Works with 2D sections.

    :param s: Sketch to be exported.
    :param fname: Output filename.
    :param approx: Approximation strategy. None means no approximation is applied.
    "spline" results in all splines being approximated as cubic splines. "arc" results
    in all curves being approximated as arcs and straight segments.
    :param tolerance: Approximation tolerance.

    """
    w = cq.Workplane().placeSketch(s)
    plane = w.plane
    
    dxf = ezdxf.new()
    msp = dxf.modelspace()

    for f in s.faces():
      
      shape = f.transformShape(plane.fG)

      if approx == "spline":
          edges = [
              e.toSplines() if e.geomType() == "BSPLINE" else e for e in shape.Edges()
          ]

      elif approx == "arc":
          edges = []

          # this is needed to handle free wires
          for el in shape.Wires():
              edges.extend(cq.Face.makeFromWires(el).toArcs(tolerance).Edges())

      else:
          edges = shape.Edges()

      for e in edges:

          conv = cq.exporters.dxf.DXF_CONVERTERS.get(e.geomType(), cq.exporters.dxf._dxf_spline)
          conv(e, msp, plane)

    dxf.saveas(fname)