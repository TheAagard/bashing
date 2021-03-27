# Written for Python 3.8
# Very simple, hash-based, duplicate file remover

import os, sys
import hashlib


# auxiliary function for file hashing
def hash_file(path, blocksize=65536):
    hasher = hashlib.sha256()
    with open(path, 'rb') as afile:
        # fill file in chunks into hasher
        buf = afile.read(blocksize)
        while len(buf) > 0:
            # will stop if afile.read returns nothing new
            hasher.update(buf)
            buf = afile.read(blocksize)

    # calculate hash
    return hasher.hexdigest()


def find_dups(dirname):
    if not os.path.isdir(dirname):
        sys.exit(f"ERROR: \"{dirname}\" is not a directory.")

    # 'hash-map' for duplicates. Format: {hash: [locations]}
    dups = {}
    for curdir, subdirs, files in os.walk(dirname):
        for filename in files:
            # get path to file, relative to cwd
            path = os.path.join(curdir, filename)
            fhash = hash_file(path)
            # if file already found, append dup-location
            if fhash in dups:
                dups[fhash].append(path)
            else:
                dups[fhash] = [path]

    # remove entries with no duplicates
    # iterate over new iterator to allow deletion from original
    for key in list(dups):
        if len(dups[key]) <= 1:
            del dups[key]

    return dups


def print_dups(dups):
    duplist = list(dups.values())
    print("The following files are identical:")
    print("--------------------")
    for ls in duplist:
        for l in ls:
            print(f"{l}")
        print("--------------------")


# delete all but one occurrence of a file
def delete_dups(dups):
    for key in dups:
        while len(dups[key]) > 1:
            f = dups[key].pop()
            os.remove(f)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        dups = find_dups(sys.argv[1])
        if len(dups) > 0:
            ans = "u"
            while ans.lower() not in ["a","q","d"]:
                ans = input("Duplicates found. Print, Delete or Abort? [p/d/a] > ")
                if ans.lower() == "p":
                    print_dups(dups)
                elif ans.lower() == "d":
                    delete_dups(dups)
        else:
            print("No duplicate files found.")
    else:
        print(f"Usage: python Delete-Duplicates.py <directory>")

