import Parser_Twitter
import Parser_Web


def collect_data(query):
    Parser_Twitter.get_data_from_Twitter(query, 100)
    print('Data was obtained from Twitter.')
    Parser_Web.get_data_from_Web(query, 100)
    print('Data was obtained from Google.')
