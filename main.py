# Import the necessary methods from tweepy library
from tweepy import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Credentials for Twitter api
access_token = "786751877559885825-RZW3hI6ay4eMZZ1Fc1TWZyILnhO1wpC"
access_token_secret = "i3SKuFgtGHLuCLQWo8x1tlapqDFFuY2rbXNCuWovipK1e"
consumer_key = "F9S3jrxWl3gpRkZYdzqrzzliA"
consumer_secret = "Ckf5ScaUVkz8QtHr1AD5r9HAkXnhm4ED9AsMBy52DOgXiV5jEe"

# This is list of words that will filter the twitter stream
filter_keys = ['#imwithher', 'hillary2016', 'trump2016', 'votetrump']

# Setting up file for tweets to be stored
twitter_data_path = 'data/twitter_data_1.txt'
twitter_data_store = open(twitter_data_path, 'w+')


# Print to StdOut
class StdOutListener(StreamListener):
    def on_data(self, data):
        twitter_data_store.write(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    # Twitter api authentication
    l = StdOutListener()

    # This handles authentication
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    # Filter stream of tweets with list of keywords
    stream.filter(track=filter_keys)
