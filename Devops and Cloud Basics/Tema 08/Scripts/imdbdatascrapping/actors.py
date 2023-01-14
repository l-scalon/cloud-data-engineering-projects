from pandas import read_csv, concat
import absolute, os

def people_scrapping(movies):
    cols = ['tconst', 'category', 'nconst']
    database = os.path.join(absolute.path(), 'imdbdatascrapping', 'imdbdata', 'title.principals.tsv', 'data.tsv')
    chunksize = 10 ** 6

    with read_csv(database, sep = '\t', usecols = cols, dtype = {'category': 'category'}, 
    chunksize = chunksize) as reader:
        actors_df = []
        for chunk in reader:
            df = chunk.merge(movies, on = ['tconst'])
            df = df.loc[df['category'] == 'actor']
            df = df['nconst']
            if not df.empty:
                actors_df.append(df)
    actors = concat(actors_df)
    print('Actors: Done.')
    return actors

def get(movies):
    return people_scrapping(movies)