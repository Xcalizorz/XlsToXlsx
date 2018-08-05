# PentestGenConverter

This program is specifically designed to convert old reports, created by the Pentestgenerator **older than** `v.1.0.0`, released in June 2018.

## How to use

    Give the path to the report you want to convert, e.g.:
    "C:\Users\zadjad.rezei\Desktop\bwb"

## What happens

    1. All .xls files will be converted to equivalent .xlsx files
    2. A Parameter.xlsx file will be created and filled
      1. The program will fill in the Language and OWASP Parameters
        1. Language: German
        2. OWASP: 2013
      2. You can change this, using Excel, after the conversion is done
    3. TODO: new .Rnw files are downloaded from the Repo
      1. Replace old .Rnw