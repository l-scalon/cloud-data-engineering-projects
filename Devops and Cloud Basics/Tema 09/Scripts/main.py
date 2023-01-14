from datahandle import data, names
from twitterapi import tweets
from pagebuild import page
import randfacts

def main():
    data.download()
    print('\nFetching some data. It may take a while.')
    print('Did you know? ' + randfacts.get_fact() + '\n')
    tweet_ids = tweets.get(names.get())
    page.build(tweet_ids)
    data.remove()

if __name__ == '__main__':
    main()