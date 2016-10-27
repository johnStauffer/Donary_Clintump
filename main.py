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
filter_keys = ['#imwithher', 'hillary2016', 'trump2016', '#votetrump', '#feelthebern']

# Setting up file for tweets to be stored
twitter_data_path = 'data/twitter_data.txt'
twitter_data_store = open(twitter_data_path, 'a+')

# Colors for coloring StdOut output
class bcolors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[31m'
    ENDC = '\033[0m'


# Print tweets to text file
class StdOutListener(StreamListener):
    def __init__(self):
        self.count = 0

    def on_data(self, data):
        # Write data to file
        twitter_data_store.write(data)
        # Incrementally print number of tweets to StdOut
        if self.count % 50 == 0:
            print(str.format('Tweets: \033[92m{}\033[0m', self.count))
        self.count += 1
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
    print(bcolors.YELLOW+'Streaming...'+bcolors.ENDC)
    stream.filter(track=filter_keys)
