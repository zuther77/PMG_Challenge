import os
import sys
import unittest
from CSV_Combiner import CSV_Combiner
from io import StringIO

import pandas as pd


class test_csv_combiner(unittest.TestCase):

    output_path = './test/combined.csv'
    script_path = './CSV_Combiner.py'
    blank_csv_path = './test/blank.csv'
    test_fixture_path1 = './test/fixtures/clothing.csv'
    test_fixture_path2 = './test/fixtures/accessories.csv'

    random_extension_files_path = './test/random_files'

    # instantiate combiner object
    combiner_object = CSV_Combiner()
    output_test = open(output_path, 'w')

    @classmethod
    def setUpClass(cls):
        sys.stdout = cls.output_test

    @classmethod
    def tearDownClass(cls):
        cls.output_test.close()
        if os.path.exists(cls.output_path):
            os.remove(cls.output_path)

    # For below functions,  followed -  https://docs.python.org/3/library/unittest.html
    def setUp(self):
        self.output = StringIO()
        sys.stdout = self.output
        self.output_test = open(self.output_path, 'w+')

    def tearDown(self):
        self.output_test.close()

    # test 1
    def test_no_file_pass(self):
        argv = [self.script_path]
        self.combiner_object.combiner(argv)
        self.assertIn("Error: No files provided", self.output.getvalue())

    # test 2
    def test_empty_file(self):
        argv = [self.script_path, self.blank_csv_path]
        self.combiner_object.combiner(argv)

        self.assertIn("Warning: Passing empty file ", self.output.getvalue())

    # test 3
    def test_file_extension(self):
        argv = os.listdir(self.random_extension_files_path)
        self.combiner_object.combiner(argv)
        self.assertIn("Error: Invalid file type: ", self.output.getvalue())

    # test 4
    def test_file_not_exists(self):
        argv = [self.script_path, "file_not_present.csv"]
        self.combiner_object.combiner(argv)
        self.assertIn("Error : File not found: ", self.output.getvalue())

    # test 5
    def test_filesource_column(self):
        # os.listdir not working, manually pass file path
        argv = [self.script_path, './test/fixtures/clothing.csv',
                './test/fixtures/accessories.csv']
        self.combiner_object.combiner(argv)

        self.output_test.write(self.output.getvalue())
        self.output_test.close()

        with open(self.output_path) as f:
            header = next(f)

        self.assertIn("filename", header)


if __name__ == "__main__":
    unittest.main()
