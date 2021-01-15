import os
import Collect_Data
import Analyzer

"""
    it is necessary to install the following library:
    1) pip install pandas
    2) pip install openpyxl
    3) pip install bs4
    4) pip install googlesearch
    5) pip install nltk
    6) pip install spacy
    The program must search for data about specify product represented as tweets or texts from Google.
    These tweets and texts are extracted and to put in an excel file named "dataset.xlsx".
    After that, Analyzer class will find the file "dataset.xlsx" and make an analyze each tweet and text.
    In conclusion, it will add two result tables, the first table displays analysis results tweets and 
    another table displays analysis results texts.      
"""

if __name__ == '__main__':
    query = "Iphone 12 Max Pro reviews"
    Collect_Data.collect_data(query)
    file = 'dataset.xlsx'
    if os.path.exists(file):
        Analyzer.analyze_data(file)
    else:
        print('There aren\'t any data!')
    print("Estimating is over!")
