import csv
import json
import os
from collections import defaultdict
from datetime import datetime
import pandas as pd

def load_hosts():
    hosts = []
    if os.path.exists('host.csv'):
        with open('host.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                host_name = row['Host'].strip()
                hosts.append(host_name)
    else:
        hosts = ["host1", "host2"]  # Default names if host.csv is missing
    return hosts

def main():
    dataset = pd.read_csv('output.csv')
    timestamp_ms = dataset['timestamp_ms'].iloc[0]
    year = datetime.fromtimestamp(timestamp_ms / 1000.0).year

    with open('answer.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        award_data = defaultdict(lambda: {'nominees': [], 'winner': None, 'max_frequency': 0})

        for row in reader:
            nominee = row['Nominee'].strip()
            award = row['Award'].strip().lower()
            frequency = int(row['Frequency'])

            award_data[award]['nominees'].append(nominee)

            if frequency > award_data[award]['max_frequency']:
                award_data[award]['winner'] = nominee
                award_data[award]['max_frequency'] = frequency

    formatted_award_data = {}
    for award, details in award_data.items():
        formatted_award_data[award] = {
            'nominees': details['nominees'],
            'presenters': [],
            'winner': details['winner']
        }

    hosts = load_hosts()

    output_data = {
        'hosts': hosts,
        'award_data': formatted_award_data
    }

    output_filename = f'gg{year}answers.json'
    with open(output_filename, 'w') as jsonfile:
        json.dump(output_data, jsonfile, indent=4)

if __name__ == "__main__":
    main()

