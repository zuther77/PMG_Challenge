import csv
import os
import pathlib
import sys


class CSV_Combiner():
    def __init__(self) -> None:
        super().__init__()

    def file_validation(self, argv) -> bool:
        # print(argv)
        if len(argv) < 2:
            print("Error: No files provided")
            print(
                "Script Usage: python CSV_combiner.py ./path/file1.csv ./path/file2.csv  ./path/file3.csv  ")
            return False

        csv_files = argv[1:]
        for filename in csv_files:
            try:
                # Check file extension
                if pathlib.Path(filename).suffix != ".csv":
                    raise TypeError(
                        "Error: Invalid file type: \"{}\". Only pass .csv files".format(filename))

                # check if files exist in the directory
                if not os.path.exists(filename):
                    raise FileNotFoundError(
                        "Error : File not found: {}".format(filename))

                # Check if file is not empty
                if os.stat(filename).st_size == 0:
                    raise OSError(
                        "Warning: Passing empty file {}. File will be skipped".format(filename))

            # Throw corresponding error
            except FileNotFoundError as e:
                print(e)
                return False
            except OSError as e:
                print(e)
            except TypeError as e:
                print(e)
                return False

        return True

    ''' 
        Code Notes - 
        1) Don't load the whole csv file to memory. 
        3) Read each file line-by-line, make required modifations to the line. 
        4) Write line in once its read in a stream fashion. 

        Solution: Use similar approaches like fs.createreadstream  and fs.createwritestream in JS.
    '''

    def combiner(self, argv):
        header_saved = False
        if self.file_validation(argv):
            files = argv[1:]

            # open target file for writing. with clause will automatically close the file
            with open("combined.csv", 'w', newline='') as target:
                writer = csv.writer(
                    target, delimiter=',', quoting=csv.QUOTE_NONE, escapechar='', quotechar='\n')

                # iterate through each file
                for filename in files:
                    # print("Adding " + filename)  # debug print

                    # open each file in read mode
                    try:
                        with open(filename, 'r') as current_file:

                            # add header only once
                            header = next(current_file).strip().split(",")
                            header.append("\"filename\"")
                            if not header_saved:
                                print(",".join(header).replace('"', ''))
                                writer.writerow(header)
                                header_saved = True

                            # Add rest to the target file
                            for line in current_file:
                                if len(line) > 1:
                                    line_list = line.strip().split(',')
                                    file_location = os.path.basename(filename)
                                    line_list.append(
                                        "\"" + file_location + "\"")
                                    print(",".join(line_list).replace(
                                        '"', ''))
                                    writer.writerow(line_list)

                    except StopIteration:
                        print("Blank file found and will be skipped")

        # remove combined.csv if the file was not written to
        if os.path.exists('combined.csv') and os.stat('combined.csv').st_size == 0:
            os.remove('combined.csv')

        return


if __name__ == '__main__':
    combiner = CSV_Combiner()
    combiner.combiner(sys.argv)
