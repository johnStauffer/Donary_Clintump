from twitterdao import TwitterDao
from scrape import TweetScraperService

class TweetService(object):
    def __init__(self):
        self.dao = TwitterDao()

    def create_tweet(self, tweet):
        return self.dao.create_tweet(tweet)

    def create_user(self, user):
        return self.dao.create_user(user)
