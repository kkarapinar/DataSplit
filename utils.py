import os
import shutil
import glob


# Remove folder with files inside and create empty one again
def re_create_folder(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.makedirs(path)


def insensitive_glob(pattern):
    def either(c):
        return '[%s%s]' % (c.lower(), c.upper()) if c.isalpha() else c

    return glob.glob(''.join(map(either, pattern)))
