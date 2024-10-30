import pandas as pd
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from ftfy import fix_text
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import spacy
from tqdm import tqdm  # Progress bar
import json

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")
sid_obj = SentimentIntensityAnalyzer()
dataset = pd.read_csv('output.csv')

# Helper functions
def sentiment_scores(sentence):
    return sid_obj.polarity_scores(sentence)['compound']

def preprocess(text):
    text = re.sub(r"\b(Yay+|Congrats|Yess+|And|Aaaand|Official)\b", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# Patterns for winners and nominees
pattern_winner_award = r"(?<!\w)([A-Z][a-zA-Z]*(?:\s[A-Z][a-zA-Z]*)*)\s(?:wins|receives|takes|gets|awarded)\s(Best [\w\s]+?(?:\sfor\s[\w\s]+?)?)(?=\s(?:for|in|at|by|$)|$)"
pattern_nominee = r"(?<!\w)([A-Z][a-zA-Z]*(?:\s[A-Z][a-zA-Z]*)*)\s(?:nominated for|up for|a nominee for)\s(Best [\w\s]+?(?:\sfor\s[\w\s]+?)?)(?=\s(?:for|in|at|by|$)|$)"

# Initialize lists
nominees, awards, freq, sentiment = [], [], [], []

# Process each tweet
for tweet in tqdm(dataset['text'], desc="Processing Tweets"):
    if not isinstance(tweet, str):
        continue

    text = preprocess(fix_text(tweet))
    
    # Match winners
    match_winner = re.search(pattern_winner_award, text)
    if match_winner:
        winner_name, award_name = match_winner.group(1), match_winner.group(2)

        # Confirm winner name using SpaCy
        doc = nlp(text)
        spaCy_detected = False
        for ent in doc.ents:
            if ent.label_ == "PERSON" and fuzz.token_sort_ratio(ent.text, winner_name) > 80:
                winner_name = ent.text  
                spaCy_detected = True
                break
        if not spaCy_detected:
            continue

        # Handle duplicates and update lists
        similar_name = process.extractOne(winner_name, nominees, scorer=fuzz.token_sort_ratio)
        if similar_name and similar_name[1] > 80:
            idx = nominees.index(similar_name[0])
            freq[idx] += 1
            sentiment[idx] += sentiment_scores(text)
        else:
            nominees.append(winner_name)
            awards.append(award_name)
            freq.append(1)
            sentiment.append(sentiment_scores(text))

    # Match nominees
    match_nominee = re.search(pattern_nominee, text)
    if match_nominee:
        nominee_name, award_name = match_nominee.group(1), match_nominee.group(2)

        # Confirm nominee name with SpaCy
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == "PERSON" and fuzz.token_sort_ratio(ent.text, nominee_name) > 80:
                nominee_name = ent.text
                break

        # Add nominees without affecting the winner lists
        similar_name = process.extractOne(nominee_name, nominees, scorer=fuzz.token_sort_ratio)
        if not similar_name or similar_name[1] < 80:
            nominees.append(nominee_name)
            awards.append(award_name)
            freq.append(1)
            sentiment.append(sentiment_scores(text))

# Calculate average sentiment
for i in range(len(sentiment)):
    sentiment[i] /= freq[i]

# Determine winner
max_freq = max(freq)
winner = nominees[freq.index(max_freq)]
print('Winner:', winner)
print('Award:', awards[freq.index(max_freq)])

# Display nominees
for i in range(len(freq)):
    print(f"Nominee: {nominees[i]}, Award: {awards[i]}, Mentions: {freq[i]}, Avg Sentiment: {sentiment[i]:.2f}")

# Save results to JSON
results = {
    'winner': {'name': winner, 'award': awards[freq.index(max_freq)]},
    'nominees': [{'name': nominees[i], 'award': awards[i], 'mentions': freq[i], 'avg_sentiment': sentiment[i]} for i in range(len(freq))]
}
with open('raw_output.json', 'w') as f:
    json.dump(results, f, indent=4)
print("Results saved to 'raw_output.json'")
