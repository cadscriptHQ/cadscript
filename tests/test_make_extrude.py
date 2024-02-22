# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

import unittest
import cadscript


class MakeExtrudeTest(unittest.TestCase):
    epsilon = 1e-5

    def assertExtentEqualX(self, extent, xmin, xmax):
        self.assertAlmostEqual(extent.min_x, xmin, delta=self.epsilon, msg="min_x different")
        self.assertAlmostEqual(extent.max_x, xmax, delta=self.epsilon, msg="max_x different")

    def assertExtentEqualY(self, extent, ymin, ymax):
        self.assertAlmostEqual(extent.min_y, ymin, delta=self.epsilon, msg="min_y different")
        self.assertAlmostEqual(extent.max_y, ymax, delta=self.epsilon, msg="max_y different")

    def assertExtentEqualZ(self, extent, zmin, zmax):
        self.assertAlmostEqual(extent.min_z, zmin, delta=self.epsilon, msg="min_z different")
        self.assertAlmostEqual(extent.max_z, zmax, delta=self.epsilon, msg="max_z different")

    def test_make_extrude_x(self):
        size1 = 2
        size2 = 1
        amount = 4
        sketch = cadscript.make_sketch().add_rect(size1, size2, center=False)
        body = cadscript.make_extrude_x(sketch, amount)
        dim = body.get_extent()
        self.assertExtentEqualX(dim, 0, amount)
        self.assertExtentEqualY(dim, 0, size1)
        self.assertExtentEqualZ(dim, 0, size2)

    def test_make_extrude_x_centered(self):
        size1 = 2
        size2 = 1
        amount = 4
        sketch = cadscript.make_sketch().add_rect(size1, size2, center=False)
        body = cadscript.make_extrude_x(sketch, amount, center=True)
        dim = body.get_extent()
        self.assertExtentEqualX(dim, -amount / 2, amount / 2)
        self.assertExtentEqualY(dim, 0, size1)
        self.assertExtentEqualZ(dim, 0, size2)

    def test_make_extrude_y(self):
        size1 = 2
        size2 = 1
        amount = 4
        sketch = cadscript.make_sketch().add_rect(size1, size2, center=False)
        body = cadscript.make_extrude_y(sketch, amount)
        dim = body.get_extent()
        self.assertExtentEqualX(dim, 0, size1)
        self.assertExtentEqualY(dim, 0, amount)
        self.assertExtentEqualZ(dim, 0, size2)

    def test_make_extrude_y_centered(self):
        size1 = 2
        size2 = 1
        amount = 4
        sketch = cadscript.make_sketch().add_rect(size1, size2, center=False)
        body = cadscript.make_extrude_y(sketch, amount, center=True)
        dim = body.get_extent()
        self.assertExtentEqualX(dim, 0, size1)
        self.assertExtentEqualY(dim, -amount / 2, amount / 2)
        self.assertExtentEqualZ(dim, 0, size2)

    def test_make_extrude_z(self):
        size1 = 2
        size2 = 1
        amount = 4
        sketch = cadscript.make_sketch().add_rect(size1, size2, center=False)
        body = cadscript.make_extrude_z(sketch, amount)
        dim = body.get_extent()
        self.assertExtentEqualX(dim, 0, size1)
        self.assertExtentEqualY(dim, 0, size2)
        self.assertExtentEqualZ(dim, 0, amount)

    def test_make_extrude_z_centered(self):
        size1 = 2
        size2 = 1
        amount = 4
        sketch = cadscript.make_sketch().add_rect(size1, size2, center=False)
        body = cadscript.make_extrude_z(sketch, amount, center=True)
        dim = body.get_extent()
        self.assertExtentEqualX(dim, 0, size1)
        self.assertExtentEqualY(dim, 0, size2)
        self.assertExtentEqualZ(dim, -amount / 2, amount / 2)

    def test_make_extrude_x_minmax(self):
        size1 = 2
        size2 = 1
        amount = (-1, 3)
        sketch = cadscript.make_sketch().add_rect(size1, size2, center=False)
        body = cadscript.make_extrude_x(sketch, amount)
        dim = body.get_extent()
        self.assertExtentEqualX(dim, amount[0], amount[1])
        self.assertExtentEqualY(dim, 0, size1)
        self.assertExtentEqualZ(dim, 0, size2)

    def test_make_extrude_y_minmax(self):
        size1 = 2
        size2 = 1
        amount = (-1, 3)
        sketch = cadscript.make_sketch().add_rect(size1, size2, center=False)
        body = cadscript.make_extrude_y(sketch, amount)
        dim = body.get_extent()
        self.assertExtentEqualX(dim, 0, size1)
        self.assertExtentEqualY(dim, amount[0], amount[1])
        self.assertExtentEqualZ(dim, 0, size2)

    def test_make_extrude_z_minmax(self):
        size1 = 2
        size2 = 1
        amount = (-1, 3)
        sketch = cadscript.make_sketch().add_rect(size1, size2, center=False)
        body = cadscript.make_extrude_z(sketch, amount)
        dim = body.get_extent()
        self.assertExtentEqualX(dim, 0, size1)
        self.assertExtentEqualY(dim, 0, size2)
        self.assertExtentEqualZ(dim, amount[0], amount[1])

    def test_make_extrude_xy(self):
        size1 = 2
        size2 = 1
        amount = 4
        sketch = cadscript.make_sketch().add_rect(size1, size2, center=False)
        body = cadscript.make_extrude("XY", sketch, amount)
        dim = body.get_extent()
        self.assertExtentEqualX(dim, 0, size1)
        self.assertExtentEqualY(dim, 0, size2)
        self.assertExtentEqualZ(dim, 0, amount)

    def test_make_extrude_xz(self):
        size1 = 2
        size2 = 1
        amount = 4
        sketch = cadscript.make_sketch().add_rect(size1, size2, center=False)
        body = cadscript.make_extrude("XZ", sketch, amount)
        dim = body.get_extent()
        self.assertExtentEqualX(dim, 0, size1)
        self.assertExtentEqualY(dim, -amount, 0)
        self.assertExtentEqualZ(dim, 0, size2)

    def test_make_extrude_yz(self):
        size1 = 2
        size2 = 1
        amount = 4
        sketch = cadscript.make_sketch().add_rect(size1, size2, center=False)
        body = cadscript.make_extrude("YZ", sketch, amount)
        dim = body.get_extent()
        self.assertExtentEqualX(dim, 0, amount)
        self.assertExtentEqualY(dim, 0, size1)
        self.assertExtentEqualZ(dim, 0, size2)

    def test_make_extrude_xy_centered(self):
        size1 = 2
        size2 = 1
        amount = 4
        sketch = cadscript.make_sketch().add_rect(size1, size2, center=False)
        body = cadscript.make_extrude("XY", sketch, amount, center=True)
        dim = body.get_extent()
        self.assertExtentEqualX(dim, 0, size1)
        self.assertExtentEqualY(dim, 0, size2)
        self.assertExtentEqualZ(dim, -amount / 2, amount / 2)

    def test_make_extrude_xy_constructionplane_centered(self):
        size1 = 2
        size2 = 1
        amount = 4
        plane_offset = 10
        sketch = cadscript.make_sketch().add_rect(size1, size2, center=False)
        plane = cadscript.make_construction_plane("XY", plane_offset)
        body = cadscript.make_extrude(plane, sketch, amount, center=True)
        dim = body.get_extent()
        self.assertExtentEqualX(dim, 0, size1)
        self.assertExtentEqualY(dim, 0, size2)
        self.assertExtentEqualZ(dim, plane_offset - amount / 2, plane_offset + amount / 2)


if __name__ == '__main__':
    unittest.main()
