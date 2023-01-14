from genericpath import exists
import os, absolute
from datetime import datetime

def create():
    database_list = ['title.basics.tsv', 'title.principals.tsv', 'name.basics.tsv']
    for database in database_list:
        folder_path = os.path.join(absolute.path(), 'imdbdatascrapping', 'imdbdata', database)
        if not exists(folder_path):
            os.makedirs(folder_path)
    output_folder = os.path.join(absolute.path(), 'output')
    if not exists(output_folder):
        os.makedirs(output_folder)

def new():
    now = datetime.now()
    date_and_time = now.strftime("%Y-%m-%d_%H-%M-%S")
    path = os.path.join(absolute.path(), 'output', date_and_time)
    os.mkdir(path)
    return path