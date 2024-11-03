import pandas as pd
from collections import Counter
from textblob import TextBlob
from tqdm import tqdm
import spacy
import json
import re


nlp = spacy.load("en_core_web_sm")


tweets = pd.read_csv("output.csv")

non_name_words = {"Golden", "Globes", "Best", "Award", "Wins", "Receives"}


def quick_extract_names(text):
   
    names = re.findall(r'\b[A-Z][a-z]*\s[A-Z][a-z]*\b', text)
    
    names = [name for name in names if not any(word in name.split() for word in non_name_words)]

    return names


def validate_names(names):
    valid_names = []
    for name in names:
        doc = nlp(name)
        
        if any(ent.label_ == "PERSON" for ent in doc.ents):
            valid_names.append(name)
    return valid_names


def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity


name_counter = Counter()
sentiment_dict = {}


for _, row in tqdm(tweets.iterrows(), total=len(tweets), desc="Processing Tweets"):
    text = row['text'] 
    names = quick_extract_names(text)
    
    
    for name in names:
        name_counter[name] += 1
        sentiment_score = analyze_sentiment(text)
        if name in sentiment_dict:
            sentiment_dict[name].append(sentiment_score)
        else:
            sentiment_dict[name] = [sentiment_score]

top_names = [name for name, _ in name_counter.most_common(100)] 
valid_names = validate_names(top_names)


filtered_name_counter = {name: count for name, count in name_counter.items() if name in valid_names}
filtered_sentiment_dict = {name: sentiments for name, sentiments in sentiment_dict.items() if name in valid_names}


most_discussed = Counter(filtered_name_counter).most_common(5)


controversial_names = sorted(
    filtered_sentiment_dict.keys(),
    key=lambda name: -abs(max(filtered_sentiment_dict[name]) - min(filtered_sentiment_dict[name]))
)[:5]


results = {
    "Most Discussed People": [{"name": name, "mentions": count} for name, count in most_discussed],
    "Most Controversial People": [
        {"name": name, "sentiment_variance": max(filtered_sentiment_dict[name]) - min(filtered_sentiment_dict[name])}
        for name in controversial_names
    ]
}


print("Most Discussed People:")
for entry in results["Most Discussed People"]:
    print(f"{entry['name']}: {entry['mentions']} mentions")

print("\nMost Controversial People:")
for entry in results["Most Controversial People"]:
    print(f"{entry['name']}: Sentiment Variance {entry['sentiment_variance']}")

# save results in JSON file
with open("tweet_analysis_results.json", "w") as json_file:
    json.dump(results, json_file, indent=4)

print("\nResults saved to 'tweet_analysis_results.json'")
