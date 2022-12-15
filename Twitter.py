import tweepy
import pandas as pd 
import json
from datetime import datetime
import s3fs 
import configparser 

#read configs 
config = configparser.ConfigParser()
config.read('config.ini')


def run_twitter_etl():
    access_key = config['twitter']['access_key']
    access_secret = config['twitter']['access_secret']
    consumer_key = config['twitter']['consumer_key']
    consumer_secret = config['twitter']['consumer_secret']




    # Twitter authentication
    auth = tweepy.OAuthHandler(access_key, access_secret)   
    auth.set_access_token(consumer_key, consumer_secret) 

    api = tweepy.API(auth)
    tweets = api.user_timeline(screen_name='@elonmusk', 
                            # 200 is the maximum allowed count
                            count=200,
                            include_rts = False,
                            # Necessary to keep full_text 
                            # otherwise only the first 140 words are extracted
                            tweet_mode = 'extended'
                            )

    #print(tweets[0].created_at)
    tweet_list = []
    for tweet in tweets:
     text = tweet._json["full_text"]
    refined_tweeet = {"user": tweet.user.screen_name,
                        'text' : text,
                        'favorite_count' : tweet.favorite_count,
                        'retweet_count' : tweet.retweet_count,
                        'created_at' : tweet.created_at}
    tweet_list.append(refined_tweeet)
    df = pd.DataFrame(tweet_list)
    df.to_csv("ElonMusk.csv")




    '''for tweet in tweets:
    print(tweet.txt)'''