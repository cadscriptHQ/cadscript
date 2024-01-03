# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

import unittest
import cadscript 


class BodyPropertiesTest(unittest.TestCase):

    def test_box_center(self):
        box = cadscript.make_box(1,2,3, center=False)
        self.assertEqual(box.get_center(), (0.5,1,1.5))
        
    def test_box_extent(self):
        box = cadscript.make_box(1,2,3, center=True)
        self.assertEqual(box.get_extent(), ((-0.5,0.5),(-1,1),(-1.5,1.5)))

if __name__ == '__main__':
    unittest.main()        