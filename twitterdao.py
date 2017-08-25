import dbconnection
import sqlite3
from tweet import Tweet
from twitteruser import TwitterUser


class TwitterDao:
    def __init__(self):
        self.connector = dbconnection.SqliteConnector()
        pass

    def create_tweet(self, tweet):
        """
        Persist a tweet to the sqlite database

        :param Tweet tweet:
        :param TwitterUser twitter_user:
        :return:
        """
        insert_tweet_query = 'INSERT INTO tweets(twitter_reference, reply_status_id, reply_user_id, tweet_text, ' \
                             'submit_datetime, user_id, favorites, retweets) ' \
                             'VALUES (?, ?, ?, ?, ?, ?, ?, ?);'

        cursor = self.connector.get_cursor()
        connection = self.connector.conn

        try:
            cursor.execute(insert_tweet_query, (tweet.user_id,
                                                tweet.in_reply_to_status_id,
                                                tweet.in_reply_to_user_id,
                                                tweet.text,
                                                tweet.create_datetime,
                                                tweet.user_id,
                                                tweet.favorites,
                                                tweet.retweets))
            connection.commit()
            connection.close()
        except sqlite3.OperationalError as oe:
            print("Error inserting tweet {}, {}".format(type(oe), oe))
            cursor.close()
        except sqlite3.IntegrityError as ie:
            print("Integrity error {}".format(tweet.user_id))
        except AttributeError as ae:
            print("cursor not available")

    def create_user(self, user):
        """

        :param User user:
        :return:
        """

        insert_user_query = 'INSERT INTO twitter_users (user_id, user_name, screen_name, location, followers) ' \
                            'VALUES (?, ?, ?, ?, ?)'
        cursor = self.connector.get_cursor()
        connection = self.connector.conn
        try:
            cursor.execute(insert_user_query, (user.user_id,
                                               user.user_name,
                                               user.screen_name,
                                               user.location,
                                               user.followers))
            connection.commit()
            connection.close()
        except sqlite3.OperationalError as oe:
            print("Error inserting tweet {}, {}".format(type(oe), oe))
            cursor.close()
        except sqlite3.IntegrityError as ie:
            print("Integrity error {}".format(user.user_id))
        except AttributeError as ae:
            print("cursor not available")

    def none_to_null(self, object):
        if object == None:
            return 'null'
        else:
            return object
