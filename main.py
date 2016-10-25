#Import the necessary methods from tweepy library
from tweepy import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API
access_token = "786751877559885825-RZW3hI6ay4eMZZ1Fc1TWZyILnhO1wpC"
access_token_secret = "i3SKuFgtGHLuCLQWo8x1tlapqDFFuY2rbXNCuWovipK1e"
consumer_key = "F9S3jrxWl3gpRkZYdzqrzzliA"
consumer_secret = "Ckf5ScaUVkz8QtHr1AD5r9HAkXnhm4ED9AsMBy52DOgXiV5jEe"

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print (data)
        return True

    def on_error(self, status):
        print (status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['hillary'])