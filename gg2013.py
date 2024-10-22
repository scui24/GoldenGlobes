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
	words = word_tokenize(sentence)
	stemmed_words = [stemmer.stem(word) for word in words]
	stemmed_sentence = ' '.join(stemmed_words)
	return stemmed_sentence

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
award = []
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

	# tmp = stemming(text)
	matches = re.findall(r"(.+) (win|receive|get) (.+)", text)
	
	if matches:
		doc = nlp(matches[0][2])
		score = fuzz.partial_ratio(string1, string2)

	doc = nlp(text)
	for ent in doc.ents:
        if ent.label_ == "PERSON":
            if ent not in nominees:
            	nominees.append(ent)







