import requests
import jmespath
import json
import csv
import argparse
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

def format_date(date):
    # Assuming date is in the format 'YYYY-MM-DD'
    return date.replace("-", "") + "00"

def transform_min_max_date(date):
    date_string = str(date)
    date_obj = datetime.strptime(date_string, "%Y%m%d%H")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date

def relative_date_window_list(window_size = 5,df_location = None):

    date_lists = [] 
    for index, row in df_location.iterrows():
        current_date = row['Date_Time']
        min_date = current_date - relativedelta(days=window_size)
        max_date = current_date + relativedelta(days=window_size)
        date_range = pd.date_range(start=min_date, end=max_date, freq='D')
        int_dates = [int(date.strftime('%Y%m%d%H')) for date in date_range]
        date_lists.append(int_dates)
        
    return date_lists

def transform_relative_date_window_list(date_lists):
    transform_list = []
    for sub_list in date_lists:
        min_date = transform_min_max_date(sub_list[0])
        max_date = transform_min_max_date(sub_list[-1])
        transform_list.append([min_date,max_date])
    return transform_list

def get_merged_df(elem_list,transform_list,sid,url,i):
    json_data_sources = []

    for elem in elem_list:
        payload =  {"sid":sid,"sDate":transform_list[i][0],"eDate":transform_list[i][1],"elems":elem}
        r = requests.get(url,params=payload)
        json_sublist = r.json()
        json_data_sources.append(json_sublist)
        
    merged_df = pd.DataFrame(json_data_sources[0]['data'], columns=["Date",elem_list[0]])
    i_elem=1
    for json_data_source in json_data_sources[1:]:
        df = pd.DataFrame(json_data_source['data'], columns=["Date",elem_list[i_elem]])
        merged_df = merged_df.merge(df, on="Date")
        i_elem+=1

    return merged_df


def get_final_df(merged_df,location,df_news,window_size):
    
    merged_df["Location"] = [location] * len(merged_df)

    merged_df["Date"] = merged_df["Date"].apply(format_date).astype(int)

    merged_df = merged_df[['Date', 'Location'] + [col for col in merged_df.columns if col not in ['Date', 'Location']]]

    df1 = merged_df
    df2 = df_news[df_news['Location']==location]

    final_df = df1.merge(df2, on=['Date','Location'], how='outer')

    final_df = final_df.iloc[:2*window_size+1]

    return final_df


def create(df_news, dic_location_id, window_size = 5, url = "", elem_list = []):
    
    concat_df = pd.DataFrame()
    
    for location in df_news['Location'].unique():
        if location == "Nashville, TN":
            continue
            
        df_location = df_news[df_news['Location']==location]
        
        date_lists = relative_date_window_list(window_size = window_size, df_location = df_location)
        
        transform_list = transform_relative_date_window_list(date_lists)
        
        sid = dic_location_id[location]
    
        for i in range(len(transform_list)):
        
            merged_df =  get_merged_df(elem_list,transform_list,sid,url,i)
            
            final_df = get_final_df(merged_df,location,df_news,window_size) 
            
            concat_df = pd.concat([concat_df, final_df ], axis=0)
            
    result_df = pd.concat([concat_df, df_news[df_news['Location']=="Nashville, TN"]], axis=0).drop('Date_Time',axis=1)

    
    return result_df


def main():

    dic_location_id = \
    {
        "Burlington, VT" : "BTVthr 9", 
        "Binghamton, NY" : "BGMthr 9", 
        "Charleston, WV" : "CRWthr 9", 
        "Albany, NY" : "ALBthr 9", 
        "Shreveport, LA" : "SHVthr 9", 
        "Great Falls, MT" : "GTFthr 9", 
        "Pocatello, ID" : "PIHthr 9", 
        "NWS Phoenix" : "PHXthr 9",
        "Gray - Portland, ME" : "PWMthr 9",
        "Philadelphia/Mt Holly" : "PHLthr 9",
        "NWS Wilmington, NC" :"ILMthr 9",
        "Charleston, SC" : "CHSthr 9",
        "Newport/Morehead City, NC" : "316096 2"
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_csv",default = "weather_data.csv")
    parser.add_argument("--output_csv", default="Weather_Data_and_News_Dataset.csv")

    args = parser.parse_args()

    input_file_path = args.input_csv
    column_names = ["Date", "Location", "News"] 
    df_news = pd.read_csv(input_file_path, names=column_names)
    df_news['Date_Time'] = pd.to_datetime(df_news['Date'], format='%Y%m%d%H')

    url = "https://data.rcc-acis.org/StnData?"
    elem_list = ["maxt","mint","avgt","hdd","cdd","pcpn","snow","snwd"]

    result_df = create(df_news = df_news, dic_location_id = dic_location_id , window_size = 5, url = url, elem_list = elem_list)

    output_file_path = args.output_csv

    result_df.to_csv(output_file_path, index=False) 
    
    print("Result Dataset saved to {}".format(output_file_path))

if __name__ == "__main__":
    main()
