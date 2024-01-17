# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path
import tempfile
import time
import inspect
from typing import Optional, Union, Tuple

import cadquery as cq

from .typedefs import DimensionDefinitionType, CenterDefinitionType

from .body import Body
from .sketch import Sketch
from .construction_plane import ConstructionPlane
from .assembly import Assembly
from .helpers import get_dimensions
from .patterns import pattern_grid, pattern_rect  # noqa


def make_box(sizex: DimensionDefinitionType,
             sizey: DimensionDefinitionType,
             sizez: DimensionDefinitionType,
             *,
             center: CenterDefinitionType = True
             ) -> 'Body':
    """
    Create a box-shaped body with the given dimensions.

    Args:
        sizex (DimensionDefinitionType): The size of the box along the x-axis.
        sizey (DimensionDefinitionType): The size of the box along the y-axis.
        sizez (DimensionDefinitionType): The size of the box along the z-axis.
        center (CenterDefinitionType, optional): Whether to center the box at the origin. If False, the box will start from the origin.
            Can also be "X", "Y" or "Z" to center in only one direction or "XY", "XZ", "YZ" to center in two directions.
            Defaults to True which centers the box in all directions.

    Returns:
        Body: The created box-shaped body.
    """
    dimx, dimy, dimz = get_dimensions([sizex, sizey, sizez], center)
    return __make_box_min_max(dimx[0], dimx[1], dimy[0], dimy[1], dimz[0], dimz[1])


def __make_box_min_max(x1: float,
                       x2: float,
                       y1: float,
                       y2: float,
                       z1: float,
                       z2: float
                       ) -> 'Body':
    solid = cq.Solid.makeBox(x2 - x1, y2 - y1, z2 - z1).move(cq.Location(cq.Vector(x1, y1, z1)))
    wp = cq.Workplane(obj=solid)
    return Body(wp)


def make_extrude(plane: Union[ConstructionPlane, str],
                 sketch: Sketch,
                 amount: Union[float, Tuple[float, float]]
                 ) -> 'Body':
    """
    Create an extrusion from a sketch.

    Args:
        plane (Union[ConstructionPlane,str]): The plane to extrude on.
            Can be one of the strings "XY", "YZ", "XZ", "front", "back", "top", "bottom", "left" or "right"
        sketch (Sketch): The sketch to extrude.
        amount (float): The amount of extrusion. Can also be a tuple of two floats to extrude between two planes with the given offsets.

    Returns:
        Body: The extruded body.
    """
    if isinstance(amount, (float, int)):
        if isinstance(plane, str):
            wp = cq.Workplane(plane)
        else:
            wp = plane.cq()
        extr = wp.placeSketch(sketch.cq()).extrude(amount, False)
        return Body(extr)
    else:
        # test that the tuple has two elements
        if not isinstance(amount, tuple) or len(amount) != 2:
            raise ValueError("amount must be a float or a tuple of two floats")
        start_plane = make_construction_plane(plane, amount[0])
        return make_extrude(start_plane, sketch, amount[1] - amount[0])


def make_text(text: str,
              size: float,
              height: float,
              *,
              center: CenterDefinitionType = True,
              font: str = "Arial",
              ):
    """
    Create a 3D text object.

    Args:
        text (str): The text to be created.
        size (float): The size of the text.
        height (float): The height of the text.
        center (CenterDefinitionType, optional): Whether to center the text object at the origin. If False, the text will start from the origin.
            Can also be "X", "Y" or "Z" to center in only one direction or "XY", "XZ", "YZ" to center in two directions.
            Defaults to True which centers the text object in all directions.
        font (str, optional): The font of the text. Defaults to "Arial".

    Returns:
        Body: The 3D text object.
    """
    c = cq.Compound.makeText(text, size, height, font=font)
    body = Body(cq.Workplane(obj=c))
    (extendx, extendy, extendz) = body.get_extent()
    (startx, _), (starty, _), (startz, _) = get_dimensions(
        [extendx[1] - extendx[0], extendy[1] - extendy[0], extendz[1] - extendz[0]], center)
    return body.move((startx - extendx[0], starty - extendy[0], startz - extendz[0]))


def make_construction_plane(plane: Union[ConstructionPlane, str], offset: Optional[float] = None):
    if isinstance(plane, str):
        wp = cq.Workplane(plane)
    else:
        wp = plane.cq()
    if offset is not None:
        wp = wp.workplane(offset=offset)
    return ConstructionPlane(wp)


def make_sketch():
    """
    Creates a new empty sketch object.

    Returns:
        Sketch: The newly created sketch object.
    """
    sketch = cq.Sketch()
    return Sketch(sketch)


def import_step(path):
    """
    Import a STEP file and return a Body object.

    Args:
        path (str): The path to the STEP file.

    Returns:
        Body: The imported body as a Body object.
    """
    wp = cq.importers.importStep(path)
    return Body(wp)


def show(item: Union[Body, Sketch, ConstructionPlane, Assembly]):
    '''
    If inside CQ-Editor, will display the item in the 3D view.
    Otherwise save a STL or DXF into the system temp directory.

    Args:
        item: the item to show. Can be a :class:`Body` or a :class:`Sketch`
    '''
    # check if there is a function "show_object" available
    # if so, call it
    show_fn = __get_show_fn()
    if show_fn:
        show_fn(item.cq())
    # TODO when cadquery.vis is available
    # show(item)

    # otherwise, export file to temp dir and print path
    else:
        temp_dir = Path(tempfile.gettempdir())
        temp_path = str(temp_dir / f"cadscript_{time.time()}")
        if isinstance(item, Body):
            temp_path = temp_path + ".stl"
            item.export_stl(temp_path)
            print("Cadscript body exported to ", temp_path)
        elif isinstance(item, Sketch):
            temp_path = temp_path + ".dxf"
            item.export_dxf(temp_path)
            print("Cadscript sketch exported to ", temp_path)


# examine the context of the caller. check if there is a function "show_object" available, return a reference to it
def __get_show_fn():
    # Start with the immediate caller's caller frame.
    f = inspect.currentframe()
    if f is None or f.f_back is None:
        return None
    frame = f.f_back.f_back

    while frame:
        # Check global scope.
        if 'show_object' in frame.f_globals:
            potential_func = frame.f_globals['show_object']
            if callable(potential_func):
                return potential_func

        # Move up to the next caller in the stack.
        frame = frame.f_back

    # If function is not found in any ancestor's scope, return None.
    return None
