# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

import cadquery as cq

from typing import Optional, Literal


def export_sketch_DXF(
    s: cq.Sketch,
    fname: str,
    approx: Optional[Literal["spline", "arc"]] = None,
    tolerance: float = 1e-3    
):
    """
    Export Sketch content to DXF. Works with 2D sections.

    :param s: Sketch to be exported.
    :param fname: Output filename.
    :param approx: Approximation strategy. None means no approximation is applied.
        "spline" results in all splines being approximated as cubic splines. "arc" results
        in all curves being approximated as arcs and straight segments.
    :param tolerance: Approximation tolerance.

    Remark: uses mm as unit.
    """
    w = cq.Workplane().add(s._faces)  # see https://github.com/CadQuery/cadquery/issues/1575
    cq.exporters.dxf.exportDXF(w, fname, approx=approx, tolerance=tolerance)




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
