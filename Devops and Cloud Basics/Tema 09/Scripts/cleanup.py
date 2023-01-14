from genericpath import exists
from os import path, listdir, remove
import absolute
from datahandle import data
from shutil import rmtree

# @@@@@ ///// WARNING \\\\\ @@@@@
# This script should be used for testing and cleaning up data.
# Make sure you have a backup of the /tweets/ folder before running it.
# @@@@@ \\\\\ WARNING ///// @@@@@

def cleanup():
    database_list = ['title.basics.tsv', 'title.principals.tsv', 'name.basics.tsv']
    for database in database_list:
        gz_file = path.join(absolute.path(), 'imdbdatascrapping', 'imdbdata', database, database + '.gz')
        data_file = path.join(absolute.path(), 'imdbdatascrapping', 'imdbdata', database, 'data.tsv')
        if exists(gz_file):
            data.delete_file(gz_file, 1)
        if exists(data_file):
            data.delete_file(data_file, 2)
    folder = path.join(absolute.path(), 'tweets')
    for files in listdir(folder):
        file = path.join(folder, files)
        try:
            rmtree(file)
        except OSError:
            remove(file)
        
if __name__ == '__main__':
    cleanup()
