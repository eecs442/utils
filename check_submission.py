# David Fouhey
# last modified by Nikhil Devraj on 2022.03.10
# 442 submission format checker
#
# This should only accept a zip file containing a single folder ${uniqname} and which homework ${hwi}
# e.g. python check_submission.py myuniqname.zip hw1
# In particular, it will fail for:
#    -Files outside that folder
#    -Multiple folders (although __MACOSX is fine)
#    -Non-zip files

import os
import sys
import zipfile


def die(s):
    print('%s\nExiting Unsuccessfully.' % s)
    sys.exit(1)


def first_folder(path):
    """ Return the first folder in the path """
    while path != "":
        nextPath, _ = os.path.split(path)
        if nextPath == "":
            return path
        path = nextPath


def main(hws):
    if len(sys.argv) < 3:
        print("Usage: %s ZIP_NAME(uniqname.zip) HW_NAME(hw0|hw1|...)" % sys.argv[0])
        sys.exit(1)

    filename = sys.argv[1]
    hw = sys.argv[2]

    if hw not in ["hw0", "hw1", "hw2", "hw3", "hw4", "hw5", "hw6"]:
        die("Oops! %s is not a valid hw name" % hw)

    if len(hws[int(hw[2:])]) == 0:
        die("Please update this check_submission.py file")

    if not os.path.exists(filename):
        die("Oops! %s doesn't exist" % filename)

    if not zipfile.is_zipfile(filename):
        die("Oops! %s is not a zipfile" % filename) 

    try:
        zf = zipfile.ZipFile(filename, 'r')
    except:  # noqa: E722
        die("Oops! I can't can't open %s")

    subdirs = set()
    files = set()
    for zfFilen in zf.namelist():
        head, tail = os.path.split(zfFilen)
        if head == "":
            die("I found a file that's not in a directory: %s" % zfFilen)
        subdirs.add(first_folder(zfFilen))
        # Handle macs, sigh again
        if first_folder(zfFilen) != "__MACOSX" and os.path.basename(zfFilen) != '':
            files.add(os.path.basename(zfFilen))

    # Handle macs, sigh
    subdirs.discard("__MACOSX")

    if len(subdirs) > 1:
        subdir_str = ', '.join(list(subdirs))
        die("There are multiple root subfolders: %s" % subdir_str)

    # test if files have been included
    required_files = set(hws[int(hw[2:])])
    for file in files:
        # stop when all the required files included
        if not required_files:
            break
        if file in required_files:
            required_files.remove(file)
    if required_files:
        missing_files = ', '.join(list(required_files))
        die("I can't find these files: %s" % missing_files)

    zf.close()
    print("Tests passsed, assuming your uniqname is ``%s''" % list(subdirs)[0])


if __name__ == "__main__":
    # Please hard code the required files for each homework here
    # students please DO NOT modify this
    hws = [
        ["warmups.py", "tests.py", "dither.py", "mystery_visualize.py"],  # hw0
        ["main.py", "util.py", "cube.gif", "im1.jpg", "im2.jpg", "info.txt"],  # hw1
        ["filters.py", "corners.py", "blob_detection.py", "common.py"],  # hw2
        ["common.py", "homography.py", "task5.py", "task6.py", "mypanorama1.jpg", "mypanorama2.jpg"], # hw3
        ["layers.py", "fitting.py", "functions.py", "train.py", "two_layer_net.py"],  # hw4
        ["part1.ipynb", "part2.ipynb", "part3.ipynb"],  # hw5
        ["task1.py", "task23.py"], # hw6
    ]
        
    main(hws)
