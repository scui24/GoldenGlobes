
import json
from collections import defaultdict
# Load the data
with open('raw_output.json', 'r') as f:
    data = json.load(f)
consolidated_results = defaultdict(lambda: {
    'nominees': [],
    'winner': None,
    'max_mentions': 0  
})
# Group nominees under each consolidated award category
for nominee_data in data['nominees']:
    award = nominee_data['award'].strip().lower()  
    nominee_name = nominee_data['name']
    mentions = nominee_data['mentions']
    avg_sentiment = nominee_data['avg_sentiment']
    
    consolidated_results[award]['nominees'].append({
        'name': nominee_name,
        'mentions': mentions,
        'avg_sentiment': avg_sentiment
    })
    
    if mentions > consolidated_results[award]['max_mentions']:
        consolidated_results[award]['winner'] = nominee_name
        consolidated_results[award]['max_mentions'] = mentions
# Format results 
formatted_results = {}
for award, details in consolidated_results.items():
    formatted_results[award] = {
        'nominees': [nominee['name'] for nominee in details['nominees']],
        'winner': details['winner'],
        'presenters': [] 
    }

with open('formatted_award_results-1.json', 'w') as f:
    json.dump(formatted_results, f, indent=4)
print("Consolidated and formatted results saved to 'formatted_award_results-1.json'")