import pandas as pd
import csv
import re

dataset = pd.read_csv('subset.csv')

found = []
nominees = []
freq = []
for i in range(0, len(dataset['text'])):
	if (type(dataset['text'][i]) is not type("str")):
	    print(int(i + 2))
	    corpus.append("error")
	    continue

	pattern = r"best actor"
	pattern_hashtag = r"#bestactor"
	name_pattern = r"[A-Z][a-zA-Z]*\s[A-Z][a-zA-Z]*(?:\s[A-Z][a-zA-Z]*)*"
	match = re.search(pattern, dataset['text'][i], re.IGNORECASE)
	match_hashtag = re.search(pattern_hashtag, dataset['text'][i], re.IGNORECASE)
	if match:
		found.append(dataset['text'][i])
		name_matches = re.findall(name_pattern, dataset['text'][i])
		for name in name_matches:
			if name in nominees:
				freq[nominees.index(name)] += 1
			else:
				nominees.append(name)
				freq.append(1)

print(nominees)
print(freq)
print(len(found))