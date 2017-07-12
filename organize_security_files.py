#!/usr/bin/python
"""
    This modules organizes my security files
    First- Look for new files to organize
    For each file found:
        1. Extract date from filename
        2. Create dest dir if not already existing
        3. Rename file to include properly formatted date
        4. Move file to dest directory
"""
import os.path as path
import os
import fnmatch
import sys
import time

BASE_DIR = "/mnt/usbstorage/security/"
DEST_DIR = "/mnt/usbstorage/security/"
SECS_IN_DAY = 86400 # 1 day of seconds

print("{} | Organizing files.".format(time.asctime()))

# First look for new files to organize, we do not do this recursively
new_file_list = []
files = os.listdir(BASE_DIR)
for filename in fnmatch.filter(files, '*.JPG'):
    new_file_list.append(os.path.join(BASE_DIR, filename))
for filename in fnmatch.filter(files, '*.jpg'):
    new_file_list.append(os.path.join(BASE_DIR, filename))
for filename in fnmatch.filter(files, '*.avi'):
    new_file_list.append(os.path.join(BASE_DIR, filename))
for filename in fnmatch.filter(files, '*.mp4'):
    new_file_list.append(os.path.join(BASE_DIR, filename))

if len(new_file_list) == 0:
    print("{} | No files found".format(time.asctime()))
    sys.exit(0)
else:
    print("{} | We have a list of {} files. The first file is {}".format(
            time.asctime(), len(new_file_list), new_file_list[0]))

# For each file found, extract date and rename (move)
# We've already filtered the files so that we only have jpg's or avi's
# now extract the dates. Files are formatted as yyyymmdd as the first 8 chars
f_ctr = 0
cutoff = time.time() - (1 * SECS_IN_DAY)
# Uncomment to write list of already existing files
#flist = open("./files_already_existing", "a+")
for f in new_file_list:

    # To help with debugging by limiting size of list
    f_ctr += 1
    if f_ctr >9999:
        sys.exit(1)

    f_base = os.path.basename(f)

    # if file is newer than cutoff then skip it
    try:
        if os.stat(f).st_mtime > cutoff:
            #print("{} | File newer than cutoff: {}".format(time.asctime(), f))
            continue
    except OSError:
        print("Unable to stat {}.".format(f))
        pass

    #Assume this is running for 2015-2029, we can fix this hardcoding in 2030
    if f_base[0:3] not in ("201", "202"):
        print("{} | Filename \"{}\" is not valid.".format(
                time.asctime(), f_base))
        continue

    year = f_base[0:4]
    month = f_base[4:6]
    day = f_base[6:8]
    #print("year {} month {} day {} file {}".format(year, month, day, f_base))

    # Create new file name
    new_f = path.join(DEST_DIR, year, month, day, f_base)

    if os.path.exists(new_f):
        #print("{} | Filename \"{}\" already exists. Not moving \"{}\"".format(
        #        time.asctime(), new_f, f))
        # Uncomment to write list of already existing files
        #flist.write(f + "\n")
        #print("{} | Removing {}.".format(time.asctime(), f))
        os.remove(f)
        continue

    #print("{} | Moving \"{}\" to \"{}\"".format(time.asctime(), f, new_f))
    os.renames(f, new_f)

# Uncomment to write list of already existing files
#flist.close()
