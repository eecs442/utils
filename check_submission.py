# !/usr/bin/python
# David Fouhey
# 442 submission format checker
#
# This should only accept a zip file containing a single folder ${uniqname}
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


def main():
    if len(sys.argv) < 2:
        print("%s zipname" % sys.argv[0])
        sys.exit(1)

    filename = sys.argv[1]

    if not os.path.exists(filename):
        die("Oops! %s doesn't exist" % filename)

    if not zipfile.is_zipfile(filename):
        die("Oops! %s is not a zipfile" % filename)

    try:
        zf = zipfile.ZipFile(filename, 'r')
    except:  # noqa: E722
        die("Oops! I can't can't open %s")

    subdirs = set()

    for zfFilen in zf.namelist():
        head, tail = os.path.split(zfFilen)
        if head == "":
            die("I found a file that's not in a directory: %s" % zfFilen)
        subdirs.add(first_folder(zfFilen))

    # Handle macs, sigh
    subdirs.discard("__MACOSX")

    if len(subdirs) > 1:
        subdir_str = ', '.join(list(subdirs))
        die("There are multiple root subfolders: %s" % subdir_str)

    zf.close()
    print("Tests passsed, assuming your uniqname is ``%s''" % list(subdirs)[0])


if __name__ == "__main__":
    main()
