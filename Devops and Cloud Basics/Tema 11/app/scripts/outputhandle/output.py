import os, io, csv

def new_file(work_dir):
    file = os.path.join(work_dir, 'data.csv')
    return io.open(file, "w", encoding = 'utf-8', newline = '')

def write_csv(file, tweet_ids):
    with file:
        writer = csv.writer(file)
        for actor, id_list in tweet_ids.items():
            writer.writerow([actor, len(id_list)])

def set(tweet_ids, work_dir):
    file = new_file(work_dir)
    write_csv(file, tweet_ids)
    file.close()