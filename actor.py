import pandas as pd
import csv
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from ftfy import fix_text
import unidecode
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Return sentiment score of the given tweet
def sentiment_scores(sentence):
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(sentence)
    # print("Overall sentiment dictionary is : ", sentiment_dict)
    return sentiment_dict['compound']
    # if sentiment_dict['compound'] >= 0.05:
    #     return "Positive"
    # elif sentiment_dict['compound'] <= - 0.05:
    #     return "Negative"
    # else:
    #     return "Neutral"

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Normalize the tweet
def normalize(text):
    tokens = word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalnum() and word not in stop_words]
    return tokens

dataset = pd.read_csv('output.csv')

text = []
found = []
nominees = []
freq = []
sentiment = []
for i in range(0, len(dataset['text'])):
	if (type(dataset['text'][i]) is not type("str")):
	    print(int(i + 2))
	    text.append("error")
	    continue

	# Data preprocessing
	text = fix_text(dataset['text'][i])
	# review = unidecode(review) # remove emojis
	text = re.sub(r'http\S+', '', text)
	text = normalize(text)

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
		for name in name_matches:
			if re.search(pattern_gg, name) or re.search(pattern_actor, name): # Remove Best Actor & Golden Globes
				continue
			sentiment_name = sentiment_scores(text) 
			if name in nominees:
				freq[nominees.index(name)] += 1
				sentiment[nominees.index(name)] += sentiment_name
			else:
				nominees.append(name)
				freq.append(1)
				sentiment.append(sentiment_name)

for i in range(len(sentiment)):
	sentiment[i] /= freq[i]



	# winner2 = re.findall(r"(.+) (wins|Wins|WINS|receives|received|gets) (.+)", text)
	# if winner2:
	# 	print('')

	# nominees2 = re.findall(r"(.+) (nominated|Nominated|nominee|Nominee) (.+)", text)
	# if nominees2:
	# 	print(nominees2[0])

print(nominees)
print(freq)
print(len(found))

max_freq = max(freq)
max_index = freq.index(max_freq)
winner = nominees[max_index]

print('Winner: ' + winner)

for i in range(len(freq)):
	if freq[i] > 100:
		print(nominees[i] + ' ' + str(freq[i]) + ' ' + str(sentiment[i]))




