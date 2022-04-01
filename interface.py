#!/usr/bin/env python3

from Corpus import Corpus
import sys
import nltk
#import argparse
#import getopt

#Usage: interface.py [corpus file]
if __name__=='__main__':
    nltk.download('stopwords')
    sectionBreak = "****************************************************************"

    print("Data loading from: ", str(sys.argv[1]))
    #self.corpus = Corpus(self.corpusFile, self.stopFile, self.idValue, self.textValue, self.column, self.key, self.invert)
    analysis = Corpus(sys.argv[1], None, "id", "data", [], [], False)
    analysis.readFromFile()
    analysis.getCount()
    analysis.parse()
    print("Data loaded, ready to begin analysis")

    print(sectionBreak)
    print("Beinning frequency analysis")
    freqs = analysis.getWordFreq()
    for f in freqs:
        print(f)
    print("Frequency anlysis done.")

    print(sectionBreak)
    print("Bigram analysis starting, this may take a few minutes.")
    bigrams = analysis.ngram(numToReturn=250,numOfGrams=2)
    print("Results (bigram, count):")
    for b in bigrams:
        print(b)
    print("Brigram analysis done.")

    print(sectionBreak)
    print("Trigram analysis starting, this may take a few minutes.")
    trigrams = analysis.ngram(numToReturn=250,numOfGrams=3)
    print("Results (trigram, count):")
    for t in trigrams:
        print(t)
    print("Trigram analysis done.")

    #Word cloud functionality is broken in current version of TextQ 
    #print(sectionBreak)
    #print("Generating word cloud.")
    #analysis.makeCloud('ngrams',100)
    #print("Word cloud done.")

    #analysis.exportData("out.csv")
