import os
import re
import shutil
import pandas


class FileManipulator:

    def __init__(self, input_path, output_path):
        """
        Creates a FileManipulator object
        :param input_path: Directory of the Project you want to work on
        :type input_path: Path to directory
        :param output_path: Directory to the output
        :type output_path: Path to directory
        """
        if os.path.isdir(input_path):
            self.input_path = input_path
            print(f"I'm going to search in {self.input_path} \n")

            self.output_path = output_path
            print(f"I'm going to insert the data in {self.output_path} \n")
        else:
            print("Input and Output need to be directories!")

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
            path = self.input_path
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
                print("You are trying to copy " + str(len(src)) +
                      " to " + str(len(dst)) + " directories!")
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
        """
        We make a full copy of the given project - all changes will be made there
        :param src:
        :param dst:
        :param delete:
        :return:
        """
        try:
            if os.path.isdir(dst) and delete:
                shutil.rmtree(dst, ignore_errors=False)

            shutil.copytree(src, dst, symlinks=True, ignore=None)
        except OSError:
            print("An error occurred, while copying!")
            print("Please delete the output folder, if it exists.")

    def write_to_file(self, dst_paths, infos='', info_paths=''):
        """
        Can do 2 things:
            a) Write a String or list of Information (infos) to a file or list of files
            b) Read file(s) and write their content into new file(s)

        :param dst_paths:
            Path(s) to the destination
        :type dst_paths:
            Path to file, not a directory
        :param infos:
            Optional part_parameters - either infos or info_paths must be given.
        :type infos:
            Information provided as String(s)
        :param info_paths:
            Optional part_parameters - either infos or info_paths must be given.
        :type info_paths:
            Information provided as path to file(s)
        """
        if infos:
            # Many Strings into many different files (writes pairwise)
            if isinstance(infos, (list, tuple)) and isinstance(dst_paths, (list, tuple)):
                for info, dst_path in zip(infos, dst_paths):
                    try:
                        with open(dst_path, "w+", encoding="utf-8") as new_file:
                            new_file.write(info)
                    except IOError as e:
                        print(f"I/O Error {e.errno}: {e.strerror}")
            # N Strings into 1 file
            elif isinstance(infos, (list, tuple)):
                try:
                    with open(dst_paths, "w+", encoding="utf-8") as new_file:
                        for info in infos:
                            new_file.write(info + " \n")
                except IOError as e:
                    print(f"I/O Error {e.errno}: {e.strerror}")
            # 1 String into N files
            elif isinstance(dst_paths, (list, tuple)):
                for dst_path in dst_paths:
                    try:
                        with open(dst_path, "w+", encoding="utf-8") as new_file:
                            new_file.write(infos)
                    except IOError as e:
                        print(f"I/O Error {e.errno}: {e.strerror}")
            # 1 String into 1 specific file
            else:
                try:
                    with open(dst_paths, "w+", encoding="utf-8") as new_file:
                        new_file.write(infos)
                except IOError as e:
                    print(f"I/O Error {e.errno}: {e.strerror}")

        if info_paths and not infos:
            for info_path, dst_path in zip(info_paths, dst_paths):
                try:
                    if os.path.isfile(info_path) and os.path.isfile(dst_path):
                        # Open source file
                        with open(info_path, "r") as info:
                            # read source file
                            temp = info.read()

                        # Open or create dst. file
                        with open(dst_path, "w+", encoding="utf-8") as new_file:
                            # write to dst file
                            new_file.write(temp)
                    else:
                        raise IOError('You did not provide file paths!')
                except IOError as e:
                    print(f"I/O Error {e.errno}: {e.strerror}")
