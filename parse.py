# Allows for the parsing of twitter csvs generated in the long mode of searchTwitter.py . This is only useful when all data is collected. Searchtwitter.py defaults to the short data output of ID and tweet text.
import pandas as pd
import numpy as np
import csv
import json

def main():
    outputNoAns = {} # {'id':'data'}
    outputAns = {} # {'id':{'data':text,'links':True/False'}}
    tweets = pd.read_csv( "allTweets.csv", header=None, index_col=1, delimiter=",", dtype={1:np.int64}, quoting=2, on_bad_lines='skip' ).to_dict() # Read entire test set of tweets and convert to dictionary
    for id in tweets[ 2 ]:
        urlLocation = tweets[ 4 ][ id ].find("expanded_url") # Search for url in current tweet
        outputNoAns[ id ] = tweets[ 2 ][ id ] # Always save no answer
        
        if urlLocation == -1: # If there are no urls
            outputAns[ id ] = {'data': tweets[ 2 ][ id ], 'links': False }
        elif tweets[ 4 ][ id ][ urlLocation+16:urlLocation+35 ] == 'https://twitter.com': # Internal links are not counted
            outputAns[ id ] = {'data': tweets[ 2 ][ id ], 'links': False }
        else:
            outputAns[ id ] = {'data': tweets[ 2 ][ id ], 'links': True }

    csvFile = open( "allParsedTweets.csv", 'w')
    ansCsvFile = open( "allParsedTweetsAns.csv", 'w')

    csvWriter =  csv.writer( csvFile )
    ansCsvWriter = csv.writer( ansCsvFile )

    for id in outputNoAns:
        csvWriter.writerow([ id, outputNoAns [id ] ])
        ansCsvWriter.writerow([ id, outputAns[ id ][ 'data' ], outputAns[ id ][ 'links' ] ])

    csvFile.close()
    ansCsvFile.close()

if __name__=="__main__":
    main()
