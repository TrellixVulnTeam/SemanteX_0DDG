import os
import Collect_Data
import Analyzer

if __name__ == '__main__':
    query = "Iphone 12 Max Pro reviews"
    number_of_texts = 50
    Collect_Data.collect_data(query, number_of_texts)
    path = '/Users/dankevich.te/Desktop/Developing/Python/SemanteX/dataset.xlsx'
    if os.path.exists(path):
        # Analyzer.analyze_data_with_education(path)
        Analyzer.analyze_data_without_education(path)
    else:
        print('There aren\'t any data!')
    print("Estimating is over!")
