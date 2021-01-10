import Parser_Twitter
import Parser_Web


def collect_data(query, number):
    Parser_Twitter.get_data_from_Twitter(query, number)
    print('Data was obtained from Twitter.')
    Parser_Web.get_data_from_Web(query, number)
    print('Data was obtained from the Web resources.')
