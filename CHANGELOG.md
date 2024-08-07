# Changelog



## [0.5.3] - 2024-07-10

- FIX: dxf export results in error with newer cadquery versions #12
- FIX: introduced dependency to numpy<2, as current cadquery version (2.4, dev) is incompatible with new numpy 2.0 #13

## [0.5.2] - 2024-02-22

- new functions make_extrude_x(), make_extrude_y(), and make_extrude_z()
- new param center for make_extrude(), bug fixes

## [0.5.1] - 2024-02-20

- fix in Interval1D.max
- added move() methods in interval classes

## [0.5] - 2024-02-15

- make_box(): center param accessible as named param only
- make_text(): added center param, center as default
- added add_ellipse and cut_ellipse()
- added angle param to add/cut_rect()
- added add/cut_slot variant with 2 points
- added add/cut/intersect_sketch()
- added make_sphere() and make_cylinder()
- added Body.cut_hole()
- added Body.move_to_origin(), Body.center() and Body.mirror()
- added Sketch.move_to_origin(), Sketch.center() and Sketch.mirror()
- added pattern_distribute() and pattern_distribute_stretch()
- breaking change: Sketch.add_polygon() has now parameter auto_close which is True by default
- introduced Interval1D, Interval2D, Interval3D

## [0.4] - 2024-01-12

- new method: Body.intersect()
- renamed Body.fuse() to Body.add()
- reordered params of cadscript.make_extrude, allowed passing of tuple for amount
- removed method Sketch.finalize()
- vertex selector support for Sketch.fillet() and Sketch.chamfer(). Also allow passing point(s)

## [0.3] - 2024-01-03

- Refactoring; API cleanup 

## [0.2] - 2023-11-26

- Initial version on github

