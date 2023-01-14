from .auth import *
import tweepy
from outputhandle import log
from os import environ

def auth():
    auth = tweepy.OAuthHandler(API_Key, API_Key_Secret)
    auth.set_access_token(Access_Token, Access_Token_Secret)
    return auth

def api():
    return tweepy.API(auth(), wait_on_rate_limit = True)

def tweet_scrapping(search_parameters):
    tweet_ids = {}
    total_results = 0
    for name in search_parameters:
        ids = []
        results = [status._json for status in tweepy.Cursor(api().search_tweets, q = name + '-filter:retweets', tweet_mode='extended').items(100)]
        log.info(name, len(results))
        total_results += len(results)
        for result in results:
            ids.append(result['id_str'])
        tweet_ids[name] = ids
    log.total(total_results)
    return tweet_ids


def get(search_parameters):
    return tweet_scrapping(search_parameters)