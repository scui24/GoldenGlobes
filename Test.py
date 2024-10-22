import csv
import pandas as pd

# dataset = pd.read_csv('output.csv')

# for i in range(len(dataset['user.screen_name'])):
# 	if type(dataset['user.screen_name'][i]) != type('str'):
# 		continue
# 	text =  dataset['user.screen_name'][i].lower()
# 	if 'goldenglobe' in text:
# 		print(dataset['text'][i])

from fuzzywuzzy import fuzz

string1 = "heyheyhey someone is the Best Actor for Motion Movie. he must be it"
string2 = "Best Actress for tv show"

partial_score = fuzz.partial_ratio(string1, string2)

print(f"Partial Ratio Score: {partial_score}")
