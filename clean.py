#!/usr/bin/python

'''
    This script cleans files by age (oldest first) when the size of directory
    exceeds certain threshold
    This is not generic - very specific to my setup
    Assumes files are flat - not nested in sub directories
    Only looks at files ending in .avi
    1024 KB conversion
    1,048,576 MB conversion
    1,073,741,824 GB conversion
'''
from path import path
import time

print("Starting clean @ {0}".format(time.ctime()))

# Size in MB beyond which we start to delete files
THRESHOLD = 400 * 1024

# Cushion size is the amount below the threshold to stop deleting files
# e.g. if threshold is 400gb, and cushion is 50gb, we delete until
# total file size is below 350 gb (400 - 50)
# in MB
CUSHION = 5 * 1024

AVI_PATH = '/mnt/usbstorage/security'

d = path(AVI_PATH)

total_size_mb = 0
f_list = []
for f in d.files():
    #Only look at avi file, ignore other types
    if not '.avi' in f.name:
        continue
    #print ("name <{0}> time {1}".format(f.name, f.ctime))
    f_list.append((f, f.size, f.ctime))
    # Size in MB
    total_size_mb += f.size / (1024 * 1024)

# If we are above the size then sort the list by age, oldest files last
# delete files by age until total_size_mb < THRESHOLD - CUSHION
file_count = 0
if total_size_mb > THRESHOLD:
    # sort by ctime, desc order so oldest last 
    f_list.sort(key=lambda x: x[2], reverse=True) 
    while total_size_mb > (THRESHOLD - CUSHION):
        l = f_list.pop()
        # reduce total size by size of file being deleted
        total_size_mb -= (l[1]/ (1024*1024)) 
        l[0].remove()
        file_count += 1

print("Finished. Deleted {0} files @ {1}".format(file_count, time.ctime()))
