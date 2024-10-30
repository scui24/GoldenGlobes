import pandas as pd
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from ftfy import fix_text
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import spacy
from tqdm import tqdm  # Progress bar


nlp = spacy.load("en_core_web_sm")

sid_obj = SentimentIntensityAnalyzer()
dataset = pd.read_csv('output.csv')


def sentiment_scores(sentence):
    return sid_obj.polarity_scores(sentence)['compound']

def preprocess(text):
    text = re.sub(r"\b(Yay+|Congrats|Yess+|And|Aaaand|Official)\b", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


pattern_winner_award = r"(?<!\w)([A-Z][a-zA-Z]*(?:\s[A-Z][a-zA-Z]*)*)\s(?:wins|receives|takes|gets|awarded)\s(Best [\w\s]+?(?:\sfor\s[\w\s]+?)?)(?=\s(?:for|in|at|by|$)|$)"

nominees, awards, freq, sentiment = [], [], [], []

for tweet in tqdm(dataset['text'], desc="Processing Tweets"):
    if not isinstance(tweet, str):
        continue

 
    text = preprocess(fix_text(tweet))
    match = re.search(pattern_winner_award, text)
    
    if match:
        winner_name, award_name = match.group(1), match.group(2)  


        doc = nlp(text)
        spaCy_detected = False
        for ent in doc.ents:
            if ent.label_ == "PERSON" and fuzz.token_sort_ratio(ent.text, winner_name) > 80:
                winner_name = ent.text  
                spaCy_detected = True
                break

        if not spaCy_detected:
            continue

     
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

#sentiment 
for i in range(len(sentiment)):
    sentiment[i] /= freq[i]


max_freq = max(freq)
winner = nominees[freq.index(max_freq)]
print('Winner:', winner)
print('Award:', awards[freq.index(max_freq)])


for i in range(len(freq)):
    print(f"Nominee: {nominees[i]}, Award: {awards[i]}, Mentions: {freq[i]}, Avg Sentiment: {sentiment[i]:.2f}")
