import time
import tweepy
import pandas as pd
from tweepy import OAuthHandler
import API


def initialize_twitter():
    consumer_key = API.consumer_key
    consumer_secret = API.consumer_secret
    access_key = API.access_token
    access_secret = API.access_secret_token
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return auth


def search_tweets(api, search, numTweets):
    tweets = tweepy.Cursor(api.search, q=search, lang="en").items(numTweets)
    tweet_list = []
    for tweet in tweets:
        tweet = {
            'ID': tweet.id,
            'User': tweet.user.screen_name,
            'Tweet': tweet.text,
            'Date': tweet.created_at,
            'Location': tweet.user.location.encode('UTF8'),
            'Device': tweet.source
        }
        tweet_list.append(tweet)
    tweet_df = pd.DataFrame(tweet_list)
    tweet_df.to_excel('dataset.xlsx', sheet_name='Twitter')


if __name__ == "__main__":
    # while True:
    #     try:
    auth = initialize_twitter()
    api = tweepy.API(auth)
    search_tweets(api, ['Iphone 12 Max Pro'], 500)
        # except tweepy.TweepError:
        #     time.sleep(60)
        #     continue
        # except StopIteration:
        #     break