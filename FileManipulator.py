import os
import re
import shutil
import pandas as pd


class FileManipulator:

    def __init__(self, input_directory='', output_directory=''):
        if not input_directory:
            input_directory = input("Which directory should I search? \n")

        self.input_directory = input_directory
        print(f"I'm going to search in {self.input_directory} \n")

        if not output_directory:
            output_directory = input("Which directory should I output to? \n")

        self.output_directory = output_directory
        print(f"I'm going to insert the data in {self.output_directory} \n")

    def find_files(self, pattern):
        """
        Searches the given input path for files, which are compatible
        with the given regEx pattern
        :param pattern: Any regEx pattern, should start with r
        Example: r'^I am new to this$'
        :return:
        """
        temp = []
        for root, directories, filenames in os.walk(self.output_directory):
            for filename in filenames:
                if re.match(pattern, filename):
                    temp.append(os.path.join(root, filename))
        return temp

    def copy_files(self, src, dst, relative_path=''):
        """
        https://docs.python.org/3/library/shutil.html
        :param src:         1 or N files | 1 directory
        :param dst:         N or 1 files | 1 directory
        :param relative:    Any directory, relative to the source file
        :return:
        """
        # insert the new files and overwrite the old files
        if isinstance(dst, (list, tuple)):
            # Usual case, 1 src file, many places to copy to
            if not isinstance(src, (list, tuple)):
                for dst_directory in dst:
                    shutil.copy2(src, os.path.dirname(dst_directory))
            else:
                print("You are trying to copy " + len(src) +
                      " to " + len(dst) + " directories!")
        # Useful if you want to copy many files to 1 directory
        elif not isinstance(dst, (list, tuple)):
            if isinstance(src, (list, tuple)):
                for src_file in src:
                    # relative path + any directory + filename
                    src_file_path = os.path.join(os.path.dirname(__file__), relative_path, src_file)
                    shutil.copy2(src_file_path, dst)
            else:
                src_file_path = os.path.join(os.path.dirname(__file__), relative_path, src)
                shutil.copy2(src_file_path, dst)

        else:
            shutil.copy2(src, os.path.dirname(dst))

    def xls_to_xlsx(self, filepaths):
        """

        :param filepaths: a list of paths to xls files
        :return:
        """
        for filepath in filepaths:
            # reading old xls files
            xls_df = pd.read_excel(filepath, sheet_name=None)

            # removing the .xls file
            os.unlink(filepath)

            # Create a pandas excel writer using xlsxwriter engine
            writer = pd.ExcelWriter(filepath + "x", engine='xlsxwriter')

            # if the file has more than 1 sheet
            if len(xls_df) > 1:
                for sheetname, info in xls_df.items():
                    info.to_excel(writer, sheet_name=sheetname, index=False)
            else:
                # Writing first sheet to the file
                xls_df.to_excel(writer, sheet_name='Sheet1', index=False)

            # To add more sheets
            # other_dataframe.to_excel(writer, sheet_name='Sheet2', index=False)

            writer.save()

    def copy_directory(self, src, dst, delete=True):
        # We make a full copy of the given project - all changes will be made there
        try:
            if os.path.isdir(dst) and delete:
                shutil.rmtree(dst, ignore_errors=False)

            shutil.copytree(src, dst, symlinks=True, ignore=None)
        except OSError:
            print("An error occurred, while copying!")
            print("Please delete the output folder, if it exists.")