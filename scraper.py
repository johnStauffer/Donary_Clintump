import json
import re
import datetime as dt
from textblob import TextBlob as tb
import matplotlib.pyplot as plt
import pandas


class TweetScraper(object):
    def scrape_file(self, tweet_lines):

        """ Iterate through lines of tweet json and return list of tweet tuples

        :param tweet_lines: list of lines from tweets file in json format
        :return list of tweets mapped for relevant fields :
        """
        error_count = 0
        """list to collect tweets in"""
        tweets_map_list = []
        """strip data from each tweet in file """
        for line in tweet_lines:
            tweet_map = {}
            """deserialize json to python tuple"""
            tweet = json.loads(line)
            try:
                """turn string into datetime"""
                datetime = dt.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')
                """map relevant fields"""
                tweet_map['text'] = tweet['text']
                tweet_map['location'] = tweet['user']['location']
                tweet_map['create_datetime'] = datetime
                tweet_map['lang'] = tweet['lang']
                """add tweet map to list"""
                tweets_map_list.append(tweet_map)
            except KeyError as ke:
                """print error to console with exception type"""
                print('Could not map '.format(line, type(ke)))
                """increment error count"""
                error_count += 1
                continue
        print('Completed scraping tweets with {} errors'.format(error_count))
        return tweets_map_list

    def __open_file(self, file_path):
        """ Open a file given a file path and return lines in file as a list

        :param file_path: path of file to be opened
        :return: list of all lines contained in the file specified by file_path
        """
        raw_file = open(file_path)
        """make a list of the lines contained in the file"""
        file = raw_file.readlines()
        return file
