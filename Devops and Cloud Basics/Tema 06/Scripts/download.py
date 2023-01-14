from genericpath import exists
import os, wget, gzip, shutil, absolute

def download_file(database):
    print('\nDownloading resources. Please wait.')
    url = 'https://datasets.imdbws.com/{}.gz'
    destiny = os.path.join(absolute.path(), 'imdbdatascrapping', 'imdbdata', database)
    wget.download(url.format(database), destiny)

def extract_file(database):
    file_in = os.path.join(absolute.path(), 'imdbdatascrapping', 'imdbdata', database, database + '.gz')
    file_out = os.path.join(absolute.path(), 'imdbdatascrapping', 'imdbdata', database, 'data.tsv')
    with gzip.open(file_in, 'rb') as f_in:
            with open(file_out, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

def delete_file(database):
    file = os.path.join(absolute.path(), 'imdbdatascrapping', 'imdbdata', database, database + '.gz')
    os.remove(file)

def get(database):
    this_path = os.path.join(absolute.path(), 'imdbdatascrapping', 'imdbdata', database, 'data.tsv')
    if not exists(this_path):
        download_file(database)
        extract_file(database)
        delete_file(database)

def download():
    get('title.basics.tsv')
    get('title.principals.tsv')
    get('name.basics.tsv')
