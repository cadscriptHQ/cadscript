
.. currentmodule:: cadscript

Selecting objects with query strings
====================================


.. _query_vertices:

Selecting Vertices
------------------


The following methods allow you to select points (aka vertices) in a sketch based on a query string. 

.. hlist::

    * :py:meth:`Sketch.chamfer` 
    * :py:meth:`Sketch.fillet` 

The following query strings are supported:

.. list-table:: 
   :header-rows: 1

   * - Query 
     - Example
     - Selects
   * - \* 
     - \*
     - Selects all vertices
   * - ALL
     - ALL
     - Selects all vertices
   * - >
     - >Y
     - Vertices farthest in the positive y dir
   * - <
     - <Y
     - Vertices farthest in the negative y dir
   * - >>[]
     - >>X[1]
     - The search string ">>X" sorts all vertices in positive X direction.\ 
       The "[1]" selects the second vertex (or list of vertices with the\ 
       same distance) in that list (first in the list has index 0).
   * - <<[]
     - <<Y[2]
     - The search string "<<Y" sorts all vertices in nagative Y direction.\ 
       Returns the third vertex (or list of vertices with the same distance)\ 
       in that list.
   * - or
     - >Y or <Y
     - Vertices farthest in the positive or negative y dir
   * - and
     - >Y and <X
     - Vertices farthest in the positive y dir and negative x dir
   * - not
     - not >Y
     - Vertices not farthest in the positive y dir  





