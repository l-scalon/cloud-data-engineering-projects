import pandas as pd
import os, absolute

def people_scrapping(movies):
    database = os.path.join(absolute.path(), 'imdbdatascrapping', 'imdbdata', 'title.principals.tsv', 'data.tsv')
    df = pd.read_csv(database, sep = '\t')
    df = df.merge(movies, on = ['tconst'])
    df = df.loc[df['category'] == 'actor']
    df = df['nconst']
    return df

def get(movies):
    return people_scrapping(movies)