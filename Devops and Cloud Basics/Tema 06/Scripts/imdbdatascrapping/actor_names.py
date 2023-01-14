import pandas as pd
import os, absolute

def name_scrapping(target_list):
    database = os.path.join(absolute.path(), 'imdbdatascrapping', 'imdbdata', 'name.basics.tsv', 'data.tsv')
    df = pd.read_csv(database, sep = '\t')
    name_list = []
    for reference in target_list:
        name = df['primaryName'].values[df.index[df['nconst'] == reference]]
        name_list.append(name[0])
    return name_list

def get(target_list):
    return name_scrapping(target_list)