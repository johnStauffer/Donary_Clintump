import json
import pandas
import re
import matplotlib.pyplot as plt
from textblob import TextBlob as tb

# File for response
tweets_data_path = 'data/twitter_data_1.txt'
columns = 5

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue


# Check for word in string passed in
def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False


# Auto percentage with support for showing values in pie chart
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct, v=val)

    return my_autopct


# create DataFrame to simplify manipulation
tweets = pandas.DataFrame()

# adding columns to DataFrame
tweets['country'] = list(
    map(lambda tweet: tweet['place']['full_name'] if tweet['place'] != None else None, tweets_data))
tweets['lang'] = list(map(lambda tweet: tweet['lang'], tweets_data))
tweets['text'] = list(map(lambda tweet: tweet['text'], tweets_data))

tweets['imwithher'] = tweets['text'].apply(lambda tweet: word_in_text('#imwithher', tweet))
tweets['hillary2016'] = tweets['text'].apply(lambda tweet: word_in_text('#hillary2016', tweet))
tweets['trump2016'] = tweets['text'].apply(lambda tweet: word_in_text('#trump2016', tweet))
tweets['votetrump'] = tweets['text'].apply(lambda tweet: word_in_text('#votetrump', tweet))

# Creating pie chart of hashtags
hashtags = ['#imwithher', '#hillary2016', '#trump2016', '#votetrump']
tweets_by_hashtag = [tweets['imwithher'].value_counts()[True],
                     tweets['hillary2016'].value_counts()[True],
                     tweets['trump2016'].value_counts()[True],
                     tweets['votetrump'].value_counts()[True]]

colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
explode = (0.1, 0, 0, 0)  # explode 1st slice

# Setting axis labels and ticks
plt.pie(tweets_by_hashtag, explode=explode, labels=hashtags, colors=colors,
        autopct=make_autopct(tweets_by_hashtag), shadow=True, startangle=140)
plt.axis('equal')
plt.show()

# creating chart of location
tweets_by_location = tweets['country'].value_counts()
print(tweets_by_location)

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Location', fontsize=15)
ax.set_ylabel('Number of tweets', fontsize=15)
ax.set_title('Top 5 locations', fontsize=15, fontweight='bold')
tweets_by_location[:columns].plot(ax=ax, kind='bar', color='red')

# creating chart of languages
tweets_by_language = tweets['lang'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Languages', fontsize=15)
ax.set_ylabel('Number of tweets', fontsize=15)
ax.set_title('Top 5 locations', fontsize=15, fontweight='bold')
tweets_by_language[:columns].plot(ax=ax, kind='bar', color='blue')

input("Press enter to close program")
