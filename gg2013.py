import pandas as pd
import csv
import re
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from ftfy import fix_text
from fuzzywuzzy import fuzz
from tqdm import tqdm 

nlp = spacy.load("en_core_web_sm")

# Return the indexes of every existence of the given name in the given list, false if not found
def in_list(name, name_list):
	normalized_name = name.replace(" ", "").replace("-", "").lower()
	matches = []
	for index, existing_name in enumerate(name_list):
		normalized_existing_name = existing_name.replace(" ", "").replace("-", "").lower()
		if normalized_name == normalized_existing_name:
			matches.append(index)
	return matches if matches else False

# Return the genre of the given title
def get_genre(film_title):
    film = dataset_movie[dataset_movie['primaryTitle'] == film_title]
    if not film.empty:
        return film.iloc[0]['genres']
    else:
        return False

# Return sentiment score of the given tweet
def sentiment_scores(sentence):
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(sentence)
    return sentiment_dict['compound']

# Return true if the given sentence is a hypothetical statement
def hypothetical(sentence):
	hypothetical_keywords = ["if", "could", "would", "might", "may", "should", "suppose", "imagine", "in case", "as if", "next"]
	doc = nlp(sentence)
	for token in doc:
		if token.text.lower() in hypothetical_keywords:
			return True
		if token.dep_ == "mark" and token.text.lower() == "if": # if statement
			return True
		if token.lemma_ == "wish" or (token.tag_ == "VBD" and token.dep_ == "advcl"): # subjunctive mood indicator
			return True
	return False

dataset = pd.read_csv('output.csv')
dataset_movie = pd.read_csv('title_basics.csv', low_memory=False)

text = ''
nominees, hosts, cecil = [], [], []
freq, freq_host, freq_cecil = [], [], []
sentiment = []
awards = ['best performance actor', 'best performance actress', 'best performance supporting role actor', 'best performance supporting role actress', 'best director']
award_found = []
appearance = ["dress", "outfit", "style", "look"]
dress = []

presenters = {} # Dictionary where presenters[award] is a list of two names

for i in tqdm(range(0, len(dataset['text'])), desc="Processing tweets"):

	if (type(dataset['text'][i]) is not type("str")):
	    print(int(i + 2))
	    # text.append("error")
	    continue

	text = fix_text(dataset['text'][i])
	text = re.sub(r'http\S+', '', text)
	text = re.sub(r'(?i)\bGolden\s*Globes\b|\bgoldenglobes\b', '', text)
	text = re.sub(r"'s\b'", '', text) # remove 's at the end of a word
	text = re.sub(r'["\'@]', '', text)

	matches = re.findall(r"(.+) (win|won|wins|winning|receive|received|receives|receiving|get|gets|got|getting) (.+)", text)

	if matches:
		score = 70 # threshold
		award_tmp = ''
		for a in awards:
			tmp = fuzz.partial_ratio(matches[0][2], a)
			if tmp > score: # if above threshold
				award_tmp = a
		if award_tmp:
			doc = nlp(matches[0][0])
			for ent in doc.ents:
				flag = True
				if ent.label_ == "PERSON": # person exists & award exists
					idx = in_list(ent.text, nominees)
					if idx:
						for j in idx:
							if award_found[j] == award_tmp: # merge only when both the name and the award match
								freq[j] += 1
								flag = False
					if flag:
						award_found.append(award_tmp)
						nominees.append(ent.text)
						freq.append(1)
		else:
			doc = nlp(matches[0][0])
			for ent in doc.ents:
				flag = True
				if ent.label_ == "WORK_OF_ART":
					# print(ent.text)
					genre = get_genre(ent.text)
					if genre:
						award_tmp = 'best ' + str(genre)
						if ent.text in nominees:
							freq[nominees.index(ent.text)] += 1
							flag = False
						if flag:
							award_found.append(award_tmp)
							nominees.append(ent.text)
							freq.append(1)

	if 'host' in text and not hypothetical(text): # Host
		doc = nlp(text)
		for ent in doc.ents:
			if ent.label_ == "PERSON":
				if ent.text in hosts:
					freq_host[hosts.index(ent.text)] += 1
				else:
					hosts.append(ent.text)
					freq_host.append(1)

	if 'cecil' in text.lower() or 'demille' in text.lower(): # Cecil b. demille
		doc = nlp(text)
		for ent in doc.ents:
			if ent.label_ == "PERSON":
				if ent.text in cecil:
					freq_cecil[cecil.index(ent.text)] += 1
				else:
					cecil.append(ent.text)
					freq_cecil.append(1)

	if any(keyword in text.lower() for keyword in appearance): # Best & worst dressed
		sent = sentiment_scores(text)
		if sent > 0.2 or sent < -0.02:
			doc = nlp(text)
			for ent in doc.ents:
				if ent.label_ == "PERSON":
					dress.append(ent.text)
					sentiment.append(sent)

for i in range(len(cecil)):
	nominees.append(cecil[i])
	award_found.append('cecil b. demille')
	freq.append(freq_cecil[i])

# Print results
# for i in range(len(nominees)):
# 	print(f"Nominee: {nominees[i]}, Award: {award_found[i]}")

max_sent = max(sentiment)
print('Best dress: ' + str(dress[sentiment.index(max_sent)]))
min_sent = min(sentiment)
print('Worst dress: ' + str(dress[sentiment.index(min_sent)]))

# Write csv
with open('host.csv', mode='w', newline='') as file:
	writer = csv.writer(file)
	writer.writerow(['Host', 'Frequency'])
	for row in zip(hosts, freq_host):
		writer.writerow(row)

with open('answer.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Nominee", "Award", "Frequency"])
    for row in zip(nominees, award_found, freq):
        writer.writerow(row)




