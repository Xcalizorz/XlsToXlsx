# XlsToXlsx

You can convert all .xls files from a given input path to .xlsx

Pictures won't be converted yet.

## How to use

### Install requirements

Install the requirements:

    cd /PATH/TO/XlsToXlsx
    pip install -r requirements.txt

### Use the program

Please keep in mind, this is a Python3.x project.

    Run __main__.py

    Select the path to the directory with the files you want to convert.

## What happens

    1. A copy of the directory will be created
      1. Directory name + "new"
    2. All .xls files will be converted to .xlsx
    3. Old .xls files will be deleted from the new directory

## Example files

There is a folder called "Example" - you can use this folder to test the conversion.

The .xls files were taken from [Carnegie Mellon University](https://www.cmu.edu/blackboard/files/evaluate/tests-example.xls)