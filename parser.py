import json
import pandas
import matplotlib.pyplot as plt

# File for response
tweets_data_path = 'data/twitter_data_el16.txt'
columns = 5

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue

print(len(tweets_data))

# create DataFrame to simplify manipulation
tweets = pandas.DataFrame()
# adding columns to DataFrame
tweets['country'] = list(map(lambda tweet: tweet['place']['full_name'] if tweet['place'] != None else None, tweets_data))

# creating char of location
tweets_by_location = tweets['country'].value_counts()
print(tweets_by_location)

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Languages', fontsize=15)
ax.set_ylabel('Number of tweets', fontsize=15)
ax.set_title('Top 5 locations', fontsize=15, fontweight='bold')
tweets_by_location[:columns].plot(ax=ax, kind='bar', color='red')

input("Press enter to close program")
