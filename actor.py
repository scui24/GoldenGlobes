import pandas as pd
import csv
import re
import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.stem.porter import PorterStemmer
from ftfy import fix_text
import unidecode
from nltk.corpus import stopwords

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

dataset = pd.read_csv('output.csv')

found = []
nominees = []
freq = []
sentiment = []
for i in range(0, len(dataset['text'])):
	if (type(dataset['text'][i]) is not type("str")):
	    print(int(i + 2))
	    corpus.append("error")
	    continue

	# nltk.download('stopwords')
	# nltk.download('words')
	# words = set(nltk.corpus.words.words())

	# review = fix_text(dataset['text'][i])
	# # review = unidecode(review) # remove emojis
	# review = re.sub(r'http\S+', '', review)

	# review = review.lower()
	# review = review.split()
	# ps = PorterStemmer()
	# all_stopwords = stopwords.words('english')
	# review = [ps.stem(word) for word in review if not word in set(all_stopwords)]
	# print(type(review))
	# review = ' '.join(w for w in nltk.wordpunct_tokenize(review) if w.lower() in words)
	# text = review

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




