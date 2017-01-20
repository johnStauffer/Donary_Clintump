import json
import datetime as dt
import logging as log


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
            tweets_map_list.append(self.map_tweet(tweet))
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
            tweet_map['location'] = full_tweet_map['user']['location']
            tweet_map['create_datetime'] = datetime
            tweet_map['lang'] = full_tweet_map['lang']
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
