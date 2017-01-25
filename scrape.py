import json
import datetime as dt
import logging as log
from datahandler import TwitterDataAccessor


class TweetScraperService(object):
    def __init__(self):
        self.tda = TwitterDataAccessor()

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

    def scrape_tweet_lines(self, tweet_lines):

        """ Iterate through lines of tweet json and return list of tweet maps

        :param tweet_lines: list of lines from tweets file in json format
        :return list of tweets mapped for relevant fields :
        """
        error_count = 0
        """list to collect tweets in"""
        tweets_map_list = []
        """strip data from each tweet in file """
        for line in tweet_lines:
            """deserialize json to python tuple"""
            tweet = json.loads(line)
            """strip relevant fields and make map"""
            mapped_tweet = self.map_tweet(tweet)
            tweets_map_list.append(mapped_tweet)
            rs = self.tda.create_tweet_record(mapped_tweet['text'], mapped_tweet['create_datetime'], mapped_tweet['user_id'],
                                         mapped_tweet['favorites'], mapped_tweet['retweet_count'], mapped_tweet['user_name'],
                                         mapped_tweet['screen_name'], mapped_tweet['location'])
        return tweets_map_list


    def map_tweet(self, full_tweet_map):
        """process a tweet tuple and map relevant fields

        :rtype map
        :param full_tweet_map: full tuple loaded from json of tweet
        :return: map of relevant tweet fields
        """
        tweet_map = {}
        """turn string into datetime"""
        datetime = dt.datetime.strptime(full_tweet_map['created_at'], '%a %b %d %H:%M:%S %z %Y')
        try:
            """map relevant fields"""
            tweet_map['text'] = full_tweet_map['text']
            tweet_map['create_datetime'] = datetime
            tweet_map['user_id'] = full_tweet_map['user']['id']
            tweet_map['user_name'] = full_tweet_map['user']['name']
            tweet_map['location'] = full_tweet_map['user']['location']
            tweet_map['screen_name'] = full_tweet_map['user']['screen_name']
            tweet_map['favorites'] = full_tweet_map['user']['favourites_count']
            # TODO Figure out how to process retweets
            tweet_map['retweet_count'] = None
        except KeyError as ke:
            log.warning('Could not map tweet: '.format(ke))
        return tweet_map

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
