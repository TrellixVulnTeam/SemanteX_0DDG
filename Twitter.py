from tweepy import *
from Preprocessing import *
import re
import API
LINE = 1


def stream_tweets(fetched_tweets_filename, hash_tag_list):
    consumer_key = API.consumer_key
    consumer_secret = API.consumer_secret
    access_key = API.access_key
    access_secret = API.access_secret
    listener = StdOutListener(fetched_tweets_filename)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    stream = Stream(auth, listener)
    stream.filter(track=hash_tag_list)


def get_list(data):
    regex = re.escape("\"[a-zA-Z]\"")
    print(data.split(regex))
    # return result


class StdOutListener(StreamListener):
    def __init__(self, fetched_tweets_filename):
        super().__init__()
        self.fetched_tweets_filename = fetched_tweets_filename


    def on_data(self, data):
        global LINE
        try:
            get_list(data)
            # print(list_data.get('text'))
            # with open(self.fetched_tweets_filename, 'a') as tf:
            #     tf.write(str(LINE) + str(":  ") + data.split(",")[3] + str("\n"))
            #     LINE += 1
            # return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True


    def on_error(self, status):
        print(status, "error")


if __name__ == '__main__':
    hash_tag_list = ["Apple iPhone 12", "Iphone 12", "Iphone 12 Max Pro", "Iphone", "iPhone"]
    fetched_tweets_filename = "tweets.txt"
    stream_tweets(fetched_tweets_filename, hash_tag_list)