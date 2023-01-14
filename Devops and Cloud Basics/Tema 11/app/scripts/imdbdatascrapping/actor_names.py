from pandas import read_csv
import os, absolute

def ordered_names(target_list, id_and_name_list):
    name_list = []
    for target in target_list:
        for id_and_name in id_and_name_list:
            if id_and_name[0] == target:
                name_list.append(id_and_name[1])
                break
    return name_list

def name_scrapping(target_list):
    cols = ['nconst', 'primaryName']
    database = os.path.join(absolute.path(), 'imdbdatascrapping', 'imdbdata', 'name.basics.tsv', 'data.tsv')
    chunksize = 10 ** 4
    id_and_name_list = []

    with read_csv(database, sep = '\t', usecols = cols, dtype = {'primaryName': 'string'}, 
    chunksize = chunksize) as reader:
        for chunk in reader:
            for target in target_list:
                try:
                    absolute_index = chunk.index[chunk['nconst'] == target]
                    relative_index = absolute_index % chunksize
                    name = chunk['primaryName'].values[relative_index]
                    id_and_name = (target, name[0])
                    id_and_name_list.append(id_and_name)
                except:
                    continue
    return ordered_names(target_list, id_and_name_list)

def get(target_list):
    return name_scrapping(target_list)