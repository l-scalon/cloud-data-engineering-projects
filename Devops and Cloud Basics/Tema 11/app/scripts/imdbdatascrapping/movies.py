from pandas import read_csv, concat
import absolute, os

def movie_scrapping(from_year, to_year):
    cols = ['tconst', 'titleType', 'startYear']
    database = os.path.join(absolute.path(), 'imdbdatascrapping', 'imdbdata', 'title.basics.tsv', 'data.tsv')
    chunksize = 10 ** 6

    with read_csv(database, sep = '\t', usecols = cols, dtype = {'titleType': 'category', 'startYear': 'string'}, 
    chunksize = chunksize) as reader:
        movies_df = []
        for chunk in reader:
            df = chunk
            df.loc[(df.startYear == r'\N'), 'startYear'] = '0'
            df['startYear'] = df['startYear'].astype(int)
            df = df.loc[(df['titleType'] == 'movie') & (df['startYear'] >= from_year) & (df['startYear'] <= to_year)]
            df = df['tconst']
            if not df.empty:
                movies_df.append(df)
    movies = concat(movies_df)
    return movies

def get(from_year, to_year):
    return movie_scrapping(from_year, to_year)