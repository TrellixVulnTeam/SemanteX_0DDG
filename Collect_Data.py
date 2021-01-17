import Parser_Twitter
import Parser_Google


def collect_data(query):
    Parser_Twitter.get_data_from_Twitter(query, 200)
    print('Data was obtained from Twitter.')
    """The google search require to fix several bugs, that's why I turned off collection of data from google, 
    while I eliminate all errors. """
    # Parser_Google.get_data_from_Web(query, 25)
    # print('Data was obtained from Google.')
