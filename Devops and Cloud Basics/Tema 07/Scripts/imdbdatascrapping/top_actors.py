import pandas as pd

def casting_count(actors, target):
    df = pd.DataFrame(actors)
    return df['nconst'].value_counts().index.tolist()[:target]

def get(actors, target):
    return casting_count(actors, target)