#Dependencies
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import tweepy
import json

#import vader sentiment intensity analyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

#set authorization keys and secrets
#edit this out to keep keys secret and whatnot...
consumer_key = 'slkeKRpO4wPsytrmYu1EuDmdY'
consumer_secret =  'cm0rML2nllTdyjgMiJTCrL0FC7YmuskWotb1K12ltQ5imys6qJ'
access_token = '77581674-vJ8yVYXJq3K55L2IqzEaWyBjiD13ECnIjPanNZhw7'
access_token_secret =  'y69VBgQDKiBWGmOZYF61tpCsHAS5otcIrG1qmePyvAG6u'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

target = ['@BBC', '@CBS', '@CNN', '@FoxNews', '@nytimes']

#loop through target users and get 100 most recent tweets from each

for user in target:
    compound_ls = []

    #test using 10 tweets first
    publicTweets = api.user_timeline(user, count=10, result_type="recent")

    # loop through each tweet for a user 
    for tweet in publicTweets:
        # vader analyze sentiments for each tweet
        compound = analyzer.polarity_scores(tweet['text'])['compound']
        # Add each value to the appropriate list
        compound_ls.append(compound)

       

        
