from genericpath import exists
import os, absolute


def create():
    database_list = ['title.basics.tsv', 'title.principals.tsv', 'name.basics.tsv']
    for database in database_list:
        folder_path = os.path.join(absolute.path(), 'imdbdatascrapping', 'imdbdata', database)
        if not exists(folder_path):
            os.makedirs(folder_path)
    tweets_folder = os.path.join(absolute.path(), 'tweets')
    if not exists(tweets_folder):
        os.makedirs(tweets_folder)