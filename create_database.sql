--  Drop database if it already exists
DROP DATABASE dc_twitter; 

-- Create Database 
CREATE DATABASE dc_twitter; 

-- Use database 
USE dc_twitter; 

-- Table Creation
CREATE TABLE twitter_user (
	user_id bigint NOT NULL UNIQUE, 
    user_name varchar(30), 
    screen_name varchar(30),
    location varchar(140),
    PRIMARY KEY (user_id)
	); 

CREATE TABLE tweets (
	tweet_id bigint NOT NULL AUTO_INCREMENT, 
    tweet_text varchar(140),
    submit_datetime datetime, 
    user_id bigint NOT NULL,
    favorites int,
    retweets int,
    PRIMARY KEY (tweet_id),
    FOREIGN KEY (user_id) REFERENCES twitter_user(user_id)
	);
    
-- Stored Procedures 

-- Insert records for a tweet and user if user does not already exist
DELIMITER // 
USE dc_twitter//
CREATE DEFINER='python'@'localhost' PROCEDURE insertTweetAndUser(
		tweetText varchar(140), 
		submitDatetime datetime, 
		userId bigint, 
		tweetFavorites int, 
		tweetRetweets int,
		userName varchar(30), 
		screenName varchar(30), 
		userLocation varchar(140))
	BEGIN
		INSERT INTO twitter_user (user_id,user_name, screen_name, location) 
			VALUES (userId, userName, screenName, userLocation) 
			ON DUPLICATE KEY UPDATE location = userLocation;
	
		INSERT INTO tweets (tweet_text, submit_datetime, user_id, favorites, retweets)
			VALUES (tweetText, submitDatetime, userId, tweetFavorites, tweetRetweets);
	END //
DELIMITER ; 


