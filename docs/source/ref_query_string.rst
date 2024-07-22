
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

The following query bits are supported:

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
       same position) in that list (first in the list has index 0).
   * - <<[]
     - <<Y[2]
     - The search string "<<Y" sorts all vertices in negative Y direction.\ 
       Returns the third vertex (or list of vertices with the same position)\ 
       in that list.
   * - or
     - >Y or <Y
     - Vertices farthest in the positive or negative y dir
   * - and
     - >Y and <X
     - Vertices farthest in the positive y dir and negative x dir
   * - not
     - not >Y
     - All vertices but farthest in the positive y dir  



.. _query_edges:

Selecting Edges
---------------


The following methods allow you to edges of a body based on a query string. 

.. hlist::

    * :py:meth:`Body.chamfer` 
    * :py:meth:`Body.fillet` 

The following query bits are supported:



.. list-table:: 
   :header-rows: 1

   * - Query
     - Example
     - Selects
   * - \* 
     - \*
     - Selects all edges
   * - ALL
     - ALL
     - Selects all edges
   * - \+
     - \+Z
     - Edges aligned in the z direction
   * - \|
     - \|Z
     - Edges parallel to z direction
   * - #
     - #Z
     - Edges perpendicular to z direction
   * - >
     - >Y
     - Edges farthest in positive y direction
   * - <
     - <Y
     - Edges closest in positive y direction
   * - >>[]
     - >>Y[1]
     - The search string ">>Y" sorts all edges in positive Y direction.\ 
       The "[1]" selects the second edge (or list of edges with the\ 
       same position) in that list (first in the list has index 0).
   * - <<[]
     - <<Y[0]
     - The search string "<<Y" sorts all edges in negative Y direction.\ 
       The "[0]" selects the first edge (or list of edges with the\ 
       same position) in that list.
   * - >[]
     - >Y[1]
     - Sorts all **parallel** edges in the positive y direction, gets the second one.
   * - <[]
     - <Y[2]
     - Sorts all **parallel** edges in the negative y direction, gets the third one.
   * - or
     - >Y or <Y
     - Edges farthest in the positive or negative y dir
   * - and
     - >Y and <X
     - Edges farthest in the positive y dir and negative x dir
   * - not
     - not >Y
     - All edges but the farthest in the positive y dir  



.. _query_faces:

Selecting Faces
---------------


The following methods allow you to select faces of a body based on a query string. 

.. hlist::

    * :py:meth:`Body.make_extrude` 
    * :py:meth:`Body.add_extrude` 
    * :py:meth:`Body.cut_extrude` 

The following query bits are supported:



.. list-table:: 
   :header-rows: 1

   * - Query
     - Example
     - Selects
   * - \+
     - \+Z
     - Faces with normal in positive z direction
   * - \|
     - \|Z
     - Faces with normal in positive or negative z direction
   * - #
     - #Z
     - Faces with normal perpendicular to z direction
   * - >
     - >Y
     - Face farthest in positive y direction
   * - <
     - <Y
     - Face closest in positive y direction
   * - >>[]
     - >>Y[1]
     - The search string ">>Y" sorts all faces in positive Y direction.\ 
       The "[1]" selects the second face in that list (first in the list has index 0).
   * - <<[]
     - <<Y[0]
     - The search string "<<Y" sorts all faces in negative Y direction.\ 
       The "[0]" selects the first face in that list.
   * - or
     - >Y or <Y
     - Faces farthest in the positive or negative y dir
   * - and
     - >Y and +Y
     - Faces farthest in the positive y dir and normal in positive y dir
   * - not
     - not >Y
     - All faces but the farthest in the positive y dir  