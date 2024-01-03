import csv
import pandas as pd
import argparse
import ast


def text_parser(weather_event_keywords,part0,part1):
    with open(part0, 'r') as file:
        file_contents0 = file.read()
    
    with open(part1, 'r') as file:
        file_contents1 = file.read()

    lines = file_contents0.split('\n')+file_contents1.split('\n')

    result = []

    for line in lines:
        if line.strip():  
            key, value = line.split(',', 1)
            key = key[2:-1]
            value = value[1:-1]
            if key in weather_event_keywords:
                result.append((key, ast.literal_eval(value)))

    return result
    
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
    weather_event_keywords = \
    ['wind', 'tornado', 'waterspout', 'microburst', \
    'ice', 'storm', 'cold', 'snowstorm', 'snow', \
    'hail', 'rain', 'cyclon', 'tornad', 'downburst', 'hailstorm', \
    'tornadocan', 'widespread', 'sever', 'rainfal', \
    'flood', 'thunderstorm','outbreak', 'flash', \
    'snowfal','winter', 'heat', 'hurrican', \
    'tropic', 'freez', 'blizzard', 'gustnado']

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_csv",default = "key_region.csv")
    parser.add_argument("--input_II_0",default = "Inverted_Index/part-00000")
    parser.add_argument("--input_II_1",default = "Inverted_Index/part-00001")
    parser.add_argument("--input_TFIDF_0",default = "Output_Weather_News_TF_IDF/part-00000")
    parser.add_argument("--input_TFIDF_1",default = "Output_Weather_News_TF_IDF/part-00001")
    parser.add_argument("-o1", "--output_csv_II", default="InvertedIndex_Table.csv")
    parser.add_argument("-o2", "--output_csv_TFIDF", default="TFIDF_Table.csv")

    args = parser.parse_args()

    data_II = text_parser(weather_event_keywords,args.input_II_0,args.input_II_1)
    data_TF_IDF = text_parser(weather_event_keywords,args.input_TFIDF_0,args.input_TFIDF_1)

    key_value_dict,pivoted_data = create_pivot_data(args.input_csv,data_II)
    create_csv_file(key_value_dict,pivoted_data,args.output_csv_II)

    key_value_dict,pivoted_data = create_pivot_data(args.input_csv,data_TF_IDF)
    create_csv_file(key_value_dict,pivoted_data,args.output_csv_TFIDF)

if __name__ == "__main__":
    main()
