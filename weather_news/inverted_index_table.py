import csv
import pandas as pd
import argparse

def create_pivot_data(input_key_region_file,data):
    key_value_dict = {}
    with open(input_key_region_file, mode="r") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            key_value_dict[int(row[0])] = row[1]
    pivoted_data = {}

    for name, values in data:
        pivoted_data[name] = {}
        for key, val in values:
            pivoted_data[name][key_value_dict.get(key, val)]=val
    
    return key_value_dict,pivoted_data

def create_csv_file(key_value_dict,pivoted_data,csv_file_path):
    news_II_data = []
    for event in pivoted_data.keys():
        pre_data = {'weather_event': event}
        for i in range(len(key_value_dict)):
            pre_data[key_value_dict[i]] = pivoted_data[event].get(key_value_dict[i], 0)
        news_II_data.append(pre_data)
    df = pd.DataFrame(news_II_data)
    df.to_csv(csv_file_path, index=False)   


def main():
    #data extracted from pyspark
    data = \
        [('wind', [(0, 4), (1, 1), (4, 12), (5, 5), (6, 1), (7, 2), (13, 5)]), \
        ('tornado', [(0, 1), (1, 5), (2, 1), (3, 1), (4, 88), (5, 69), (7, 1), (11, 1), (13, 23)]), \
        ('waterspout', [(5, 1), (13, 2)]), \
        ('microburst', [(0, 2), (4, 2), (7, 1), (10, 1)]), \
        ('ice', [(0, 1), (13, 1)]), \
        ('storm', [(1, 23), (3, 4), (4, 23), (5, 1), (7, 1), (13, 4)]), \
        ('cold', [(1, 1), (4, 1), (11, 1)]), \
        ('snowstorm', [(3, 2), (13, 5)]), \
        ('snow', [(3, 1), (4, 10), (5, 2), (13, 9)]), \
        ('hail', [(5, 3), (13, 4)]), \
        ('rain', [(5, 1), (7, 1), (13, 1)]), \
        ('cyclon', [(13, 1)]), \
        ('tornad', [(13, 1)]), \
        ('downburst', [(13, 2)]), \
        ('hailstorm', [(13, 1)]), \
        ('tornadocan', [(13, 1)]), \
        ('widespread', [(0, 1), (5, 2)]), \
        ('sever', [(0, 7), (1, 28), (4, 32), (5, 6), (13, 9)]), \
        ('rainfal', [(0, 1), (1, 3), (4, 1), (5, 1), (12, 1)]), \
        ('flood', [(0, 1), (1, 11), (3, 4), (4, 16), (5, 1), (13, 4)]), \
        ('thunderstorm', [(1, 1), (4, 5), (5, 1), (7, 2), (13, 5)]), \
        ('outbreak', [(1, 2), (4, 25), (5, 4), (11, 1), (13, 8)]), \
        ('flash', [(1, 3), (3, 4), (4, 8)]), \
        ('snowfal', [(1, 8)]), \
        ('winter', [(1, 3), (5, 3), (7, 1)]), \
        ('heat', [(1, 1)]), \
        ('hurrican', [(3, 2), (4, 3), (5, 3), (11, 1), (13, 25)]), \
        ('tropic', [(3, 1), (4, 2), (13, 6)]), \
        ('freez', [(3, 1), (13, 1)]), \
        ('blizzard', [(3, 2)]), \
        ('gustnado', [(13, 1)])]

    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input_csv",default = "key_region.csv")
    parser.add_argument("-o", "--output_csv", default="InvertedIndex_Table.csv")

    args = parser.parse_args()

    key_value_dict,pivoted_data = create_pivot_data(args.input_csv,data)
    create_csv_file(key_value_dict,pivoted_data,args.output_csv)

if __name__ == "__main__":
    main()
