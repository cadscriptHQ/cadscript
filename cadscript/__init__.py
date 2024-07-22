# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path
import tempfile
import time
import inspect
from typing import Literal, Optional, Union

import cadquery as cq
from .typedefs import AxisType, DimensionDefinitionType, CenterDefinitionType

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
                 *,
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
                   *,
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
    return make_extrude(plane, sketch, amount, center=center)


def make_extrude_y(sketch: Sketch,
                   amount: DimensionDefinitionType,
                   *,
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
    return make_extrude(plane, sketch, amount, center=center).mirror("Y", copy_and_merge=False)


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
    return make_extrude(plane, sketch, amount, center=center)


def make_revolve(axis: AxisType,
                 sketch: Sketch,
                 *,
                 angle: DimensionDefinitionType = 360,
                 start_axis: Optional[Literal["X", "Y", "Z", "+X", "+Y", "+Z", "-X", "-Y", "-Z"]] = None
                 ) -> 'Body':
    """
    Create a revolved body from a sketch.

    Args:
        axis (AxisType): The axis of revolution. Can be one of "X", "Y" or "Z".
        sketch (Sketch): The sketch to revolve.
        angle (float, optional): The angle of revolution in degrees.
            Can also be a tuple of two floats to revolve between two angles.
            Defaults to 360.
            Revolution will be counter-clockwise around the axis of revolution (right-hand rule with axis in 
            positive direction),  starting from the start axis.
        start_axis (str, optional): The start axis of the revolution. Doesn't have an effect if angle is 360.
            Can be one of "X", "Y", "Z", "+X", "+Y", "+Z", "-X", "-Y", "-Z". "X" and "+X" are equivalent, 
            describing the global x axis in positive direction. "-X" describes the global x axis in negative 
            direction. The same applies to "Y" and "Z".
            If not specified, the start axis will be "+Y" for the "X" axis, "+Z" for the "Y" axis and 
            "+X" for the "Z" axis.


    Returns:
        Body: The revolved body.
    """

    if axis == "X":
        axis_vec = cq.Vector(1, 0, 0)
        start_axis = start_axis or "+Y"
        start_axis_vec = __get_revolve_start_axis(start_axis, axis)
    elif axis == "Y":
        axis_vec = cq.Vector(0, 1, 0)
        start_axis = start_axis or "+Z"
        start_axis_vec = __get_revolve_start_axis(start_axis, axis)
    elif axis == "Z":
        axis_vec = cq.Vector(0, 0, 1)
        start_axis = start_axis or "+X"
        start_axis_vec = __get_revolve_start_axis(start_axis, axis)
    else:
        raise ValueError("Invalid axis parameter")

    # we lay the sketch on a plane with rotation axis (axis_vec) up, and start axis to the right (start_axis_vec)
    # Plane objects are defined by origin, xDir and normal, so we need to calculate the normal
    normal = start_axis_vec.cross(axis_vec)
    plane = cq.Plane(origin=cq.Vector(0, 0, 0), xDir=start_axis_vec, normal=normal)
    if isinstance(angle, tuple):
        # rotate the plane to the start angle
        plane = plane.rotated(cq.Vector(0, angle[0], 0))
        angle = angle[1] - angle[0]
    wp = cq.Workplane(plane)
    # revolve around the sketch y axis (up)
    revolve = wp.placeSketch(sketch.cq()).revolve(axisStart=cq.Vector(0, 0, 0), axisEnd=cq.Vector(0, 1, 0), angleDegrees=angle)
    return Body(revolve)


def __get_revolve_start_axis(start_axis, axis):
    vec = None
    if start_axis == "X" or start_axis == "+X":
        vec = cq.Vector(1, 0, 0)
    elif start_axis == "-X":
        vec = cq.Vector(-1, 0, 0)
    elif start_axis == "Y" or start_axis == "+Y":
        vec = cq.Vector(0, 1, 0)
    elif start_axis == "-Y":
        vec = cq.Vector(0, -1, 0)
    elif start_axis == "Z" or start_axis == "+Z":
        vec = cq.Vector(0, 0, 1)
    elif start_axis == "-Z":
        vec = cq.Vector(0, 0, -1)
    if vec is None:
        raise ValueError("Invalid start start_axis")
    if str(axis) in str(start_axis):
        raise ValueError("Start axis must be perpendicular to the revolution axis")
    return vec


def make_loft(plane1: Union[ConstructionPlane, str],
              sketch1: Sketch,
              plane2: Union[ConstructionPlane, str],
              sketch2: Sketch,
              ) -> 'Body':
    """
    Create a loft between two sketches.

    Args:
        plane1 (Union[ConstructionPlane,str]): The plane of the first sketch.
            Can be one of the strings "XY", "YZ", "ZX", "XZ", "YX", "ZY".
        sketch1 (Sketch): The first sketch.
        plane2 (Union[ConstructionPlane,str]): The plane of the second sketch.
            Can be one of the strings "XY", "YZ", "ZX", "XZ", "YX", "ZY".
        sketch2 (Sketch): The second sketch.

    Returns:
        Body: The lofted body.

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
    """
    if isinstance(plane1, ConstructionPlane):
        wp1 = plane1.cq()
    elif isinstance(plane1, str):
        wp1 = cq.Workplane(plane1)
    elif isinstance(plane1, cq.Workplane):
        wp1 = plane1
    else:
        raise ValueError("Invalid plane parameter type")

    if isinstance(plane2, ConstructionPlane):
        wp2 = plane2.cq()
    elif isinstance(plane2, str):
        wp2 = cq.Workplane(plane2)
    elif isinstance(plane2, cq.Workplane):
        wp2 = plane2
    else:
        raise ValueError("Invalid plane parameter type")

    e1 = wp1.placeSketch(sketch1.cq())
    e2 = wp2.placeSketch(sketch2.cq())

    loft = cq.Workplane().add(e1).add(e2).toPending().loft(ruled=False)
    return Body(loft)



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
