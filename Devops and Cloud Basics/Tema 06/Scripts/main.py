from download import *
from names import *
from twitterapi import tweets
from pagebuild import page
import randfacts

def main():
    download()
    print('\nFetching some data. It may take a while.')
    print('Did you know? ' + randfacts.get_fact() + '\n')
    tweet_ids = tweets.get(get_names())
    page.build(tweet_ids)
            
if __name__ == "__main__":
    main()