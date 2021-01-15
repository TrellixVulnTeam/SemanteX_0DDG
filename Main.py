import os
import Collect_Data
import Analyzer

"""
    The program must search for data about specify product represented as tweets or texts from Google.
    These tweets and texts are extracted and to put in an excel file named "dataset.xlsx".
    After that, Analyzer class will find the file "dataset.xlsx" and make an analyze each tweet and text.
    In conclusion, it will add two result tables, the first table displays analysis results tweets and 
    another table displays analysis results texts.      
"""

if __name__ == '__main__':
    query = "Iphone 12 Max Pro reviews"
    Collect_Data.collect_data(query)
    # It's here, it is necessary to have to specify a path to file "dataset.xlsx".
    # This file was created in the current directory of this project.
    path = '/Users/dankevich.te/Desktop/Developing/Python/SemanteX/dataset.xlsx'
    if os.path.exists(path):
        Analyzer.analyze_data(path)
    else:
        print('There aren\'t any data!')
    print("Estimating is over!")
