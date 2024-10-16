# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv

# Importing the dataset
dataset = pd.read_csv('output.csv')

# Cleaning the texts
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('words')
words = set(nltk.corpus.words.words())

from nltk.stem.porter import PorterStemmer
from ftfy import fix_text
import unidecode

corpus = []
for i in range(0, len(dataset['text'])):
  if (type(dataset['text'][i]) is not type("str")):
    print(int(i + 2))
    corpus.append("error")
    continue
  # print('original: ' + dataset['text'][i])
  
  review = fix_text(dataset['text'][i])
  review = unidecode(review) # remove emojis
  # review = re.sub('[^a-zA-Z]', ' ', dataset['text'][i]) # remove everything that is not a letter
  review = re.sub(r'http\S+', '', review) # remove url
  review = = " ".join(review.split()) # remove white spaces
  review = re.sub(' +', ' ', review) # keep tab

# lang detect remain

  review = review.lower()
  review = review.split()
  ps = PorterStemmer()
  all_stopwords = stopwords.words('english')
  all_stopwords.remove('not')
  review = [ps.stem(word) for word in review if not word in set(all_stopwords)]
  review = ' '.join(review)
  review = ' '.join(re.sub("(#[A-Za-z0-9]+)|(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",dataset['text'][i]).split())
  review = ' '.join(w for w in nltk.wordpunct_tokenize(review) if w.lower() in words)
  review = ''.join("" if c.isdigit() else c for c in review)
  corpus.append(review)
# print(corpus)

# Writing the csv file
# fields = ['id', 'cleaned_text']

# filename = "Twitter_Dataset.csv"

# data = []

# for i in range(0, 49408):
#   tmp = []
#   tmp.append(dataset['id'][i])
#   tmp.append(corpus[i])
#   data.append(tmp)

# with open(filename, 'w', newline = '') as csvfile:
#    csvwriter = csv.writer(csvfile)
#    csvwriter.writerow(fields)
#    csvwriter.writerows(data)