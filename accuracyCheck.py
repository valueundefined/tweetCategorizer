# File created to check the accuracy of our Random Forest Algorithhm
import pandas as pd
import sys
import csv

def main():
    correctGuesses = 0
    totalGuesses = 0
    skip = 0

    dictAnswers = {}
    with open('answers.csv', mode='r') as file:
        skipOne = 0
        for line in file:
            if not( skipOne ):
                skipOne = 1
                continue
            contents = line.split(',')
            dictAnswers[ int(contents[0]) ] = contents[-1].rstrip()

    dictGuesses = pd.read_csv('Labels.csv', header=0, index_col=0, delimiter=",", quoting=3, on_bad_lines='skip').to_dict()

    for tweet in dictGuesses['ANSWER']:
        try:#
            if( str(dictGuesses['ANSWER'][tweet]) == dictAnswers[tweet] ): # Correct guess
                correctGuesses += 1
            else:
                print(tweet)
            totalGuesses += 1

        except: # ID not found (wrong files input)
            #print("ID for this tweet is missing in Answer File:", tweet )
            skip +=1

    print("The algorithm correctly guessed", correctGuesses/totalGuesses*100,"% of the tweets")
    print("Correct Guesses:",correctGuesses)
    print("Total Guesses:",totalGuesses)
    print("Skipped Tweets:", skip)

if __name__ == "__main__":
    main()


