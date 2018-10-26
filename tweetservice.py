from twitterdao import TwitterDao

class TweetService(object):
    def __init__(self):
        self.dao = TwitterDao()

    def create_tweet(self, tweet):
        return self.dao.create_tweet(tweet)

    def create_user(self, user):
        return self.dao.create_user(user)

    def create_hashtag(self, hashtag):
        return
