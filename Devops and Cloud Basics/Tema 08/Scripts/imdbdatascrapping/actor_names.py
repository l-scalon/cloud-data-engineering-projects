from pandas import read_csv
import os, absolute

def name_scrapping(target_list):
    cols = ['nconst', 'primaryName']
    database = os.path.join(absolute.path(), 'imdbdatascrapping', 'imdbdata', 'name.basics.tsv', 'data.tsv')
    chunksize = 10 ** 4
    name_list = []

    with read_csv(database, sep = '\t', usecols = cols, dtype = {'primaryName': 'string'}, 
    chunksize = chunksize) as reader:
        for chunk in reader:
            for reference in target_list:
                try:
                    name = chunk['primaryName'].values[chunk.index[chunk['nconst'] == reference]]
                    if not len(name) == 0:
                        name_list.append(name[0])
                except:
                    continue
    print('Name List: Done.')
    return name_list

def get(target_list):
    return name_scrapping(target_list)