.. _examples:

.. currentmodule:: cadscript

Getting Started
===============


Simple Box
----------

Just about the simplest possible example, a rectangular box


.. cadscript:: 
    :as_image:   

    result = cadscript.make_box(30, 20, 4)


Now we fillet the corners. We choose the edges with the first argument for fillet() method. "|Z" selects all edges parallel to Z axis. 
The second argument is the radius of the fillet.

.. cadscript:: 
    :as_image:   

    result = cadscript.make_box(30, 20, 4)
    result.fillet("|Z", 3)


.. topic:: Api References

    .. hlist::
        :columns: 2

        * :py:meth:`cadscript.make_box` 
        * :py:meth:`CadObject.fillet` 