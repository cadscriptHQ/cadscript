.. _examples:

.. currentmodule:: cadscript

Getting Started
===============


First Example
-------------

Let's start with a simple box:


.. cadscript:: 

    result = cadscript.make_box(30, 20, 4)


Now we fillet the corners. We choose the edges with the first argument for fillet() method. "|Z" selects all edges parallel to Z axis. 
The second argument is the radius of the fillet.

.. cadscript:: 

    result = cadscript.make_box(30, 20, 4)
    result.fillet("|Z", 3)


Next we add a little chamfer to the top and bottom edges. Again, the first argument selects the edges to work on. 
"#Z" selects all edges perpendicular to Z axis, that is, parallel to the XY plane.

.. cadscript:: 

    result = cadscript.make_box(30, 20, 4)
    result.fillet("|Z", 3)
    result.chamfer("#Z", 0.6)

We continue by creating a sketch and drawing a heart. We start with a square.

.. cadscript:: 
    :select: sketch

    sketch = cadscript.make_sketch()
    sketch.add_rect(10, 10)

Then we add two circles at the center of two of the sides. The operation is a Boolean union, so the circles are merged with the square.

.. cadscript:: 
    :select: sketch

    sketch = cadscript.make_sketch()
    sketch.add_rect(8, 8)
    sketch.add_circle(diameter=10, positions=[(4, 0), (0, 4)])

Finally, we place the sketch on the top face of our object, rotate it 45 degrees, and use it to cut a hole by extruding it down (negative value).

.. cadscript:: 

    result = cadscript.make_box(30, 20, 4)
    result.fillet("|Z", 3)
    result.chamfer("#Z", 0.6)

    sketch = cadscript.make_sketch()
    sketch.add_rect(10, 10)
    sketch.add_circle(diameter=10, positions=[(5, 0), (0, 5)])
    
    result.cut_extrude(">Z", sketch.rotate(45), -4)

.. topic:: Api References

    .. hlist::

        * :py:meth:`cadscript.make_box` 
        * :py:meth:`CadObject.fillet` 
        * :py:meth:`CadObject.chamfer` 
        * :py:meth:`cadscript.make_sketch` 
        * :py:meth:`SketchObject.add_circle` 
        * :py:meth:`SketchObject.add_rect` 
        * :py:meth:`CadObject.cut_extrude` 
