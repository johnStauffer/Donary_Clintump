import secrets
from threading import Thread
from tweepy import StreamListener, OAuthHandler, Stream

# This is list of words that will filter the twitter stream

# Setting up file for tweets to be stored
twitter_data_path = 'data/twitter_data.txt'
twitter_data_store = open(twitter_data_path, 'a+')


# Print tweets to text file
class StdOutListener(StreamListener):
    def __init__(self):
        self.count = 0

    def on_data(self, data):
        # Write data to file
        twitter_data_store.write(data)
        print(data)
        return True

    def on_error(self, status):
        print(status)


class TwitterApiService(object):
    def __init__(self):
        """Initialize twitter streaming api"""

        """ Create authentication object with consumer keys
            *** Credentials are stored in secrets.py file outside of version control ***
        """
        self.auth = OAuthHandler(secrets.CONSUMER_KEY, secrets.CONSUMER_SECRET)
        """ Add API access tokens to authentication object """
        self.auth.set_access_token(secrets.ACCESS_TOKEN, secrets.ACCESS_TOKEN_SECRET)
        """ Authenticate and initialize stream """

        """ Initialize listener for collecting tweets"""
        self.listener = StdOutListener()

    def threaded_stream(self, filter_keys):
        """ Stream twitter api and filter by list of keys

        :param filter_keys:
        :return:
        """

        def my_stream(filter_keys):
            """
            :param filter_keys: list of keys to filter tweets by
            :return:
            """
            try:
                """ Stream tweets to listener """
                self.stream = Stream(self.auth, self.listener)
                """ Filter stream with list of keys"""
                self.stream.filter(track=filter_keys)
            except Exception as inst:
                print("error in stream: {}".format(inst))
                return None

        thread = Thread(target=my_stream, args=(filter_keys,))
        thread.start()
        return thread


if __name__ == '__main__':
    filter_keys = ['#imwithher', 'hillary2016', 'trump2016', '#votetrump', '#feelthebern']
    apiService = TwitterApiService()
    thread = apiService.threaded_stream(filter_keys)
    thread._stop()
