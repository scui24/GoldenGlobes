import pandas as pd
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from ftfy import fix_text
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Initialize tools
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
sid_obj = SentimentIntensityAnalyzer()
dataset = pd.read_csv('output.csv')

# Define helper functions
def sentiment_scores(sentence):
    return sid_obj.polarity_scores(sentence)['compound']

def preprocess(text):
    text = re.sub(r"\b(Yay+|Congrats|Yess+|And|Aaaand|Official)\b", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# Refined pattern to capture structured award names
pattern_winner_award = r"(?<!\w)([A-Z][a-zA-Z]*(?:\s[A-Z][a-zA-Z]*)*)\s(?:wins|receives|gets|awarded)\s(Best [\w\s]+)(?=\s|$)"

nominees, awards, freq, sentiment = [], [], [], []

# Process each tweet in the dataset
for tweet in dataset['text']:
    if not isinstance(tweet, str):
        continue

    # Pre-process and apply the regex pattern
    text = preprocess(fix_text(tweet))
    match = re.search(pattern_winner_award, text)
    if match:
        winner_name = match.group(1)  # Extract the winner's name
        award_name = match.group(2)  # Extract the award title

        # Discard unlikely awards
        if not re.match(r"Best (Actor|Actress|Picture|Director|Screenplay|Series|Score|Song|Miniseries)", award_name):
            continue  # Skip non-standard award names

        # Fuzzy match for duplicate or similar names
        similar_name = process.extractOne(winner_name, nominees, scorer=fuzz.token_sort_ratio)
        if similar_name and similar_name[1] > 80:  # Threshold for similarity
            idx = nominees.index(similar_name[0])
            freq[idx] += 1
            sentiment[idx] += sentiment_scores(text)
        else:
            nominees.append(winner_name)
            awards.append(award_name)
            freq.append(1)
            sentiment.append(sentiment_scores(text))

# Calculate average sentiment for each nominee
for i in range(len(sentiment)):
    sentiment[i] /= freq[i]

# Identify the most mentioned nominee as the likely winner
max_freq = max(freq)
winner = nominees[freq.index(max_freq)]
print('Winner:', winner)
print('Award:', awards[freq.index(max_freq)])

# Display results
for i in range(len(freq)):
    print(f"Nominee: {nominees[i]}, Award: {awards[i]}, Mentions: {freq[i]}, Avg Sentiment: {sentiment[i]:.2f}")
