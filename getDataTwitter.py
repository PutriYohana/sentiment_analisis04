import tweepy
import configparser
import pandas as pd


# read configs
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

# authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


class Listener(tweepy.Stream):

    tweets = []
    limit = 10000
    def on_status(self, status):
        self.tweets.append(status)
        print(status.user.screen_name + ": " + status.text)

        if len(self.tweets) == self.limit:
            self.disconnect()






stream_tweet = Listener(api_key, api_key_secret, access_token, access_token_secret)

# stream by keywords
keywords = ['Trending', '#music']

stream_tweet.filter(track=keywords,languages=['en'])


# Create DataFrame

columns= ['User','Tweet']
data = []

for tweet in stream_tweet.tweets:
    if not tweet.truncated:
        print(tweet.user.screen_name + '|' + tweet.text )
        data.append([tweet.user.screen_name, tweet.text])
    else:
        print(tweet.user.screen_name + '|' + tweet.text )
        data.append([tweet.user.screen_name, tweet.extended_tweet['full_text']])

df = pd.DataFrame(data, columns = columns)
df.to_csv('data_tweet_music.csv',index=False)
print("Udah kelar brads!!!")