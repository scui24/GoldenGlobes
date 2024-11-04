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
        hosts = hosts[:2]  # Keep only the top 2 hosts
    else:
        hosts = ["host1", "host2"]  # Default names if host.csv is missing
    return hosts

def load_presenters():
    presenters_data = defaultdict(list)
    if os.path.exists('presenters.csv'):
        with open('presenters.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                award = row['Award'].strip().lower()
                presenters = [row[col].strip() for col in ['Presenter 1', 'Presenter 2'] if row[col] and row[col].strip()]
                presenters_data[award] = presenters
    return presenters_data


def main():
    dataset = pd.read_csv('output.csv')
    timestamp_ms = dataset['timestamp_ms'].iloc[0]
    year = datetime.fromtimestamp(timestamp_ms / 1000.0).year

    # Load award nominees and winners
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

    # Load presenters and add them to award_data
    presenters_data = load_presenters()
    formatted_award_data = {}
    for award, details in award_data.items():
        formatted_award_data[award] = {
            'nominees': details['nominees'],
            'presenters': presenters_data.get(award, []),
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
        
    # human-readable output of host, award, presenters, nominees, winner
    with open('f'gg{year}answers.json'', 'r') as file:
        data1 = json.load(file)
        print (data1)
    # human-readable output of most discusses people, most, controversial people with sentiment score
     with open('tweet_analysis_results.json', 'r') as file:
        data2 = json.load(file)
        print (data2)

if __name__ == "__main__":
    main()
