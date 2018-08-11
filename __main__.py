from FileManipulator import FileManipulator
from tkinter.filedialog import askdirectory
import os.path


def __main__():

    # Path declaration block | init. directory is the directory of this python script
    input_path = os.path.normpath(
        askdirectory(initialdir = os.path.normpath(os.path.dirname(__file__))
        )
    )
    output_path = os.path.normpath(input_path + "_new")

    # Converting block
    converter = FileManipulator(input_path, output_path)
    
    # creates a list of paths to the .xls files
    xls_files = converter.find_files("(.*?).xls$")

    # creating the copy if there are any .xls files
    if xls_files:
        converter.copy_directory(input_path, output_path)
        converter.xls_to_xlsx(xls_files)
    else:
        print("No .xls files found!")

if __name__ == "__main__":
    __main__()
