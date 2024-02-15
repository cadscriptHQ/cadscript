# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

import unittest
import cadscript


class MakeTextTest(unittest.TestCase):

    def test_box_extent(self):
        size = 4
        height = 5
        epsilon = 1e-5
        text = cadscript.make_text("TEST", size, height, center=False)
        dim = text.get_extent()
        self.assertAlmostEqual(dim.min_x, 0, delta=epsilon)
        self.assertGreater(dim.max_x, 1)
        self.assertAlmostEqual(dim.min_y, 0, delta=epsilon)
        self.assertGreater(dim.max_y, 1)
        self.assertAlmostEqual(dim.min_z, 0, delta=epsilon)
        self.assertAlmostEqual(dim.max_z, height, delta=epsilon)

        text = cadscript.make_text("TEST", size, height, center=True)
        dim2 = text.get_extent()
        self.assertAlmostEqual(-dim2.min_x, dim2.max_x, delta=epsilon)
        self.assertAlmostEqual(-dim2.min_y, dim2.max_y, delta=epsilon)
        self.assertAlmostEqual(-dim2.min_z, dim2.max_z, delta=epsilon)
        self.assertAlmostEqual(dim.size_x, dim2.size_x, delta=epsilon)
        self.assertAlmostEqual(dim.size_y, dim2.size_y, delta=epsilon)
        self.assertAlmostEqual(dim.size_z, dim2.size_z, delta=epsilon)





if __name__ == '__main__':
    unittest.main()
