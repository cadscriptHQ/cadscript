# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path
import tempfile
import time
import unittest
import cadscript


class DxfTest(unittest.TestCase):

    def test_export_dxf_reimport(self):
        # Create a simple sketch
        s = cadscript.make_sketch()
        s.add_rect(10, 20)
        # export to temp file, use library to create unique filename
        temp_dir = Path(tempfile.gettempdir())
        temp_path = str(temp_dir / f"cadscript_{time.time()}.dxf")

        s.export_dxf(temp_path)

        # test if file exists
        self.assertTrue(Path(temp_path).exists())

        # reimport
        s2 = cadscript.make_sketch()
        s2.add_import_dxf(temp_path)

        # test if reimported sketch has same extents
        self.assertEqual(s.get_extent(), s2.get_extent())



if __name__ == '__main__':
    unittest.main()
