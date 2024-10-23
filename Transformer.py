
import pandas as pd
from transformers import pipeline

# Load your dataset
dataset = pd.read_csv('subset2.csv')

# Load the RoBERTa Question Answering model
qa_pipeline = pipeline('question-answering', model="distilbert-base-uncased-distilled-squad")

combined_tweets = " ".join(dataset['text'].tolist())


# Example questions (you can change these based on your target information)
questions = [
    # "What is the Golden Globe award mentioned?",
    "Who is the winner of Best Actor?",
    "Who are the hosts of the Golden Globe award?"
    # "Who is the nominee?"
]

def ask_questions_on_combined_context(context, questions):
    results = {}
    for question in questions:
        try:
            # Use the combined context for Q&A
            result = qa_pipeline(question=question, context=context)
            results[question] = result['answer'] if result['score'] > 0.5 else "No answer"
        except Exception as e:
            results[question] = "Error"
    return results

# Ask questions based on the entire dataset (combined tweets)
qa_results = ask_questions_on_combined_context(combined_tweets, questions)

# Display the answers
for question, answer in qa_results.items():
    print(f"Question: {question}\nAnswer: {answer}\n")