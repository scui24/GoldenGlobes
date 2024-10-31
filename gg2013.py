import pandas as pd
import csv
import re
import unidecode
import spacy
import nltk
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from ftfy import fix_text
from fuzzywuzzy import fuzz
# from imdb import IMDb
from tqdm import tqdm 

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
nlp = spacy.load("en_core_web_sm")
# ia = IMDb()

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

dataset = pd.read_csv('output.csv')
dataset_movie = pd.read_csv('title_basics.csv', low_memory=False)

text = ''
nominees = []
freq = []
sentiment = []
awards = ['best performance actor', 'best performance actress', 'best performance supporting role actor', 'best performance supporting role actress', 'best director']
# awards_work = ['best screenplay', 'best foreign language film', 'best motion picture', 'best mini-series', 'best original score', 'best television series', 'best animated feature film', 'best original song']
award_found = []
x = 0
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
	matches = re.findall(r"(.+) (win|receive|get) (.+)", tmp)
	
	if matches:
		x += 1
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


with open('answer.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Nominee", "Award", "Frequency"])
    for row in zip(nominees, award_found, freq):
        writer.writerow(row)


print(award_found)
print(nominees)
print(len(award_found))
print(len(nominees))
print(x)

for i in range(len(nominees)):
	# if award_found[i] in ['best performance actor', 'best performance actress', 'best performance supporting role actor', 'best performance supporting role actress']:
	# 	tmp = get_actor_work_types(nominees[i], 2013)
	# 	if tmp:
	# 		award = award_found[i] + ' in a ' + tmp[0]
	print(f"Nominee: {nominees[i]}, Award: {award_found[i]}")





