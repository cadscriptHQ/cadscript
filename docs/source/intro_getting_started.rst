.. _examples:

.. currentmodule:: cadscript

Getting Started
===============


First Example
-------------

Let's start with a simple box:


.. cadscript:: 
    :source: ../examples/getting_started.py
    :steps: 1

    

Now we fillet the corners. We choose the edges with the first argument for :py:meth:`Body.fillet` method. 
``"|Z"`` selects all edges parallel to Z axis. 
The second argument is the radius of the fillet.

.. cadscript:: 
    :source: ../examples/getting_started.py
    :steps: 1-2


Next we add a little chamfer to the top and bottom edges. Again, the first argument selects the edges to work on. 
``"#Z"`` selects all edges perpendicular to Z axis, that is, parallel to the XY plane.

.. cadscript:: 
    :source: ../examples/getting_started.py
    :steps: 1-3

We continue by creating a sketch and drawing a heart. We start with a square.

.. cadscript:: 
    :source: ../examples/getting_started.py
    :steps: 4
    :select: sketch


Then we add two circles at the center of two of the sides. The operation is a Boolean union, so the circles are merged with the square.

.. cadscript:: 
    :source: ../examples/getting_started.py
    :steps: 4-5
    :select: sketch

Finally, we place the sketch on the top face of our object, rotate it 45 degrees, and use it to cut a hole by extruding it down (negative value).

.. cadscript:: 
    :source: ../examples/getting_started.py

.. topic:: Api References

    .. hlist::

        * :py:meth:`cadscript.make_box` 
        * :py:meth:`Body.fillet` 
        * :py:meth:`Body.chamfer` 
        * :py:meth:`cadscript.make_sketch`    
        * :py:meth:`Sketch.add_circle` 
        * :py:meth:`Sketch.add_rect` 
        * :py:meth:`Body.cut_extrude` 


Second Example
--------------


.. cadscript:: 
    :source: ../examples/bracket.py
    :steps: 1-2
    :text_from_comment:
    :select: sketch1

.. cadscript:: 
    :source: ../examples/bracket.py
    :steps: 1-3
    :text_from_comment:
    :select: sketch1

.. cadscript:: 
    :source: ../examples/bracket.py
    :steps: 1-4
    :text_from_comment:
    :select: sketch1
    
.. cadscript:: 
    :source: ../examples/bracket.py
    :steps: 1-5
    :text_from_comment:
    :select: sketch1    

.. cadscript:: 
    :source: ../examples/bracket.py
    :steps: 1-6
    :text_from_comment:
    :select: sketch1    

.. cadscript:: 
    :source: ../examples/bracket.py
    :steps: 1-7
    :text_from_comment:
    :select: sketch1    