import pandas as pd
import csv
import re

dataset = pd.read_csv('output.csv')

found = []
nominees = []
freq = []
for i in range(0, len(dataset['text'])):
	if (type(dataset['text'][i]) is not type("str")):
	    print(int(i + 2))
	    corpus.append("error")
	    continue

	pattern_gg = r"(?i)#?golden\s?globes"
	text = re.sub(pattern_gg, '', dataset['text'][i]) # Remove golden globes

	pattern_actor = r"(?i)best actor"
	pattern_hashtag = r"(?i)#bestactor"
	pattern_name = r"[A-Z][a-zA-Z]*\s[A-Z][a-zA-Z]*(?:\s[A-Z][a-zA-Z]*)*"
	
	match = re.search(pattern_actor, text)
	match_hashtag = re.search(pattern_hashtag, text)
	
	if match or match_hashtag:
		found.append(text)
		name_matches = re.findall(pattern_name, text)
		# remaining task: deal with "I" & "The"
		for name in name_matches:
			if re.search(pattern_gg, name) or re.search(pattern_actor, name): # Remove Best Actor & Golden Globes
				continue
			if name in nominees:
				freq[nominees.index(name)] += 1
			else:
				nominees.append(name)
				freq.append(1)

print(nominees)
print(freq)
print(len(found))

max_freq = max(freq)
max_index = freq.index(max_freq)
winner = nominees[max_index]

print('Winner: ' + winner)

for i in range(len(freq)):
	if freq[i] > 100:
		print(nominees[i] + ' ' + str(freq[i]))
