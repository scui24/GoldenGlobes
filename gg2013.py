import pandas as pd
import csv
import re
import unidecode
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from ftfy import fix_text
from fuzzywuzzy import fuzz

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
nlp = spacy.load("en_core_web_sm")

# Normalize the tweet
def normalize(text):
    tokens = word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalnum() and word not in stop_words]
    return tokens

# Stemming algorithm
def stemming(text):
	words = word_tokenize(text)
	pos_tags = pos_tag(words)
	stemmed_words = [
	    word if tag in ['NNP', 'NNPS'] else stemmer.stem(word)  # Skip proper nouns
	    for word, tag in pos_tags
	]
	stemmed_sentence = ' '.join(stemmed_words)
	# stemmed_words = [stemmer.stem(word) for word in words]
	# stemmed_sentence = ' '.join(stemmed_words)
	return stemmed_sentence

# Return names found in given text
def find_person(text):
	if type(text) is not type('str'):
		print('error')
		return
	person = []
	doc = nlp(text)
	for ent in doc.ents:
		if ent.label_ == "PERSON":
			person.append(ent)
	return person

# Return sentiment score of the given tweet
def sentiment_scores(sentence):
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(sentence)
    return sentiment_dict['compound']

dataset = pd.read_csv('subset.csv')

text = ''
nominees = []
freq = []
sentiment = []
awards = [] # TODO
award_found = []
for i in range(0, len(dataset['text'])):
	if (type(dataset['text'][i]) is not type("str")):
	    print(int(i + 2))
	    # text.append("error")
	    continue

	text = fix_text(dataset['text'][i])
	# review = unidecode(review) # remove emojis
	text = re.sub(r'http\S+', '', text)
	# text = re.sub('')
	# text = normalize(text)

	tmp = stemming(text)
	matches = re.findall(r"(.+) (win|receive|get) (.+)", tmp)
	
	if matches:
		score = 80 # threshold
		award_tmp = ''
		for a in awards:
			tmp = fuzz.partial_ratio(matches[0][2], a)
			if tmp > score:
				award_tmp = a
		if award_tmp:
			doc = nlp(matches[0][0])
			for ent in doc.ents:
				if ent.label_ == "PERSON": # person exists & award exists
					award_found.append(award_tmp)
					nominees.append(ent.text)
					# freq?
		else: 
			# TODO: person exists, award doesn't
			continue
	else:
		doc = nlp(text)
		for ent in doc.ents:
			if ent.label_ == "PERSON":
				# TODO: no pattern but person exists
				continue

print(award_found)
print(nominees)			







