# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path
import tempfile
import time
import inspect
from typing import Literal, Optional, Union

import cadquery as cq
from .typedefs import DimensionDefinitionType, CenterDefinitionType

from .body import Body
from .sketch import Sketch
from .construction_plane import ConstructionPlane
from .assembly import Assembly
from .helpers import get_center_flags, get_dimension, get_dimensions_3d, get_height, get_radius
from .patterns import pattern_grid, pattern_rect, pattern_distribute, pattern_distribute_stretch  # noqa

from OCP.BRepPrimAPI import BRepPrimAPI_MakeSphere


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
    dimension = get_dimensions_3d([sizex, sizey, sizez], center)
    solid = cq.Solid.makeBox(dimension.size_x, dimension.size_y, dimension.size_z)
    solid = solid.move(cq.Location(dimension.min_corner))
    wp = cq.Workplane(obj=solid)
    return Body(wp)


def make_sphere(*,
                r: Optional[float] = None,
                radius: Optional[float] = None,
                d: Optional[float] = None,
                diameter: Optional[float] = None,
                center: CenterDefinitionType = True
                ) -> 'Body':
    """
    Create a spherical body with the given radius or diameter.

    Args:
        r (float, optional): The radius of the sphere (alternative to 'radius', 'd' or 'diameter').
        radius (float, optional): The radius of the sphere (alternative to 'r', 'd' or 'diameter').
        d (float, optional): The diameter of the sphere (alternative to 'r', 'radius' or 'diameter').
        diameter (float, optional): The diameter of the sphere (alternative to 'r', 'radius' or 'd').
        center (CenterDefinitionType, optional): Whether to center the box at the sphere. If False, the box will start from the origin.
            Can also be "X", "Y" or "Z" to center in only one direction or "XY", "XZ", "YZ" to center in two directions.
            Defaults to True which centers the box in all directions.

    Returns:
        Body: The created spherical body.
    """
    radius = get_radius(r, radius, d, diameter)
    cx, cy, cz = get_center_flags(center)
    center_point = cq.Vector(0 if cx else radius, 0 if cy else radius, 0 if cz else radius)
    solid = cq.Solid(BRepPrimAPI_MakeSphere(center_point.toPnt(), radius).Shape())
    wp = cq.Workplane(obj=solid)
    return Body(wp)


def make_cylinder(*,
                  h: Optional[float] = None,
                  height: Optional[float] = None,
                  r: Optional[float] = None,
                  radius: Optional[float] = None,
                  d: Optional[float] = None,
                  diameter: Optional[float] = None,
                  center: CenterDefinitionType = True,
                  direction: Optional[Literal["X", "Y", "Z"]] = "Z"
                  ) -> 'Body':
    """
    Create a cylinder with the given height and radius or diameter.
    The cylinder is aligned along the z-axis, unless specified otherwise using the 'direction' parameter.

    Args:
        h (float, optional): The height of the cylinder (alternative to 'height' parameter).
        height (float, optional): The height of the cylinder (alternative to 'h' parameter).
        r (float, optional): The radius of the cylinder (alternative to 'radius', 'd' or 'diameter').
        radius (float, optional): The radius of the cylinder (alternative to 'r', 'd' or 'diameter').
        d (float, optional): The diameter of the cylinder (alternative to 'r', 'radius' or 'diameter').
        diameter (float, optional): The diameter of the cylinder (alternative to 'r', 'radius' or 'd').
        center (CenterDefinitionType, optional): Whether to center the cylinder at the origin. If False, the box will start from the origin.
            Can also be "X", "Y" or "Z" to center in only one direction or "XY", "XZ", "YZ" to center in two directions.
            if "base" is specified, the cylinder will be centered at the base, e.g. in XY if direction is "Z".
            Defaults to True which centers the box in all directions.
        direction (str, optional): The direction of the cylinder axis. Can be one of "X", "Y" or "Z". Defaults to "Z".

    Returns:
        Body: The created body.
    """
    if isinstance(center, str) and center.lower() == "base":
        center = "XY" if direction == "Z" else "XZ" if direction == "Y" else "YZ"
    radius = get_radius(r, radius, d, diameter)
    cx, cy, cz = get_center_flags(center)
    height = get_height(h, height)
    dir = cq.Vector(0, 0, 1)
    base_center = cq.Vector(0 if cx else radius, 0 if cy else radius, -height / 2 if cz else 0)
    if direction == "X":
        dir = cq.Vector(1, 0, 0)
        base_center = cq.Vector(-height / 2 if cx else 0, 0 if cy else radius, 0 if cz else radius)
    elif direction == "Y":
        dir = cq.Vector(0, 1, 0)
        base_center = cq.Vector(0 if cx else radius, -height / 2 if cy else 0, 0 if cz else radius)
    solid = cq.Solid.makeCylinder(radius, height, base_center, dir)
    wp = cq.Workplane(obj=solid)
    return Body(wp)




def make_extrude(plane: Union[ConstructionPlane, str],
                 sketch: Sketch,
                 amount: DimensionDefinitionType,
                 center: bool = False
                 ) -> 'Body':
    """
    Create an extrusion from a sketch.

    Args:
        plane (Union[ConstructionPlane,str]): The plane to extrude on.
            Can be one of the strings "XY", "YZ", "ZX", "XZ", "YX", "ZY".

        sketch (Sketch): The sketch to extrude.
        amount (float): The amount of extrusion. Can also be a tuple of two floats to extrude between two planes with the given offsets.
        center (CenterDefinitionType, optional): Whether to center the extrusion at the plane. 
            If False, the extrusion will start from the plane.
            If True, the extrusion will be centered at the plane. 
            If amount is a tuple, this parameter is ignored. 
            Defaults to False.

    Returns:
        Body: The extruded body.

    Remarks:
        The planes are defined as follows. Directions refer to
        the global directions.
       
        +-----------+-------+-------+-------+
        | Plane     | xDir  | yDir  | zDir  |
        +===========+=======+=======+=======+
        | XY        | +x    | +y    | +z    |
        +-----------+-------+-------+-------+
        | YZ        | +y    | +z    | +x    |
        +-----------+-------+-------+-------+
        | ZX        | +z    | +x    | +y    |
        +-----------+-------+-------+-------+
        | XZ        | +x    | +z    | -y    |
        +-----------+-------+-------+-------+
        | YX        | +y    | +x    | -z    |
        +-----------+-------+-------+-------+
        | ZY        | +z    | +y    | -x    |
        +-----------+-------+-------+-------+   

        Please note that the "XZ" plane has its normal in negative y direction.

        To avoid confusion, it is recommended to use the 
        :meth:`make_extrude_x`, :meth:`make_extrude_y` or :meth:`make_extrude_z` functions     
    """
    if isinstance(plane, ConstructionPlane):
        wp = plane.cq()
    elif isinstance(plane, str):
        wp = cq.Workplane(plane)
    elif isinstance(plane, cq.Workplane):
        wp = plane
    else:
        raise ValueError("Invalid plane parameter type")

    dim = get_dimension(amount, center)

    if abs(dim.min) > 1e-6:
        # introduce construction plane and extrude from there
        wp = wp.workplane(offset=dim.min)

    extr = wp.placeSketch(sketch.cq()).extrude(dim.size, False)
    return Body(extr)


def make_extrude_x(sketch: Sketch,
                   amount: DimensionDefinitionType,
                   center: bool = False
                   ) -> 'Body':
    """
    Create an extrusion from a sketch at the origin in the x direction.
    The x direction of the sketch will be aligned with the global y direction.
    The y direction of the sketch will be aligned with the global z direction.

    Args:
        sketch (Sketch): The sketch to extrude.
        amount (float): The amount of extrusion in positive x direction (global coordinates).
                Can also be a tuple of two floats to extrude between two planes with the given offsets.
        center (CenterDefinitionType, optional): Whether to center the extrusion at the orogin. 
            If False, the extrusion will start from the origin.
            If True, the extrusion will be centered at the origin. 
            If amount is a tuple, this parameter is ignored. Defaults to False.

    Returns:
        Body: The extruded body.
    """
    plane = ConstructionPlane(cq.Workplane("YZ"))
    return make_extrude(plane, sketch, amount, center)


def make_extrude_y(sketch: Sketch,
                   amount: DimensionDefinitionType,
                   center: bool = False
                   ) -> 'Body':
    """
    Create an extrusion from a sketch at the origin in the y direction.
    The x direction of the sketch will be aligned with the global x direction.
    The y direction of the sketch will be aligned with the global z direction.

    Args:
        sketch (Sketch): The sketch to extrude.
        amount (float): The amount of extrusion in positive y direction (global coordinates).
                Can also be a tuple of two floats to extrude between two planes with the given offsets.
        center (CenterDefinitionType, optional): Whether to center the extrusion at the orogin. 
            If False, the extrusion will start from the origin.
            If True, the extrusion will be centered at the origin. 
            If amount is a tuple, this parameter is ignored. Defaults to False.

    Returns:
        Body: The extruded body.

    Remarks:
        Please note that this function does not do the same as using :meth:`make_extrude` 
        with "XZ" as the plane parameter.
        The "XZ" plane has its normal in negative y direction, while this function uses
        global coordinates and extrudes in positive y direction therefore.
    """
    # special case for y extrusion:
    # the plane "XZ" has its normal in negative y direction,
    # but we want to extrude in positive y direction (global coordinates)
    # so we use the "XZ" plane and mirror the result
    plane = ConstructionPlane(cq.Workplane("XZ"))
    return make_extrude(plane, sketch, amount, center).mirror("Y", copy_and_merge=False)


def make_extrude_z(sketch: Sketch,
                   amount: DimensionDefinitionType,
                   center: bool = False
                   ) -> 'Body':
    """
    Create an extrusion from a sketch at the origin in the z direction.
    The x direction of the sketch will be aligned with the global x direction.
    The y direction of the sketch will be aligned with the global y direction.

    Args:
        sketch (Sketch): The sketch to extrude.
        amount (float): The amount of extrusion in positive z direction (global coordinates).
                Can also be a tuple of two floats to extrude between two planes with the given offsets.
        center (CenterDefinitionType, optional): Whether to center the extrusion at the orogin. 
            If False, the extrusion will start from the origin.
            If True, the extrusion will be centered at the origin. 
            If amount is a tuple, this parameter is ignored. Defaults to False.

    Returns:
        Body: The extruded body.
    """
    plane = ConstructionPlane(cq.Workplane("XY"))
    return make_extrude(plane, sketch, amount, center)


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
        center (CenterDefinitionType, optional): Whether to center the text object at the origin.
            If False, the text will start from the origin.
            Can also be "X", "Y" or "Z" to center in only one direction or "XY", "XZ", "YZ" to center in two directions.
            Defaults to True which centers the text object in all directions.
        font (str, optional): The font of the text. Defaults to "Arial".

    Returns:
        Body: The 3D text object.
    """
    c = cq.Compound.makeText(text, size, height, font=font)
    body = Body(cq.Workplane(obj=c))
    return body.move_to_origin().center(center)


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
