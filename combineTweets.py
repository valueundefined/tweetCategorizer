# Take file and find duplicate tweets only save one version. Only useful for when you find duplicate tweets within files.

import pandas as pd
import csv

dict_from_csv = {}

def main():
    with open('test.csv', mode='r') as file:
        csvReader = csv.reader( file )
        dict_from_csv = {rows[0]:rows[1] for rows in csvReader}

    with open('test.csv', mode='w') as file:
        csvWriter = csv.writer( file )
        for id in dict_from_csv:
            csvWriter.writerow([id, dict_from_csv[id]])

main()
