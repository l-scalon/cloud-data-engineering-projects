import pandas as pd
import os, absolute

def movie_scrapping(from_year, to_year):
    database = os.path.join(absolute.path(), 'imdbdatascrapping', 'imdbdata', 'title.basics.tsv', 'data.tsv')
    df = pd.read_csv(database, sep = '\t')
    df.loc[(df.startYear == r'\N'), 'startYear'] = '0'
    df['startYear'] = df['startYear'].astype(int)
    df = df.loc[(df['titleType'] == 'movie') & (df['startYear'] >= from_year) & (df['startYear'] <= to_year)]
    df = df['tconst']
    return df

def get(from_year, to_year):
    return movie_scrapping(from_year, to_year)