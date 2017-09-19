# Import Dependencies
import tweepy
import time
import datetime
import json
import random
import pandas as pandas
import matplotlib.pyplot as plt
import seaborn as sns
import sys
#from textblob import TextBlob (figure this out)
import numpy as np

# Import and Initialize Sentiment Analyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

# Twitter API Keys
consumer_key = "1kiIH7jZF7PQUUJ8toc34qyRg"
consumer_secret = "kz9fQqtyTzI82nGcJEewRwOfOg9NJgbZFKXH8SIq3mCuIvKJw5"
access_token = "907734081244450817-sCHEcTJYiHb8A0PLWdJUe1K3pqwVPU7"
access_token_secret = "QZnnI0g3IO5r9MLhpw9aVz0k5VOuCttM5w2bPduBR04NW"

# Input twitter handle
me = "@DataBootcampSJS"
print("Saved my handle")

# Define function
def tweet_analyzer():
    # Create empty lists
    compound = []
    positive = []
    neutral = []
    negative = []

    print("Created empty lists")

    # Loop through 25 pages of tweets (total 500 tweets)
    for x in range(25):

        # Pull last 500 tweets from target user
        tweets = api.user_timeline(target_user, page=x)

        # Loop through tweets in current page
        for tweet in tweets:

            # Append lists with sentiment analysis of each tweet
            compound.append(analyzer.polarity_scores(tweet["text"])["compound"])
            positive.append(analyzer.polarity_scores(tweet["text"])["pos"])
            neutral.append(analyzer.polarity_scores(tweet["text"])["neu"])
            negative.append(analyzer.polarity_scores(tweet["text"])["neg"])

    # Reverse the order of compound list
    compound = list(reversed(compound))

    print("Reversed order")
    
    # Initialize plot + format the plot
    fig, ax = plt.subplots()
    ax.plot(np.arange(-500,0), compound, '-o', alpha=.9, color="#5377AC", linewidth=0.5, label=target_user)

    # Format and print the plot
    plt.legend(title="Tweets", bbox_to_anchor=(1, 1), loc='upper left')
    plt.title("Sentiment Analysis of Tweets (" + datetime.datetime.now().strftime("%x") + ")")
    plt.xlabel("Tweets Ago")
    plt.ylabel("Tweet Polarity")
    plt.yticks(np.arange(-1,1.5,.5))
    #plt.tight_layout()

    plt.xlim(-507,7)
    plt.ylim(-1.05,1.05)
    plt.savefig("Resources/SentimentAnalysis.png", bbox_inches="tight")

    print("Saved plot")
    
    # Post tweet with plot
    api.update_with_media("Resources/SentimentAnalysis.png",
                      "New Tweet Analysis: @" + target_user + " (Thx @" + requesting_user + "!!)")
    print("Successful tweet!")
    
print("Defined function")

# Run our infinitely-looped function
while(True):

	    # Use Tweepy to Authenticate our access
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    print("Authorized with Twitter")
    
    # Get list of already-analyzed accounts
    analyzed = []
    check = api.user_timeline(me, count=100)
    for tweet in check:
        try:
            analyzed.append(tweet["entities"]["user_mentions"][0]["screen_name"])
        except:
            continue
            
    print("Logged analyzed accounts")

    # Check for new mentions
    new_mentions = api.search(q=me, since_id=check[0]["id"], result_type="recent")
    

    if len(new_mentions["statuses"]) == 0:
    	print("No new mentions")

    else:
    	print("New mention(s)")
    	
	    # Loop through new mentions, running function if not previously analyzed
    	for mention in new_mentions["statuses"]:
            if mention["entities"]["user_mentions"][1]["screen_name"] not in analyzed:
                target_user = mention["entities"]["user_mentions"][1]["screen_name"]
                print("Target user: " + target_user)
                requesting_user = mention["user"]["screen_name"]
                print("Requesting user: " + requesting_user)
                print("Ready to analyze")
                tweet_analyzer()
            else:
            	print("Account already analyzed")

    # Wait 5 minutes before checking for new mentions
    time.sleep(300)


### Fix legend getting cut off (check if it worked)
### Check for duplicate ignorance
### Got error importing tkinter on Heroku