# $spark-submit tf_idf_processing.py
# $python3 tf_idf_processing.py
from pyspark.sql import SparkSession
import re
import math
import Stemmer
import csv
import argparse
from pyspark import SparkContext

def csv_parser(input_file,output_file):
    region_data = {}

    with open(input_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:

            date = row[0]
            region = row[1]
            weather_news = row[2]

            if region not in region_data:
                region_data[region] = []

            region_data[region].append(weather_news)

    with open(output_file, 'w') as text_file:
        for region, weather_news in region_data.items():

            combined_news = ",".join(weather_news)

            text_file.write(f"{region},{combined_news}\n")


def mapper(key,value):

    stop_words=set()
    with open("stop_words.txt") as f:
        for line in f:
            stop_words.add(line.rstrip('\r\n'))

    value=value[0]
    it = re.finditer(r"\w+",value,re.UNICODE)
    words=dict()
    stemmer = Stemmer.Stemmer('english')

    length=0

    for match in it:
        token=match.group().lower()

        if not(token in stop_words):
            length=length+1
            token=stemmer.stemWord(token)
            if token in words:
                words[token]+=1
            else:
                words[token]=1
    for word, count in words.items():
        yield word, (key,count*1./length)

def reducer(key,values,nb_documents):
    result=[]
    idf=math.log(nb_documents*1./len(values))
    for (document, count) in values:
        count*=idf
        result.append((document,count))
    return key, result

def mapper_count(key,value):

    stop_words=set()
    with open("stop_words.txt") as f:
        for line in f:
            stop_words.add(line.rstrip('\r\n'))

    value=value[0]
    it = re.finditer(r"\w+",value,re.UNICODE)
    words=dict()
    stemmer = Stemmer.Stemmer('english')

    for match in it:
        token=match.group().lower()

        if not(token in stop_words):
            token=stemmer.stemWord(token)
            if token in words:
                words[token]+=1
            else:
                words[token]=1
    for word, count in words.items():
        yield word, (key,count)

def reducer_count(key,values):
    result=[]
    for (document, count) in values:
        result.append((document,count))
    return key, result


def main():
    sc=SparkContext()

    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input_csv",default = "weather_data.csv")
    parser.add_argument("-o", "--output_txt", default="output_weather_data.txt")

    args = parser.parse_args()
    csv_parser(args.input_csv,args.output_txt)
    rdd = sc.textFile(args.output_txt)
    rdd.map(lambda x: x.split("\t"))
    length = rdd.map(lambda x: x.split("\t")).count()
    new_column_values = sc.parallelize(range(length)).collect()

    rdd.map(lambda x: x.split("\t"))\
        .zipWithIndex().map(lambda x: ( new_column_values[x[1]],x[0]))\
        .flatMap(lambda l: list(mapper(l[0],l[1])))\
        .groupByKey() \
        .map(lambda l: reducer(l[0],list(l[1]),length))\
        .saveAsTextFile("Output_Weather_News_TF_IDF")    

    rdd.map(lambda x: x.split("\t"))\
        .zipWithIndex().map(lambda x: ( new_column_values[x[1]],x[0]))\
        .flatMap(lambda l: list(mapper_count(l[0],l[1])))\
        .groupByKey() \
        .map(lambda l: reducer_count(l[0],list(l[1])))\
        .saveAsTextFile("Inverted_Index")    


if __name__ == "__main__":
    main()
