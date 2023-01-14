from datahandle import data, names, folder_structure
from twitterapi import tweets
from pagebuild import page
import randfacts

def main():
    folder_structure.create()
    data.download()
    print('\nFetching some data. It may take a while.')
    print('Did you know? ' + randfacts.get_fact() + '\n')
    tweet_ids = tweets.get(names.get())
    page.build(tweet_ids)
    data.remove()
    print('\nSuccess!')

if __name__ == '__main__':
    main()