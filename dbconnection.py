import sqlite3

sqlite_file = 'tweet_db.sqlite'


class SqliteConnector(object):
    def __init__(self):
        self.conn = None

    def get_connection(self):
        self.conn = sqlite3.connect(sqlite_file)
        return self.conn

    def get_cursor(self):
        """
        :rtype sqlite3.cursor
        :return: cursor
        """
        cursor = None
        connection = self.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
            except:
                pass
        return cursor

    def close_connection(self):
        try:
            self.conn.commit()
            self.conn.close()
        except:
            pass

    def __del__(self):
        try:
            self.conn.commit()
            self.conn.close()
        except:
            pass



class DbInitializer(object):
    sqlite_file = 'tweet_db.sqlite'

    # Table for tweets
    tweet_table_name = 'tweets'
    tweet_table_sql = 'CREATE TABLE tweets(tweet_id integer primary key autoincrement, twitter_reference bigint, ' \
                      'reply_status_id bigint, reply_user_id bigint, tweet_text varchar(140), submit_datetime datetime, ' \
                      'user_id bigint NOT NULL, favorites int, retweets int, ' \
                      'FOREIGN KEY (user_id) REFERENCES twitter_user(user_id));'
    # Table for users
    user_table_name = 'users'
    user_table_sql = 'CREATE TABLE twitter_users (user_id bigint NOT NULL UNIQUE, user_name varchar(30), ' \
                     'screen_name varchar(30), location varchar(255), followers int, PRIMARY KEY (user_id));'

    hashtag_table_name = 'hashtags'
    hashtag_table_sql = 'CREATE TABLE hashtags (hashtag_id integer primary key autoincrement, text varchar(40), ' \
                        'user_id bigint'

    drop_tweets_sql = 'DROP TABLE IF EXISTS tweet; '
    drop_users_sql = 'DROP TABLE IF EXISTS twitter_user;'
    drop_hashtags_sql = 'DROP TABLE IF EXISTS hashtags'

    def __init__(self):
        self.connector = SqliteConnector()

    def setup_tables(self):
        cursor = self.connector.get_cursor()
        cursor.execute(self.drop_tweets_sql)
        cursor.execute(self.drop_users_sql)
        cursor.execute(self.user_table_sql)
        cursor.execute(self.tweet_table_sql)

if __name__ == '__main__':
    initializer = DbInitializer()
    try:
        initializer.setup_tables()
    except:
        print("Tables have already been initialized")
