import pandas as pd
import csv
import re
import unidecode
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from ftfy import fix_text
from fuzzywuzzy import fuzz
from tqdm import tqdm 

nlp = spacy.load("en_core_web_sm")

# Stemming algorithm
def stemming(text):
	words = word_tokenize(text)
	pos_tags = pos_tag(words)
	stemmed_words = [
	    word if tag in ['NNP', 'NNPS'] else stemmer.stem(word)  # Skip proper nouns
	    for word, tag in pos_tags
	]
	stemmed_sentence = ' '.join(stemmed_words)
	return stemmed_sentence

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

# Detect a presenter in the given text.
def detect_presenter(text):
    
    presenter_match = re.findall(r"(.+) (present|introduce|announce) (.+)", text)
    if presenter_match:
        doc = nlp(presenter_match[0][0])
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
    return None

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
nominees = []
freq = []
sentiment = []
awards = ['best performance actor', 'best performance actress', 'best performance supporting role actor', 'best performance supporting role actress', 'best director']
award_found = []

presenters = []

for i in tqdm(range(0, len(dataset['text'])), desc="Processing tweets"):

	if (type(dataset['text'][i]) is not type("str")):
	    print(int(i + 2))
	    # text.append("error")
	    continue

	text = fix_text(dataset['text'][i])
	# review = unidecode(review) # remove emojis
	text = re.sub(r'http\S+', '', text)
	text = re.sub(r'(?i)\bGolden\s*Globes\b|\bgoldenglobes\b', '', text)
	text = re.sub(r"'s\b'", '', text) # remove 's at the end of a word
	text = re.sub(r'["\'@]', '', text)

	tmp = stemming(text)
	matches = re.findall(r"(.+) (win|won|wins|winning|receive|received|receives|receiving|get|gets|got|getting) (.+)", tmp)
	
	if matches:
		score = 70 # threshold
		award_tmp = ''
		for a in awards:
			tmp = fuzz.partial_ratio(matches[0][2], a)
			if tmp > score: # if above threshold
				award_tmp = a
				# print('found')
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
				# break

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

	presenter = detect_presenter(text)
	if presenter and presenter not in presenters and presenter[0:2] != "RT":
		presenters.append(presenter)

	if 'host' in text and not hypothetical(text):
		doc = nlp(text)
		for ent in doc.ents:
			if ent.label_ == "PERSON":
				if ent.text in hosts:
					freq_host[hosts.index(ent.text)] += 1
				else:
					hosts.append(ent.text)
					freq_host.append(1)


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

    writer.writerow([])
    writer.writerow(["Presenters"])
    for presenter in presenters:
        writer.writerow([presenter])

# Print results
print(award_found)
print(nominees)
print("Presenters and Awards:", presenters)
print(len(award_found))
print(len(nominees))

for i in range(len(nominees)):
	# if award_found[i] in ['best performance actor', 'best performance actress', 'best performance supporting role actor', 'best performance supporting role actress']:
	# 	tmp = get_actor_work_types(nominees[i], 2013)
	# 	if tmp:
	# 		award = award_found[i] + ' in a ' + tmp[0]
	print(f"Nominee: {nominees[i]}, Award: {award_found[i]}")





