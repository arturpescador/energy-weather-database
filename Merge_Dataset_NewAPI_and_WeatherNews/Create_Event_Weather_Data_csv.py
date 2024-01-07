import pandas as pd
import csv
import argparse

def create_csv(input_file_path,window_size):

    df_all = pd.read_csv(input_file_path)

    col_list = []
    for col in ['maxt', 'mint', 'avgt', 'hdd', 'cdd', 'pcpn', 'snow', 'snwd']:
        col_list+=[f'day{day}_{col}' for day in range(-5, 1)]
        col_list+=[f'day+{day}_{col}' for day in range(1, 6)]

    col1 =[f'day{day}_{col}' for day in range(-5, 1) for col in ['maxt', 'mint', 'avgt', 'hdd', 'cdd', 'pcpn', 'snow', 'snwd']]

    col2 = [f'day+{day}_{col}' for day in range(1,6) for col in ['maxt', 'mint', 'avgt', 'hdd', 'cdd', 'pcpn', 'snow', 'snwd']]


    concat_df = pd.DataFrame()
    column_order = ['Date', 'Location', 'News'] + col_list

    for idx in df_all[~df_all['News'].isnull()].index:
        
        df_target = df_all.iloc[idx-window_size:idx+window_size+1]
        melted_df = pd.melt(df_target, id_vars=['Date', 'Location', 'News'], var_name='Variable', value_name='Value')
        melted_df['Variable'] = column_order[3:]
        final_df = melted_df.pivot(index=['Location'], columns='Variable', values='Value').reset_index()
        final_df['News'] = df_target[~df_target['News'].isnull()]['News'].values[0]
        final_df['Date'] = df_target[~df_target['News'].isnull()]['Date'].values[0]
        concat_df = pd.concat([concat_df, final_df ], axis=0)
        if idx > 3450:
            break

    result_df = pd.DataFrame()
    result_df['Date'] = concat_df['Date']
    result_df['Location'] = concat_df['Location']
    result_df['Event'] = concat_df['News']
    result_df[col1] = concat_df[col1]
    result_df[col2] = concat_df[col2]

    return result_df



def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_csv",default = "Weather_Data_and_News_Dataset.csv")
    parser.add_argument("--output_csv", default="Event_WeatherData.csv")
    parser.add_argument("--window_size", default=5)

    args = parser.parse_args()

    input_file_path = args.input_csv
    output_file_path = args.output_csv
    window_size = args.window_size

    result_df = create_csv(input_file_path,window_size)

    result_df.to_csv(output_file_path, index=False) 

if __name__ == "__main__":
    main()
