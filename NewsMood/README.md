

```python
#Dependencies
import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import time #may not be needed
import tweepy #pip install tweepy


#import vader sentiment intensity analyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer #pip install vaderSentiment
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


```


```python
#test: get example of tweepy output

testTweet = api.user_timeline('@BBC', count=1, result_type='recent')
for tweet in testTweet:
    test = tweet._json
    print(test)
```

    {'created_at': 'Wed Dec 13 20:00:10 +0000 2017', 'id': 941035033632104448, 'id_str': '941035033632104448', 'text': "London's Euston station will be turned into a shelter for the homeless on Christmas Day. ❤️️🎁… https://t.co/Y834ULzLu5", 'truncated': True, 'entities': {'hashtags': [], 'symbols': [], 'user_mentions': [], 'urls': [{'url': 'https://t.co/Y834ULzLu5', 'expanded_url': 'https://twitter.com/i/web/status/941035033632104448', 'display_url': 'twitter.com/i/web/status/9…', 'indices': [95, 118]}]}, 'source': '<a href="http://www.radian6.com" rel="nofollow">Radian6 -Social Media Management</a>', 'in_reply_to_status_id': None, 'in_reply_to_status_id_str': None, 'in_reply_to_user_id': None, 'in_reply_to_user_id_str': None, 'in_reply_to_screen_name': None, 'user': {'id': 19701628, 'id_str': '19701628', 'name': 'BBC', 'screen_name': 'BBC', 'location': 'TV. Radio. Online', 'description': 'Our mission is to enrich your life and to inform, educate and entertain you, wherever you are.', 'url': 'http://t.co/9Yv7DJ1Pmu', 'entities': {'url': {'urls': [{'url': 'http://t.co/9Yv7DJ1Pmu', 'expanded_url': 'http://www.bbc.co.uk', 'display_url': 'bbc.co.uk', 'indices': [0, 22]}]}, 'description': {'urls': []}}, 'protected': False, 'followers_count': 1154661, 'friends_count': 160, 'listed_count': 9289, 'created_at': 'Thu Jan 29 08:30:16 +0000 2009', 'favourites_count': 3594, 'utc_offset': 0, 'time_zone': 'London', 'geo_enabled': False, 'verified': True, 'statuses_count': 20422, 'lang': 'en', 'contributors_enabled': False, 'is_translator': False, 'is_translation_enabled': False, 'profile_background_color': '000000', 'profile_background_image_url': 'http://pbs.twimg.com/profile_background_images/459267803640385537/QkzQGfqX.jpeg', 'profile_background_image_url_https': 'https://pbs.twimg.com/profile_background_images/459267803640385537/QkzQGfqX.jpeg', 'profile_background_tile': False, 'profile_image_url': 'http://pbs.twimg.com/profile_images/662708106/bbc_normal.png', 'profile_image_url_https': 'https://pbs.twimg.com/profile_images/662708106/bbc_normal.png', 'profile_banner_url': 'https://pbs.twimg.com/profile_banners/19701628/1512226202', 'profile_link_color': '000000', 'profile_sidebar_border_color': '000000', 'profile_sidebar_fill_color': 'DDEEF6', 'profile_text_color': '333333', 'profile_use_background_image': False, 'has_extended_profile': False, 'default_profile': False, 'default_profile_image': False, 'following': False, 'follow_request_sent': False, 'notifications': False, 'translator_type': 'regular'}, 'geo': None, 'coordinates': None, 'place': None, 'contributors': None, 'is_quote_status': False, 'retweet_count': 29, 'favorite_count': 97, 'favorited': False, 'retweeted': False, 'possibly_sensitive': False, 'lang': 'en'}
    


```python
# *** Creating dataframe of tweet sentimentality and other twitter info. 
target = ['@BBC', '@CBS', '@CNN', '@FoxNews', '@nytimes']
newsMood_df = pd.DataFrame(columns = ['Handle', 'Compound Score', 'Positivity Score',\
                                      'Neutrality Score', 'Negativity Score'])

#loop through target users and get 100 most recent tweets from each
    #note: rate limit seems to be 900 requests every 15 mins
for user in target:
    user_ls = []
    compound_ls = []
    pos_ls = []
    neu_ls = []
    neg_ls = []
    text_ls = []
    time_ls = [] #time created 
    tweetsAgo_ls = [] # ranking of the latest tweet ( == the latest, 100 == 100th tweet in the past)
    
    counter = 0
    
    #test using 5 tweets first
    publicTweets = api.user_timeline(user, count=100, result_type="recent")
        #Should be sorted by latest tweets
        
    # loop through each tweet for a user 
    for tweet in publicTweets:
        # vader analyze sentiments for each tweet
        compound = analyzer.polarity_scores(tweet._json['text'])['compound']
        pos = analyzer.polarity_scores(tweet._json['text'])['pos']
        neu = analyzer.polarity_scores(tweet._json['text'])['neu']
        neg = analyzer.polarity_scores(tweet._json['text'])['neg']
        #get text of tweet
        text = tweet._json['text']
        #get time tweet was posted
        time = tweet._json['created_at']
        #counter decrease by one
        counter -= 1
        
        # Add each value to the appropriate list
        #list of just the current user 
        user_ls.append(user)
        compound_ls.append(compound)
        pos_ls.append(pos)
        neu_ls.append(neu)
        neg_ls.append(neg)
        text_ls.append(text)
        time_ls.append(time)
        tweetsAgo_ls.append(counter)
        
    # Create temporary dataframe to store those values    
    df = pd.DataFrame() 
    df['Handle'] = user_ls
    df['Timestamp'] = time_ls
    df['Compound Score'] = compound_ls
    df['Positivity Score'] = pos_ls
    df['Neutrality Score'] = neu_ls
    df['Negativity Score'] = neg_ls
    df['Text'] = text_ls
    df['Tweets Ago'] = tweetsAgo_ls
    
    #append temp df to end of newsMood_df
    newsMood_df = newsMood_df.append(df)
        

df.head(20)
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Handle</th>
      <th>Timestamp</th>
      <th>Compound Score</th>
      <th>Positivity Score</th>
      <th>Neutrality Score</th>
      <th>Negativity Score</th>
      <th>Text</th>
      <th>Tweets Ago</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>@nytimes</td>
      <td>Wed Dec 13 22:47:07 +0000 2017</td>
      <td>-0.1779</td>
      <td>0.094</td>
      <td>0.787</td>
      <td>0.120</td>
      <td>RT @RaR: We've seen the vigils and makeshift m...</td>
      <td>-1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>@nytimes</td>
      <td>Wed Dec 13 22:32:09 +0000 2017</td>
      <td>0.0000</td>
      <td>0.000</td>
      <td>1.000</td>
      <td>0.000</td>
      <td>Secrets of ancient Mars might be found on a ne...</td>
      <td>-2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>@nytimes</td>
      <td>Wed Dec 13 22:17:02 +0000 2017</td>
      <td>0.0000</td>
      <td>0.000</td>
      <td>1.000</td>
      <td>0.000</td>
      <td>The Federal Reserve chair (don’t call her “cha...</td>
      <td>-3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>@nytimes</td>
      <td>Wed Dec 13 22:00:17 +0000 2017</td>
      <td>-0.0516</td>
      <td>0.125</td>
      <td>0.703</td>
      <td>0.172</td>
      <td>Salma Hayek on Harvey Weinstein, in @nytopinio...</td>
      <td>-4</td>
    </tr>
    <tr>
      <th>4</th>
      <td>@nytimes</td>
      <td>Wed Dec 13 21:50:07 +0000 2017</td>
      <td>-0.1987</td>
      <td>0.149</td>
      <td>0.537</td>
      <td>0.315</td>
      <td>It's by no means an exhaustive list. So yeah, ...</td>
      <td>-5</td>
    </tr>
    <tr>
      <th>5</th>
      <td>@nytimes</td>
      <td>Wed Dec 13 21:40:03 +0000 2017</td>
      <td>0.0000</td>
      <td>0.000</td>
      <td>1.000</td>
      <td>0.000</td>
      <td>RT @NYTNational: "We knew the world was lookin...</td>
      <td>-6</td>
    </tr>
    <tr>
      <th>6</th>
      <td>@nytimes</td>
      <td>Wed Dec 13 21:30:27 +0000 2017</td>
      <td>-0.5574</td>
      <td>0.000</td>
      <td>0.816</td>
      <td>0.184</td>
      <td>What’s "Star Wars" without its critters, creat...</td>
      <td>-7</td>
    </tr>
    <tr>
      <th>7</th>
      <td>@nytimes</td>
      <td>Wed Dec 13 21:20:07 +0000 2017</td>
      <td>-0.2960</td>
      <td>0.000</td>
      <td>0.761</td>
      <td>0.239</td>
      <td>No packet full of mystery ingredients necessar...</td>
      <td>-8</td>
    </tr>
    <tr>
      <th>8</th>
      <td>@nytimes</td>
      <td>Wed Dec 13 21:10:11 +0000 2017</td>
      <td>0.6369</td>
      <td>0.208</td>
      <td>0.792</td>
      <td>0.000</td>
      <td>RT @AKannapell: What We’re Reading: the best o...</td>
      <td>-9</td>
    </tr>
    <tr>
      <th>9</th>
      <td>@nytimes</td>
      <td>Wed Dec 13 21:04:01 +0000 2017</td>
      <td>0.0000</td>
      <td>0.000</td>
      <td>1.000</td>
      <td>0.000</td>
      <td>@nytopinion Salma Hayek escribe sobre Harvey W...</td>
      <td>-10</td>
    </tr>
    <tr>
      <th>10</th>
      <td>@nytimes</td>
      <td>Wed Dec 13 21:00:05 +0000 2017</td>
      <td>-0.3182</td>
      <td>0.000</td>
      <td>0.777</td>
      <td>0.223</td>
      <td>"We lost about 80% of our avocado crop" https:...</td>
      <td>-11</td>
    </tr>
    <tr>
      <th>11</th>
      <td>@nytimes</td>
      <td>Wed Dec 13 20:50:02 +0000 2017</td>
      <td>0.3400</td>
      <td>0.112</td>
      <td>0.888</td>
      <td>0.000</td>
      <td>Oaths of office can be taken on a Hebrew Bible...</td>
      <td>-12</td>
    </tr>
    <tr>
      <th>12</th>
      <td>@nytimes</td>
      <td>Wed Dec 13 20:40:12 +0000 2017</td>
      <td>-0.0516</td>
      <td>0.174</td>
      <td>0.606</td>
      <td>0.220</td>
      <td>Walmart will allow workers to get pay before p...</td>
      <td>-13</td>
    </tr>
    <tr>
      <th>13</th>
      <td>@nytimes</td>
      <td>Wed Dec 13 20:30:11 +0000 2017</td>
      <td>-0.8225</td>
      <td>0.056</td>
      <td>0.602</td>
      <td>0.342</td>
      <td>RT @nytimesworld: President Jacob Zuma of Sout...</td>
      <td>-14</td>
    </tr>
    <tr>
      <th>14</th>
      <td>@nytimes</td>
      <td>Wed Dec 13 20:20:18 +0000 2017</td>
      <td>0.5994</td>
      <td>0.274</td>
      <td>0.726</td>
      <td>0.000</td>
      <td>How the Fed rate increase affects your mortgag...</td>
      <td>-15</td>
    </tr>
    <tr>
      <th>15</th>
      <td>@nytimes</td>
      <td>Wed Dec 13 20:10:05 +0000 2017</td>
      <td>0.0000</td>
      <td>0.000</td>
      <td>1.000</td>
      <td>0.000</td>
      <td>A search for “Kill Bill” turns up results for ...</td>
      <td>-16</td>
    </tr>
    <tr>
      <th>16</th>
      <td>@nytimes</td>
      <td>Wed Dec 13 20:00:20 +0000 2017</td>
      <td>0.2732</td>
      <td>0.129</td>
      <td>0.871</td>
      <td>0.000</td>
      <td>RT @timesinsider: “I want everything we do to ...</td>
      <td>-17</td>
    </tr>
    <tr>
      <th>17</th>
      <td>@nytimes</td>
      <td>Wed Dec 13 19:50:04 +0000 2017</td>
      <td>-0.6908</td>
      <td>0.000</td>
      <td>0.695</td>
      <td>0.305</td>
      <td>Here’s a new way to fight back attempts to spr...</td>
      <td>-18</td>
    </tr>
    <tr>
      <th>18</th>
      <td>@nytimes</td>
      <td>Wed Dec 13 19:40:11 +0000 2017</td>
      <td>0.5574</td>
      <td>0.235</td>
      <td>0.765</td>
      <td>0.000</td>
      <td>Republican leaders have reached an agreement o...</td>
      <td>-19</td>
    </tr>
    <tr>
      <th>19</th>
      <td>@nytimes</td>
      <td>Wed Dec 13 19:36:20 +0000 2017</td>
      <td>0.2500</td>
      <td>0.153</td>
      <td>0.741</td>
      <td>0.106</td>
      <td>RT @jasondhorowitz: Naples goes nuts as Unesco...</td>
      <td>-20</td>
    </tr>
  </tbody>
</table>
</div>




```python
#data massage newsMood_df

#converts 'Timestamp' from string into datetime object
newsMood_df['Timestamp'] = pd.to_datetime(newsMood_df['Timestamp'])

# save newsMood_df to csv file in same folder
newsMood_df.to_csv('newsMood_dataframe.csv')

newsMood_df.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Compound Score</th>
      <th>Handle</th>
      <th>Negativity Score</th>
      <th>Neutrality Score</th>
      <th>Positivity Score</th>
      <th>Text</th>
      <th>Timestamp</th>
      <th>Tweets Ago</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.0000</td>
      <td>@BBC</td>
      <td>0.000</td>
      <td>1.000</td>
      <td>0.000</td>
      <td>London's Euston station will be turned into a ...</td>
      <td>2017-12-13 20:00:10</td>
      <td>-1.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.3384</td>
      <td>@BBC</td>
      <td>0.000</td>
      <td>0.854</td>
      <td>0.146</td>
      <td>🐘 Why you must never pee in front of elephants...</td>
      <td>2017-12-13 19:31:04</td>
      <td>-2.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.2263</td>
      <td>@BBC</td>
      <td>0.000</td>
      <td>0.917</td>
      <td>0.083</td>
      <td>It’s spicy, it's tangy &amp;amp; it'll warm you ri...</td>
      <td>2017-12-13 19:00:02</td>
      <td>-3.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-0.4215</td>
      <td>@BBC</td>
      <td>0.189</td>
      <td>0.811</td>
      <td>0.000</td>
      <td>Princess Margaret broke all the royal rules lo...</td>
      <td>2017-12-13 18:32:04</td>
      <td>-4.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.1280</td>
      <td>@BBC</td>
      <td>0.000</td>
      <td>0.919</td>
      <td>0.081</td>
      <td>Còsagach: A feeling of being snug, sheltered o...</td>
      <td>2017-12-13 18:00:12</td>
      <td>-5.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
# *** Scatterplot of tweets and compound scores ***
#note: Retweets are included as a tweet
fig, ax = plt.subplots()
sns.set_style('darkgrid')
fig = sns.lmplot('Tweets Ago', 'Compound Score', data=newsMood_df, hue='Handle', size=10, fit_reg=False)

# Scatterplot labels
    # get date for use in title
latestTime = pd.Timestamp.now() #gets current time in current timezone
latestDate = latestTime.date() #gets the date from the current time  
plt.title('Sentiments of the Last 100 Tweets of Several Top News Organizations' + ' (' +\
          str(latestDate) + ' GMT)', fontsize=18)
# draw line at y=0
plt.axhline(0, color='grey')

#set fontsize
plt.xlabel('Tweets Ago', fontsize=15)
plt.ylabel('VaderSentiment Compound Scores [-1, 1]', fontsize=15)

#add note at bottom
#ax.annotate("note: Retweets are counted.", xy=[-100, -1.00], xytext=(-100, -1.00), textcoords='data', size=20)
fig.fig.text(0, 0, "*Note: Retweets are counted.")

#save as png file
fig.savefig('Sentiments_100Tweets_News_Orgs.png')
    
plt.show()
    
```


![png](output_4_0.png)



![png](output_4_1.png)



```python
# *** Bar plot visualizing the _overall_ sentiments of the last 100 tweets from each organization. ***

#group by twitter handles and the average values of each column
MoodAvgs_group = newsMood_df.groupby('Handle').mean()

#set fig size
fig, ax = plt.subplots()
    # the size of A4 paper
fig.set_size_inches(11.7, 8.27)

# Seaborn barplot 
sns.barplot(x=MoodAvgs_group.index , y='Compound Score' , data=MoodAvgs_group)

#add annotations for each graph
for p in ax.patches: # loops through each bar or "patch" I think
    if p.get_height() > 0:
        ax.annotate(str(p.get_height()), (p.get_x() + .25, 0.01), size=12)
    else:
        ax.annotate(str(p.get_height()), (p.get_x() + .25, -0.015), size=12)

# draw line at y=0
plt.axhline(0, color='steelblue')

# Create labels
plt.title('Overall Sentiments of the Last 100 Tweets' + ' (' + str(latestDate) + ' GMT)', fontsize = 15)
plt.xlabel('Twitter Handles of Select News Organizations', fontsize=12)
plt.ylabel('Average VaderSentiment Compound Scores (range: [-1, 1])', fontsize=12)

#save as png file
fig.savefig('Sentiments_OverallTweets_News_Orgs.png')

plt.show()
```


![png](output_5_0.png)

