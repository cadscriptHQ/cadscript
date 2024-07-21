# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

import unittest
import cadscript


class MakeRevolveTest(unittest.TestCase):
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

    def test_make_revolve_z(self):
        size1 = 5
        size2 = 10
        sketch = cadscript.make_sketch().add_rect(size1, size2, center=False)
        body = cadscript.make_revolve("Z", sketch)  
        dim = body.get_extent()
        self.assertExtentEqualX(dim, -size1, +size1)
        self.assertExtentEqualY(dim, -size1, +size1)
        self.assertExtentEqualZ(dim, 0, size2)

    def test_make_revolve_x(self):
        size1 = 5
        size2 = 10
        sketch = cadscript.make_sketch().add_rect(size1, size2, center=False)
        body = cadscript.make_revolve("X", sketch)  
        dim = body.get_extent()
        self.assertExtentEqualX(dim, 0, size2)
        self.assertExtentEqualY(dim, -size1, +size1)
        self.assertExtentEqualZ(dim, -size1, +size1)

    def test_make_revolve_y(self):
        size1 = 5
        size2 = 10
        sketch = cadscript.make_sketch().add_rect(size1, size2, center=False)
        body = cadscript.make_revolve("Y", sketch)  
        dim = body.get_extent()
        self.assertExtentEqualX(dim, -size1, +size1)
        self.assertExtentEqualY(dim, 0, size2)
        self.assertExtentEqualZ(dim, -size1, +size1)

    def test_make_revolve_z_90(self):
        size1 = 5
        size2 = 10
        sketch = cadscript.make_sketch().add_rect(size1, size2, center=False)
        body = cadscript.make_revolve("Z", sketch, angle=90)  
        dim = body.get_extent()
        self.assertExtentEqualX(dim, 0, +size1)
        self.assertExtentEqualY(dim, 0, +size1)
        self.assertExtentEqualZ(dim, 0, size2)

    def test_make_revolve_z_90_plusx(self):
        size1 = 5
        size2 = 10
        sketch = cadscript.make_sketch().add_rect(size1, size2, center=False)
        body = cadscript.make_revolve("Z", sketch, angle=90, start_axis="+X")  
        dim = body.get_extent()
        self.assertExtentEqualX(dim, 0, +size1)
        self.assertExtentEqualY(dim, 0, +size1)
        self.assertExtentEqualZ(dim, 0, size2)

    def test_make_revolve_z_90_minusx(self):
        size1 = 5
        size2 = 10
        sketch = cadscript.make_sketch().add_rect(size1, size2, center=False)
        body = cadscript.make_revolve("Z", sketch, angle=90, start_axis="-X")  
        dim = body.get_extent()
        self.assertExtentEqualX(dim, -size1, 0)
        self.assertExtentEqualY(dim, -size1, 0)
        self.assertExtentEqualZ(dim, 0, size2)

    def test_make_revolve_z_90_plusy(self):
        size1 = 5
        size2 = 10
        sketch = cadscript.make_sketch().add_rect(size1, size2, center=False)
        body = cadscript.make_revolve("Z", sketch, angle=90, start_axis="+Y")  
        dim = body.get_extent()
        self.assertExtentEqualX(dim, -size1, 0)
        self.assertExtentEqualY(dim, 0, +size1)
        self.assertExtentEqualZ(dim, 0, size2)

    def test_make_revolve_z_90_minusy(self):
        size1 = 5
        size2 = 10
        sketch = cadscript.make_sketch().add_rect(size1, size2, center=False)
        body = cadscript.make_revolve("Z", sketch, angle=90, start_axis="-Y")  
        dim = body.get_extent()
        self.assertExtentEqualX(dim, 0, +size1)
        self.assertExtentEqualY(dim, -size1, 0)
        self.assertExtentEqualZ(dim, 0, size2)

    def test_make_revolve_x_90(self):
        size1 = 5
        size2 = 10
        sketch = cadscript.make_sketch().add_rect(size1, size2, center=False)
        body = cadscript.make_revolve("X", sketch, angle=90)  
        dim = body.get_extent()
        self.assertExtentEqualX(dim, 0, size2)
        self.assertExtentEqualY(dim, 0, +size1)
        self.assertExtentEqualZ(dim, 0, +size1)

    def test_make_revolve_x_90_plusy(self):
        size1 = 5
        size2 = 10
        sketch = cadscript.make_sketch().add_rect(size1, size2, center=False)
        body = cadscript.make_revolve("X", sketch, angle=90, start_axis="+Y")  
        dim = body.get_extent()
        self.assertExtentEqualX(dim, 0, size2)
        self.assertExtentEqualY(dim, 0, +size1)
        self.assertExtentEqualZ(dim, 0, +size1)

    def test_make_revolve_y_90(self):
        size1 = 5
        size2 = 10
        sketch = cadscript.make_sketch().add_rect(size1, size2, center=False)
        body = cadscript.make_revolve("Y", sketch, angle=90)  
        dim = body.get_extent()
        self.assertExtentEqualX(dim, 0, +size1)
        self.assertExtentEqualY(dim, 0, size2)
        self.assertExtentEqualZ(dim, 0, +size1)

    def test_make_revolve_y_90_plusz(self):
        size1 = 5
        size2 = 10
        sketch = cadscript.make_sketch().add_rect(size1, size2, center=False)
        body = cadscript.make_revolve("Y", sketch, angle=90, start_axis="+Z")  
        dim = body.get_extent()
        self.assertExtentEqualX(dim, 0, +size1)
        self.assertExtentEqualY(dim, 0, size2)
        self.assertExtentEqualZ(dim, 0, +size1)

    def test_make_revolve_z_90_to_180(self):
        size1 = 5
        size2 = 10
        sketch = cadscript.make_sketch().add_rect(size1, size2, center=False)
        body = cadscript.make_revolve("Z", sketch, angle=(90, 180))  
        dim = body.get_extent()
        self.assertExtentEqualX(dim, -size1, 0)
        self.assertExtentEqualY(dim, 0, +size1)
        self.assertExtentEqualZ(dim, 0, size2)


if __name__ == '__main__':
    unittest.main()
