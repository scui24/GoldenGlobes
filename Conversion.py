import pandas as pd
import json

# Load JSON data
with open('gg2013.json') as json_file:
    data = json.load(json_file)

# Convert JSON data to a pandas DataFrame
df = pd.json_normalize(data)

# Save DataFrame to a CSV file
df.to_csv('output.csv', index=False)
