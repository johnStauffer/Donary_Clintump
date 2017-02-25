import dbconnection
import sqlite3
from tweet import Tweet
from twitteruser import TwitterUser


class TwitterDao:
    def __init__(self):
        self.connector = dbconnection.SqliteConnector()
        pass

    def create_tweet(self, tweet, twitter_user):
        """
        Persist a tweet to the sqlite database

        :param Tweet tweet:
        :param TwitterUser twitter_user:
        :return:
        """
        insert_tweet_query = 'INSERT INTO tweet(twitter_reference, reply_status_id, reply_user_id, tweet_text, ' \
                             'submit_datetime, user_id, favorites, retweets) ' \
                             'VALUES ({ref}, {rsid}, {ruid}, "{tt}",  {dt},  {uid}, {fv}, {rt});' \
            .format(ref=tweet.user_id,
                    rsid=self.none_to_null(tweet.in_reply_to_status_id),
                    ruid=self.none_to_null(tweet.in_reply_to_user_id),
                    tt=tweet.text,
                    uid=tweet.user_id,
                    dt=tweet.create_datetime,
                    fv=tweet.favorites,
                    rt=tweet.retweets)

        insert_user_query = 'INSERT INTO twitter_user (user_id, user_name, screen_name, location, followers) ' \
                            'VALUES ({id}, "{un}", "{sn}", "{loc}", {fol})' \
                            .format(id=twitter_user.user_id, un=twitter_user.user_name, sn=twitter_user.screen_name,
                                    loc=twitter_user.location, fol=twitter_user.followers)

        commit_sql = 'commit;'

        cursor = self.connector.get_cursor()
        connection = self.connector.conn

        try:
            cursor.execute(insert_user_query)
            connection.commit()
            # cursor.execute(insert_tweet_query)
            connection.close()
        except sqlite3.OperationalError as oe:
            print("Error inserting tweet {}, {}".format(type(oe), oe))
            cursor.close()
        except sqlite3.IntegrityError as ie:
            print("Integrity error {}".format(twitter_user.user_id))
        except AttributeError as ae:
            print("cursor not available")

    def none_to_null(self, object):
        if object == None:
            return 'null'
        else: return object

