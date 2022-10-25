import os
import sys
import unittest
from CSV_Combiner import CSV_Combiner
from io import StringIO


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

    # test 6
    def test_header_only_added_once(self):
        argv = [self.script_path, './test/fixtures/clothing.csv',
                './test/fixtures/accessories.csv']
        self.combiner_object.combiner(argv)

        self.output_test.write(self.output.getvalue())
        self.output_test.close()

        # find length of the first file
        counter = 0
        with open(self.test_fixture_path1) as fileobject:
            for line in fileobject:
                counter += 1
        # divide by 2 because there is a blank line after each line
        counter = counter // 2

        # decrement counter till we reach the end of first file in the combined csv
        with open(self.output_path) as f:
            header1 = next(f)
            while counter != 0:
                header2 = next(f)
                counter -= 1

        self.assertNotEqual(header1, header2)

    def test_all_values_added(self):
        argv = [self.script_path, './test/fixtures/clothing.csv',
                './test/fixtures/accessories.csv', './test/fixtures/household_cleaners.csv']
        self.combiner_object.combiner(argv)

        self.output_test.write(self.output.getvalue())
        self.output_test.close()

        # find lengths of all files and match it with length of combined csv
        # can be done my making pandas dataframe but loading them in memory would be costly

        counter_file_1 = 0
        counter_file_2 = 0
        counter_file_3 = 0
        with open(self.test_fixture_path1) as fileobject:
            for _ in fileobject:
                counter_file_1 += 1
        with open(self.test_fixture_path1) as fileobject:
            for _ in fileobject:
                counter_file_2 += 1
        with open(self.test_fixture_path1) as fileobject:
            for _ in fileobject:
                counter_file_3 += 1

        # divide by 2 because there is a blank line after each line
        counter_file_1 = counter_file_1 // 2
        counter_file_2 = counter_file_2 // 2
        counter_file_3 = counter_file_3 // 2
        # add to find total count. Subtract 2 for repeated header
        total_count = counter_file_1 + counter_file_2 + counter_file_3 - 2

        counter_combined_csv = 0
        with open(self.output_path) as f:
            for line in f:
                counter_combined_csv += 1

        self.assertEqual(total_count, counter_combined_csv)


if __name__ == "__main__":
    unittest.main()
