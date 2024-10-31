import csv
import json
from collections import defaultdict

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


output_data = {
    'hosts': ['amy poehler', 'tina fey'],
    'award_data': formatted_award_data
}


with open('formatted_award_data.json', 'w') as jsonfile:
    json.dump(output_data, jsonfile, indent=4)

print("Data successfully converted and saved to 'formatted_award_data.json'")
