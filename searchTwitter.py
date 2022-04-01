#!/usr/local/bin/python3

# File used to generate twitter data given certain queries. 2 output CSVs will be generated with one storing [ID, tweet text] and the other [ID, tweet text, True/False with link].

from loginInfo import *
from datetime import datetime
import tweepy
import sys
import csv
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

sinceTime="1/19/20"
# Authenticate to Twitter

auth = tweepy.OAuthHandler(consumerKey,consumerSecret) 
auth.set_access_token(accessToken, accessSecret)

api = tweepy.API(auth)

dt=datetime.today()
fileName='resultsTwitter-'+str(dt.month)+'-'+str(dt.day)+'.csv'
ansFileName='resultsTwitterAns-'+str(dt.month)+'-'+str(dt.day)+'.csv'
csvFile = open(fileName, 'a')
ansCsvFile = open(ansFileName, 'a')

#Use csv writer
csvWriter = csv.writer(csvFile)
ansCsvWriter = csv.writer(ansCsvFile)


try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

for tweet in tweepy.Cursor(api.search_tweets, q="ADD QUERY HERE!"+" -filter:retweets").items(250):
    if tweet.entities['urls'] != []:
        if len(tweet.entities['urls']) > 1: # Mark all tweets with more than one link
            csvWriter.writerow([tweet.id_str, tweet.text.encode('utf-8')])
            ansCsvWriter.writerow([tweet.id_str, tweet.text.encode('utf-8'),True])
        else:
            if( tweet.entities['urls'][0]['expanded_url'][8:19] != "twitter.com" ): # mark tweets that have external links as their only link
                csvWriter.writerow([tweet.id_str, tweet.text.encode('utf-8')])
                ansCsvWriter.writerow([tweet.id_str, tweet.text.encode('utf-8'),True])
            else: #do not mark tweets with only one link that is internal to twitter
                csvWriter.writerow([tweet.id_str, tweet.text.encode('utf-8')])
                ansCsvWriter.writerow([tweet.id_str, tweet.text.encode('utf-8'),False])

    else:
        ansCsvWriter.writerow([tweet.id_str, tweet.text.encode('utf-8'),False])
        csvWriter.writerow([tweet.id_str, tweet.text.encode('utf-8')])

csvFile.close()
