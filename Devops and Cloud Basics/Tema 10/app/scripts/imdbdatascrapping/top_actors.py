from pandas import DataFrame

def casting_count(actors, target):
    df = DataFrame(actors)
    counting = df['nconst'].value_counts().index.tolist()[:target]
    print('Counting: Done!')
    return counting

def get(actors, target):
    return casting_count(actors, target)