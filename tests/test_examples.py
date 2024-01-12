# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

import unittest
from cadquery import cqgi
import os
import glob
import pathlib


class ExampleRunnerTest(unittest.TestCase):

    def test_examples(self):
        # for each of the *.py files in the examples directory
        # run the file as a script and check that it runs without errors

        # get the path to the examples directory
        examples_dir = os.path.join(os.path.dirname(__file__), '..', 'examples')
        # get a list of all the *.py files in the examples directory
        example_files = glob.glob(os.path.join(examples_dir, '*.py'))
        # exclude files starting with "private"
        example_files = [f for f in example_files if not os.path.basename(f).startswith('private')]

        # run each example as a script
        for example_file in example_files:
            with self.subTest(example=pathlib.Path(example_file).name):
                try:
                    result = cqgi.parse(open(example_file).read()).build()
                    self.assertTrue(result.success)
                    self.assertIsNotNone(result.first_result)
                except Exception as e:
                    # if the file fails to run, raise an error
                    self.fail(f"Example file '{example_file}' failed to run, exception raised: {e}")


if __name__ == '__main__':
    unittest.main()
