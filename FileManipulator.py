import os
import re
import shutil
import pandas


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

    def find_files(self, pattern, path=''):
        """
        Searches the given input path for files, which are compatible
        with the given regEx pattern
        
        :param pattern: Any regEx pattern, should start with r
        Example: r'^I am new to this$'
        
        :param path: Can be filled, if you want to search a specific path
        If it is not filled, the output directory will be searched
        
        :return:
        """
        temp = []
        quick_stop = False
        if not path:
            path = self.input_directory
            # Input directory should not be searched entirely
            quick_stop = True

        for root, directories, filenames in os.walk(path):
            for filename in filenames:
                if re.match(pattern, filename):
                    temp.append(os.path.join(root, filename))
                    if quick_stop:
                        return temp
        return temp

    def copy_files(self, src, dst, relative_path=''):
        """
        https://docs.python.org/3/library/shutil.html
        :param src:         1 or N files | 1 directory
        :param dst:         N or 1 files | 1 directory
        :param relative_path:    Any directory, relative to the source file
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
            xls_df = pandas.read_excel(filepath, sheet_name=None)

            # removing the .xls file
            os.unlink(filepath)

            # Create a pandas excel writer using xlsxwriter engine
            writer = pandas.ExcelWriter(filepath + "x", engine='xlsxwriter')

            # Write information to corresponding excel sheet
            for sheetname, info in xls_df.items():
                info.to_excel(writer, sheet_name=sheetname, index=False)

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

    def write_to_file(self, infos, paths, relative_path='', src_dst=''):
        """
        Creates files if needed and writes the given info into it
        :param infos:
        :param paths:
        :param src_dst:
        :param relative_path:
        :return:
        """
        if isinstance(paths, (list, tuple)) and isinstance(infos, (list, tuple)):
            for info, path in zip(infos, paths):
                # Replace old with new data, if src given
                if src_dst:
                    self.copy_files(src_dst, path)
                if info.strip():
                    # path to file, which shall be created/written to
                    file = open(os.path.join(os.path.dirname(path) + relative_path), "w+")
                    file.write(info)
                    file.close()
        else:
            if src_dst:
                self.copy_files(src_dst, paths)
            if infos.strip():
                # path to file, which shall be created/written to
                file = open(os.path.dirname(paths) + relative_path, "w+")
                file.write(infos)
                file.close()