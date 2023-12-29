import random
import datetime
import sys

def sample_data(data, sample_size=100): # sample data
    return random.sample(data, min(sample_size, len(data)))

def check_consistency(sample): # check data format
    consistent_format = True
    expected_datetime_format = '%Y%m%d%H'  # assuming format: YYYYMMDDHH

    for record in sample:
        try:
            # DATA in on index 1 - csv file
            datetime.datetime.strptime(record.split(',')[1], expected_datetime_format)
        except ValueError:
            consistent_format = False
            break

    return consistent_format

def check_completeness(sample): # check if there is any empty field
    return all(field.strip() for field in sample) 

def assess_quality(data):
    sampled_data = sample_data(data)
    quality_report = {
        "consistency": check_consistency(sampled_data),
        "completeness": check_completeness(sampled_data),
    }
    return quality_report

def read_data(file_path):
    with open(file_path, 'r') as file:
        data = [line.strip() for line in file.readlines() if line.strip()]  # Skip empty lines
    return data

def main():
    file_path = sys.argv[1]
    data = read_data(file_path)
    quality_report = assess_quality(data)
    print(quality_report)

if __name__ == "__main__":
    main()
