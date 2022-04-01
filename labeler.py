#!/usr/bin/env python3

import pandas as pd     
import numpy as np
from bs4 import BeautifulSoup
import re
import string
import nltk
#nltk.download('stopwords') # Uncomment for one run to download stop words.
from nltk.corpus import stopwords # Import the stop word list

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def clean_text_data(data_point, data_size): # Clean data_point tweet text for more efficient running of the algorithm
    try:
        noHex = re.sub(r"\\x[a-f0-9][a-f0-9]",'',data_point[2:]) # Remove any hexadecimal - odd characters
        noUsers = re.sub(r"@[a-z0-9_]*",'',noHex) # Remove any twitter handles
        noLinks = re.sub(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))","",noUsers) # Remove any links from the tweets
        noSpace = noLinks.rstrip() # Remove any remaining white space
        res = re.findall(r'\w+',noSpace) # Find each word remaining in the string

""" Beautiful soup can be used on any data stored in HTML or XML form. Only uncomment if your data is stored in one of these two forms or else the parsing will not work. """

    #review_soup = BeautifulSoup(data_point)
    #review_text = review_soup.get_text()
    #review_letters_only = re.sub("[^a-zA-Z]", " ", review_text)
    #review_lower_case = review_letters_only.lower()  
    #review_words = review_lower_case.split() 

        stop_words = stopwords.words("english") # Remove all stop words from the data_point
        meaningful_words = [x for x in res if x not in stop_words] # Create a final list with all words that are not also stop words
    
        if( (i)%2000 == 0):
            print("Cleaned %d of %d data (%d %%)." % ( i, data_size, ((i)/data_size*100)))
        return( " ".join( meaningful_words))
    except: # Tweet is empty
        return('')

if __name__=='__main__':

	#read train and test data
	df_train = pd.read_csv("combined-label.csv", 
	                              header=0, 
	                              delimiter=",", 
	                              quoting=3,
                                      on_bad_lines='skip')
	df_test = pd.read_csv("combined-test.csv",
	                             header=0, 
	                             delimiter=",", 
	                             quoting=2,
                                     on_bad_lines='skip',
                                     dtype={'id':np.int64}) # np.int64 is important to store your tweet ID. Without this, pandas will change the 64-bit integer to scientific notation which may miss important pieces of the data.

        """ Verify things are read correctly by uncommenting
	#print(df_train.shape)
	#print(df_test.shape)
	#print(df_train.columns.values)
	#print(df_test.columns.values)
	#print(df_train)
	#print(df_test)
        """

	training_data_size = df_train["data"].size
	testing_data_size = df_test["data"].size

	# clean text data to get Bag of Words
	for i in range(training_data_size):
		df_train["data"][i] = clean_text_data(df_train["data"][i], training_data_size)
	print("Cleaning training completed!")

	for i in range(testing_data_size):
		df_test["data"][i] = clean_text_data(df_test["data"][i], testing_data_size)
	print("Cleaning test completed!")

	# Create term doc matrix using words as features
	from sklearn.feature_extraction.text import CountVectorizer
	vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 5000) 

	#split input into training and testing data (needed to build model)
	X_train, X_cv, Y_train, Y_cv = train_test_split(df_train["data"], df_train["links"], test_size = 0.3, random_state=42)

	#training data
	X_train = vectorizer.fit_transform(X_train)
	X_train = X_train.toarray()
	print(X_train.shape)

	#testing data
	X_cv = vectorizer.transform(X_cv)
	X_cv = X_cv.toarray()
	print(X_cv.shape)

	#validation dataset, second element of tuple should match the above
	X_test = vectorizer.transform(df_test["data"])
	X_test = X_test.toarray()
	print(X_test.shape)

        # Shows most used words
	vocab = vectorizer.get_feature_names()
	print(f"Printing first 100 vocabulary samples:\n{vocab[:100]}")

	distribution = np.sum(X_train, axis=0)

	print("Printing first 100 vocab-dist pairs:")
	for tag, count in zip(vocab[:100], distribution[:100]):
	     print(count, tag)
##
	#building the model
	print("building the model")
	forest = RandomForestClassifier() 
	forest = forest.fit( X_train, Y_train)

	print("testing the model")
	#testing the model
	predictions = forest.predict(X_cv) 
	print("Accuracy: ", accuracy_score(Y_cv, predictions))

	print("creating labels for unseen instances")
	result = forest.predict(X_test) 
	output = pd.DataFrame( data={"POST ID":df_test["id"], "ANSWER":result} )
	output.to_csv( "Labels.csv", index=False, quoting=3 )
	output = pd.DataFrame( data={"id":df_test["id"], "data":df_test["data"]} )
	output.to_csv( "Labels2.csv", index=False, quoting=3 )
