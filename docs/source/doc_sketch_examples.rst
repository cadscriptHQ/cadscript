.. _examples:

.. currentmodule:: cadscript

Sketching Examples
==================


Rectangles
----------


.. cadscript:: 
    :side-by-side:
    :select: sketch

    # rectangle, width 40, height 20
    # centered
    sketch = cadscript.make_sketch()
    sketch.add_rect(40, 20)


.. cadscript:: 
    :side-by-side:
    :select: sketch

    # rectangle, width 40, height 20
    # centered only in x
    sketch = cadscript.make_sketch()
    sketch.add_rect(40, 20, center="X")


.. cadscript:: 
    :side-by-side:
    :select: sketch

    # rectangle, width 40, height 20
    # rotated 45 degrees
    sketch = cadscript.make_sketch()
    sketch.add_rect(40, 20, angle=45)



Circles
-------


.. cadscript:: 
    :side-by-side:
    :select: sketch

    # circle, radius 20
    # centered
    sketch = cadscript.make_sketch()
    sketch.add_circle(radius=20)


.. cadscript:: 
    :side-by-side:
    :select: sketch

    # circle, diameter 40
    # positioned at x=20, y=10
    sketch = cadscript.make_sketch()
    sketch.add_circle(d=40, pos=(20, 10))



