# Cadscript

A Python module for creating 3D models with scripts.

## What is Cadscript?

Cadscript is a Python module that allows you to write simple scripts that produce 3D CAD models. Using scripting, you can easily describe parametric 3D models, that can be customized without additional effort. Scripting also allows non-UI workflows, Cadscript can e.g. be integrated into automated build pipelines. Cadscript can produce STL files (e.g. for 3D printing) and STEP files (high-quality CAD format) that can be used in traditional CAD packages.

Cadscript is based on [CadQuery](https://github.com/CadQuery/cadquery/), a Python module that wraps [Open CASCADE](https://en.wikipedia.org/wiki/Open_Cascade_Technology), a powerful CAD kernel, that is also the basis for [FreeCAD](https://www.freecad.org/).

## Status

Cadscript is still in development. Version 1.0 will be the first release. Until then expect API changes to happen without prior annoucements. If you want to make sure your scripts don't break, use a specific version, e.g. 0.2.

## Why Cadscript?

Using Python, you have a simple, yet powerful scripting language. With Cadscript you can leverage these capabilities and commbine them with the powerful Open Cascade technology - and all that without making it complicated.

### Why not CadQuery?

CadQuery already is a Python module wrapping the Open Cascade kernel. It is a very feature-rich module, making most of the many Open Cascade functionalities available to the Python programmer. But in our feeling, it still is a bit to complex. If you are new to CadQuery it is bit hard to find your way around. We were looking for something simpler, a bit like [OpenSCAD](http://openscad.org/).

### Why not OpenSCAD?

[OpenSCAD](http://openscad.org/) is another project that allows the creation of 3D models using scripts. It provides a simple way to do that using [CSG modelling](https://de.wikipedia.org/wiki/Constructive_Solid_Geometry). It is quite popular for creating parametric models in the 3D printing community, but I lacks some important features: It cannot perform some standard operations available in common CAD packages (like chamfer and fillet) and it cannot import or export STEP files. Moreover, OpenSACD uses its own programming language und you cannot just use a language you already know.

## Installation

Cadscript is based on CadQuery, so the first step is to get CadQuery running. Please refer to their [installation guide](https://cadquery.readthedocs.io/en/latest/installation.html).

After that install the cadscript module using pip:

```
pip install cadscript
```

## License

Cadscript is licensed under the terms of the [Apache Public License, version 2.0](http://www.apache.org/licenses/LICENSE-2.0).

(C) 2023 Andreas Kahler


