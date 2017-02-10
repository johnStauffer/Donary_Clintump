from secrets import DB_HOST, DB_PORT, DB_USER, DB_PW
import pymysql
import datetime


class DataConnector(object):
    def __get_connection(self):
        conn = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            passwd=DB_PW,
            db='dc_twitter',
            charset='utf8'
        )
        return conn

    def get_cursor(self):
        cursor = None
        connection = self.__get_connection()
        if connection:
            cursor = connection.cursor()
        return cursor


class TwitterDataAccessor(object):
    def __init__(self):
        self.dc = DataConnector()

    def create_tweet_record(self,
                            text,
                            submit_datetime,
                            user_id,
                            tweet_favorites,
                            retweets,
                            user_name,
                            screen_name,
                            user_location):
        proc_name = 'dc_twitter.insertTweetAndUser'
        dt = datetime.datetime.strftime(submit_datetime, '%Y-%m-%d %H:%M:%S')
        print(dt)
        tweet_args = [text, submit_datetime, user_id, tweet_favorites, retweets, user_name, screen_name, user_location]
        cursor = self.dc.get_cursor()
        rs = None
        try:
            rs = cursor.callproc(procname=proc_name, args=tweet_args)
        except Exception as inst:
            print(inst)
        finally:
            cursor.close()
        return rs;
