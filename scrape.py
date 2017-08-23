import json
import datetime as dt
import logging as log
from tweet import Tweet
from twitteruser import TwitterUser


class TweetScraperService(object):
    def scrape_file(self, file_path):
        """deserialize file of json tweets and return list<map> with relevant fields

        :rtype: list
        :param file_path: filepath to file of json tweets
        :return: tweet_list: list of tweet maps with relevant fields. If file cannot be opened return None
        """
        try:
            """open file specified in file_path """
            file_lines = self.__open_file(file_path)
        except IOError as io:
            """If file cannot be opened return None"""
            return None
        """serialize list of lines to a list of tweet maps """
        tweet_list = self.scrape_tweet_lines(file_lines)
        return tweet_list

    def scrape_tweet_lines(self, raw_tweet_lines):

        """ Iterate through lines of tweet json and return list of tweet maps

        :param raw_tweet_lines: list of lines from tweets file in json format
        :return list of tweets mapped for relevant fields :
        """
        error_count = 0
        """list to collect tweets in"""
        tweets_map_list = []
        """strip data from each tweet in file """
        for line in raw_tweet_lines:
            """strip relevant fields and make map"""
            mapped_tweet = self.map_tweet_user(line)
            tweets_map_list.append(mapped_tweet)
        return tweets_map_list

    @staticmethod
    def deserialize_tweet(raw_tweet):
        """
        :param raw_tweet:
        :return Tweet:

        """
        tweet = Tweet()
        full_tweet = json.loads(raw_tweet)
        datetime = dt.datetime.strptime(full_tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')

        try:
            """map relevant fields to object"""
            tweet.text = full_tweet['text']
            tweet.create_datetime = datetime
            tweet.favorites = full_tweet['user']['favourites_count']
            tweet.retweets = full_tweet['retweet_count']
            tweet.in_reply_to_status_id = full_tweet['in_reply_to_status_id']
            tweet.in_reply_to_user_id = full_tweet['in_reply_to_user_id']
            tweet.user_id = full_tweet['user']['id']
        except KeyError as ke:
            log.warning('Could not map tweet: '.format(ke))
        return tweet

    @staticmethod
    def deserialize_user(raw_tweet):
        """
        :param raw_tweet:
        :return TwitterUser:
        """
        user = TwitterUser()
        full_tweet = json.loads(raw_tweet)
        try:
            user.user_id = full_tweet['user']['id']
            user.user_name = full_tweet['user']['name']
            user.screen_name = full_tweet['user']['screen_name']
            user.location = full_tweet['user']['location']
            user.followers = full_tweet['user']['followers_count']
        except KeyError as ke:
            log.warning('Could not map user: '.format(ke))
        return user

    def map_tweet_user(self, full_tweet):
        """process a tweet tuple and map relevant fields

        :rtype namedtuple{Tweet, TwitterUser}
        :param full_tweet: tweet as text
        :return: map of a Tweet and TwitterUser
        """
        tweet_user_map = {}
        tweet_user_map['tweet'] = self.deserialize_tweet(full_tweet)
        tweet_user_map['user'] = self.deserialize_user(full_tweet)
        return tweet_user_map

    def __open_file(self, file_path):
        """ Open a file given a file path and return lines in file as a list

        :rtype: list
        :param file_path: path of file to be opened
        :return: list of all lines contained in the file specified by file_path
        :except: IOError: if file_path is incorrect or file cannot be opened
        """
        try:
            """open file from given filepath"""
            raw_file = open(file_path)
            """make a list of the lines contained in the file"""
            file = raw_file.readlines()
            return file
        except IOError as io:
            log.warning("Could not open {}\n {}".format(file_path, type(io)))
            raise io


if __name__ == '__main__':
    file_path = 'data/twitter_data.txt'
    scraper_service = TweetScraperService()
    tweet_list = scraper_service.scrape_file(file_path)
    print(tweet_list)
