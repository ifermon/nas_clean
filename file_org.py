#!/usr/bin/python
"""
    Organizes files generated by motion into directories.
    Year / Month / Day

"""
from path import path
from sys import argv

SEARCH_PATH = '/mnt/usbstorage/security'
VALID_EXTENSIONS = [".jpg", ".avi"]


if __name__ == "__main__":
    
    if len(argv) == 1:
        search_path = SEARCH_PATH
    else:
        search_path = argv[1]

    src_dir = path(search_path)

    for f in src_dir.files():
        # First validate the extension
        if f.ext.lower() not in VALID_EXTENSIONS:
            print("Invalid extension -- {}".format(f.name))
            continue

        # Next get the file name parts (year, month, day)
        year = f.name[:4]
        month = f.name[4:6]
        day = f.name[6:8]
        dest_dir = "{}/{}/{}/{}".format(f.dirname(), year, month, day)

        # Now validate the file naming convention, just in case
        # Stupid hard-coding, but should catch issues in the near term
        # if we have them. I'll worry about it in two years
        if not year.isnumeric():
            print("Invalid year - {}".format(f))
            continue
        if not month.isnumeric():
            print("Invalid year - {}".format(f))
            continue
        if not day.isnumeric():
            print("Invalid year - {}".format(f))
            continue

        # Now make directory(s) if necessary
        dest_dir = path(dest_dir)
        dest_dir.makedirs_p()

        # Now move the file
        dest_name = "{}/{}".format(dest_dir, f.name)
        f.move(dest_name)
