# Changelog

## [0.5] - work in progress

- make_box(): center param accessible as named param only
- make_text(): added center param, center as default
- added add_ellipse and cut_ellipse()
- added angle param to add/cut_rect()
- added add/cut_slot variant with 2 points
- added add/cut/intersect_sketch()
- added make_sphere() and make_cylinder()
- added Body.cut_hole()
- added Body.move_to_origin() Body.center() and Body.mirror()
- added Sketch.move_to_origin() Sketch.center() and Sketch.mirror()
- added pattern_distribute()

## [0.4] - 2024-01-12

- new method: Body.intersect
- renamed Body.fuse() to Body.add()
- reordered params of cadscript.make_extrude, allowed passing of tuple for amount
- removed method Sketch.finalize()
- vertex selector support for Sketch.fillet() and Sketch.chamfer(). Also allow passing point(s)

## [0.3] - 2024-01-03

- Refactoring; API cleanup 

## [0.2] - 2023-11-26

- Initial version on github

