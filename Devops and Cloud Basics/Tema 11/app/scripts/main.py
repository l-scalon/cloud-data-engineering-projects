from datahandle import data, names, folder_structure
from twitterapi import tweets
from outputhandle import page, output

def main():
    folder_structure.create()
    data.download()
    actors_names = names.get()
    work_dir = folder_structure.new()
    tweet_ids = tweets.get(actors_names)
    output.set(tweet_ids, work_dir)
    page.build(tweet_ids, work_dir)
    data.remove()

if __name__ == '__main__':
    main()