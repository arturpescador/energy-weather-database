# date formats in data: "01/01/2020", "1 Jan 2020", "Jan 1, 2020", "2020-01-01", "1 January 2020"

import json
import re
import sys

def extract_sentences_with_dates(text_data):
    # Regular expressions for different date formats and date range format
    date_patterns = [
         # Formats like 01/01/2020, 1-1-20
        r'\b\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}\b', 
        # 1 Jan 2020
        r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4}\b',  
        # Jan 1, 2020
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{2,4}\b', 
        # 2020-01-01 
        r'\b\d{2,4}-\d{1,2}-\d{1,2}\b',  
        # 1 January 2020
        r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{2,4}\b', 
        # January 1, 2020
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
        else: # check other formats
            if any(re.search(pattern, line) for pattern in date_patterns):
                sentences_with_dates.append(line)

    return sentences_with_dates

def process_file(input_file_path, output_file_path):

    with open(input_file_path, 'r') as file: # read scraped data (JSON FORMAT)
        data = json.load(file)

    # JSON TO TEXT
    text_data = json.dumps(data, indent=2)

    # Extract and process the sentences
    processed_sentences = extract_sentences_with_dates(text_data)

    # Generate a new JSON file with processed sentences
    with open(output_file_path, 'w') as output_file:
        json.dump(processed_sentences, output_file, indent=2)

    print(f"Processed data saved to {output_file_path}")

input_file_path = sys.argv[1] # INPUT FILE NAME (.JSON)
output_file_path = sys.argv[2] # OUTPUT FILE NAME (.JSON)

process_file(input_file_path, output_file_path)
