[![Unit Tests](https://github.com/cadscriptHQ/cadscript/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/cadscriptHQ/cadscript/actions/workflows/python-package.yml)
[![Docs](https://readthedocs.org/projects/cadscript/badge/?version=latest)](https://cadscript.readthedocs.io/en/latest/?badge=latest)

# Cadscript

A Python module for creating 3D models with scripts.

**Quicklinks: [Getting Started](https://cadscript.readthedocs.io/en/latest/intro_getting_started.html) -  [Installation](https://cadscript.readthedocs.io/en/latest/intro_installation.html) - [Documentation](https://cadscript.readthedocs.io/)**

## What is Cadscript?

Cadscript is a Python module that allows you to write simple scripts that produce 3D CAD models. Using scripting, you can easily describe parametric 3D models, that can be customized without additional effort. Scripting also allows non-UI workflows, Cadscript can e.g. be integrated into automated build pipelines. Cadscript can produce STL files (e.g. for 3D printing) and STEP files (high-quality CAD format) that can be used in traditional CAD packages.

Cadscript is based on [CadQuery](https://github.com/CadQuery/cadquery/), a Python module that wraps [Open CASCADE](https://en.wikipedia.org/wiki/Open_Cascade_Technology), a powerful CAD kernel, that is also the basis for [FreeCAD](https://www.freecad.org/).

## Status

Cadscript is still in development. Version 1.0 will be the first release. Until then expect API changes to happen without prior annoucements. If you want to make sure your scripts don't break, use a specific version, e.g. 0.5.

## Why Cadscript?

Using Python, you have a simple, yet powerful scripting language. With Cadscript you can leverage these capabilities and commbine them with the powerful Open Cascade technology - and all that without making it complicated.

### Why not CadQuery?

CadQuery already is a Python module wrapping the Open Cascade kernel. It is a very feature-rich module, making most of the many Open Cascade functionalities available to the Python programmer. But in our feeling, it still is a bit too complex. If you are new to CadQuery it is bit hard to find your way around. We were looking for something simpler, a bit like [OpenSCAD](http://openscad.org/).

### Why not OpenSCAD?

[OpenSCAD](http://openscad.org/) is another project that allows the creation of 3D models using scripts. It provides a simple way to do that using [CSG modelling](https://de.wikipedia.org/wiki/Constructive_Solid_Geometry). It is quite popular for creating parametric models in the 3D printing community, but I lacks some important features: It cannot perform some standard operations available in common CAD packages (like chamfer and fillet) and it cannot import or export STEP files. Moreover, OpenSACD uses its own programming language und you cannot just use a language you already know.

## Installation

Cadscript is based on CadQuery, so the first step is to get CadQuery running. Please refer to their [installation guide](https://cadquery.readthedocs.io/en/latest/installation.html).

After that install the cadscript module using pip:

```
pip install cadscript
```

More details see the [installation section in the documentation](https://cadscript.readthedocs.io/en/latest/intro_installation.html)

## Modelling Workflow

The Cadscript modelling workflow is based on [Bodies](https://cadscript.readthedocs.io/en/latest/ref_body.html) and [Sketches](https://cadscript.readthedocs.io/en/latest/ref_sketch.html). Usually you start by creating a Sketch (a 2D drawing) and turn that into a Body (a 3D object) e.g. by extrusion. You can also place Sketches on faces of Bodies and add additional features to Bodies this way, e.g. by adding an extrusion or by extruding inwards to create a hole. Cadscript also supports [Boolean operations](https://en.wikipedia.org/wiki/Boolean_operations_on_polygons) on Sketches and Bodies.

For more details consult the [documentation](https://cadscript.readthedocs.io/).

## Features and Roadmap

* Sketches are built using Boolean operations from primitives (rect, circle, slots, polygons)
* Fillet and chamfer on Sketches
* Extrusion of sketches
* Boolean operations on Bodies
* Fillet and chamfer on Body edges
* 3D text objects from system fonts
* Import: DXF, STEP
* Export: DFX, SVG (Sketches), SVG (3D rendering), STEP, STL
* Compatibility with CadQuery
* CQ-Editor integration
* Construction planes (TODO, planned for version 1.0)
* Revolve and loft operation (TODO, planned for version 1.0)
* Assemblies (TODO, planned for version 1.0)
* OpenSCAD to Cadscript conversion utility (TODO, planned for version 1.5)

## API Design

Cadscript follows the following API design guidelines

* **Understandability over compactness** - Ensure the API is easy to comprehend, especially for programmers new to the library, instead of striving for overly compact code.
* **Accessibility over sophistication** - When choosing between two methods to implement a feature, opt for the one that a less experienced programmer would understand more easily.
* **Simplicity over feature richness** - Keep the API small, consistent, and easy to understand, prioritizing it over adding an extensive range of features to avoid "feature creep."
* **Specialization over generalization** - Focus on supporting the preferred way of designing 3D models excellently, rather than attempting to cater to a wide array of different styles.

But even with this focus on simplicity, Cadscript wants to be a general-purpose tool for programmatic 3D modelling. This is archived by

* **Complete 3D Modelling API**: Although simple, the Cadscript API includes everything you need for modelling complex parts
* **Compatibitly with CadQuery**: Internally Cadscript uses Cadquery for all operations. Therefore you can easily use the generated geometry with CadQuery functionality or use CadQuery tools like CQ-Editor for developing with Cadscript.

## License

Cadscript is licensed under the terms of the [Apache Public License, version 2.0](http://www.apache.org/licenses/LICENSE-2.0).

(C) 2023-2024 Andreas Kahler


