# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

from re import T
import unittest
import cadscript


class MakeTextTest(unittest.TestCase):

    def test_box_extent(self):
        size = 4
        height = 5
        epsilon = 1e-5
        text = cadscript.make_text("TEST", size, height, center=False)
        (xmin, xmax), (ymin, ymax), (zmin, zmax) = text.get_extent()
        self.assertAlmostEqual(xmin, 0, delta=epsilon)
        self.assertGreater(xmax, 1)
        self.assertAlmostEqual(ymin, 0, delta=epsilon)
        self.assertGreater(ymax, 1)
        self.assertAlmostEqual(zmin, 0, delta=epsilon)
        self.assertAlmostEqual(zmax, height, delta=epsilon)

        text = cadscript.make_text("TEST", size, height, center=True)
        (xmin2, xmax2), (ymin2, ymax2), (zmin2, zmax2) = text.get_extent()
        self.assertAlmostEqual(-xmin2, xmax2, delta=epsilon)
        self.assertAlmostEqual(-ymin2, ymax2, delta=epsilon)
        self.assertAlmostEqual(-zmin2, zmax2, delta=epsilon)
        self.assertAlmostEqual(xmax - xmin, xmax2 - xmin2, delta=epsilon)
        self.assertAlmostEqual(ymax - ymin, ymax2 - ymin2, delta=epsilon)
        self.assertAlmostEqual(zmax - zmin, zmax2 - zmin2, delta=epsilon)





if __name__ == '__main__':
    unittest.main()
