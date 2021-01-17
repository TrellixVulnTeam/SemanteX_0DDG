import tweepy
import pandas as pd
from tweepy import OAuthHandler
import xlsxwriter
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
    places = api.geo_search(query=search, granularity="country")
    tweets = tweepy.Cursor(api.search, places, lang="English").items(numTweets)
    tweet_list = []
    for tweet in tweets:
        tweet = {
            'ID': tweet.id,
            'User': tweet.user.screen_name,
            'Text': tweet.text,
            'Date': tweet.created_at,
            'Location': tweet.user.location.encode('UTF8'),
            'Device': tweet.source
        }
        tweet_list.append(tweet)
    return tweet_list


def create_excel(list):
    tweet_df = pd.DataFrame(list)
    tweet_df.to_excel('dataset.xlsx', sheet_name='Twitter', engine='xlsxwriter')


def get_data_from_Twitter(query, number_of_texts):
    auth = initialize_twitter()
    api = tweepy.API(auth)
    list = search_tweets(api, query, number_of_texts)
    create_excel(list)