import json
import re
from datetime import datetime
import csv
import jmespath
import sys
import argparse

def extract_sentences_with_dates(text_data):
    date_patterns = [
        r'\b\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}\b',
        r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4}\b',
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{2,4}\b',
        r'\b\d{2,4}-\d{1,2}-\d{1,2}\b',
        r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{2,4}\b',
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{2,4}\b'
    ]
    date_range_pattern = r'\b(\d{1,2})-(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{2,4})\b'

    sentences_with_dates = []

    for line in text_data.splitlines():
        date_range_match = re.search(date_range_pattern, line)

        if date_range_match:
            start_day, end_day, month, year = date_range_match.groups()
            for day in range(int(start_day), int(end_day) + 1):
                expanded_date = f"{day} {month} {year}"
                expanded_sentence = re.sub(date_range_pattern, expanded_date, line)
                sentences_with_dates.append(expanded_sentence)
        else:
            if any(re.search(pattern, line) for pattern in date_patterns):
                sentences_with_dates.append(line)

    return sentences_with_dates

def reg_keep_region_with_non_empty_news(input_file_path):
    with open(input_file_path, 'r') as file: 
        data = json.load(file)
    search_string = "*.[region,event_content]"
    search_data = jmespath.search(search_string, data)

    processed_data = {}
    for i in range(len(search_data)):
        if search_data[i][1] != None and len(search_data[i][1]) > 0:
            data = {'region': search_data[i][0], 'news': search_data[i][1]}
            processed_sentences = extract_sentences_with_dates(json.dumps(data['news'], indent=2))
            processed_data[search_data[i][0]] = {'news': processed_sentences}

    return processed_data

# Function to extract and format date from a news title
def extract_and_format_date(news_title):
    # Regular expression to find dates in various formats
    date_pattern = re.compile(r'\b(?:\d{1,2}\s)?(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,4},?\s?\d{4}\b')
    match = date_pattern.search(news_title)
    if match:
        date_str = match.group(0).replace(',', '')
        try:
            date = datetime.strptime(date_str, '%d %B %Y')
        except ValueError:
            try:
                date = datetime.strptime(date_str, '%B %d %Y')
            except ValueError:
                return None
        return date.strftime('%Y%m%d') + '00'
    else:
        return None
    
def create_csv_file(processed_data, output_filename):
    # extracting and formatting dates for each entr
    formatted_news_data = []
    for location, news_list in processed_data.items():
        for news_title in news_list['news']:
            formatted_date = extract_and_format_date(news_title)
            if formatted_date:
                formatted_news_data.append({
                    'date': formatted_date,
                    'location': location,
                    'news': news_title.strip()
                })

    # writing the extracted data to a csv file
    with open(output_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['date', 'location', 'news'])
        writer.writerows(formatted_news_data)    


def main():
    input_file_path = sys.argv[1]  # INPUT FILE NAME (.JSON)
    output_filename = sys.argv[2]  # OUTPUT FILE NAME (.CSV)

    processed_data = reg_keep_region_with_non_empty_news(input_file_path)
    create_csv_file(processed_data, output_filename)  
    print("CSV file created successfully (", output_filename, ")")

def main():
    parser = argparse.ArgumentParser(description='Process JSON and output CSV.')
    parser.add_argument('-i', help='Input JSON file', required=True)
    parser.add_argument('-o', help='Output CSV file', required=True)

    args = parser.parse_args()

    input_file_path = args.i
    output_filename = args.o

    processed_data = reg_keep_region_with_non_empty_news(input_file_path)
    create_csv_file(processed_data, output_filename)

if __name__ == "__main__":
    main()