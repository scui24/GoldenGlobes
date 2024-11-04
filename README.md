# GoldenGlobes
# gg-project-Group 3
 
CS337 Project 1 -- Tweet Mining & The Golden Globes 

This project uses a variety of natural language processing (NLP) and text-processing libraries/packages for handling various text-related tasks. The following libraries/packages are included in the project:

## Libraries/Packages Overview
1. **Pandas**: Pandas is a powerful and open-source Python library, used for data manipulation and analysis.
   
2. **csv**: csv module implements classes to read and write tabular data in CSV format.
   
3. **re**: re is a Python built-in package, which can be used to work with Regular Expressions.
   
4. **Unidecode**: Converts Unicode text (e.g., accented characters) into ASCII text, useful for simplifying text handling.
   
5. **SpaCy**: A powerful NLP library for advanced text processing such as tokenization, lemmatization, named entity recognition, etc.
    - Model: `en_core_web_sm` (Small English model for NLP tasks).
      
6. **VADER Sentiment Analysis**: VADER (Valence Aware Dictionary and sEntiment Reasoner) is a lexicon and rule-based sentiment analysis tool that is specifically attuned to sentiments expressed in social media, and works well on texts from other domains.
   
7. **FTFY**: Fixes text encoding issues, like repairing mojibake (encoding errors), and ensures proper display of text.
   
8. **FuzzyWuzzy** is a Python library which is used for string matching. Fuzzy string matching is the process of finding strings that match a given pattern.
   
9.  **tqdm** is a Python library that provides a fast, extensible progress bar for loops and iterables, making it easy to visualize the progress of your code.
   
10. **NLTK**: The Natural Language Toolkit (NLTK) is a comprehensive library for working with human language data (text) in Python, including text classification, tokenization, stemming, tagging, parsing, and more.
    
 

## Setup Instructions

The setup process automates the creation of a Conda environment, installs and downloads the required libraries from a `environment.yml` file. 

## Group 3 Github Repository
 You can access our group's Github repository through following address: https://github.com/scui24/GoldenGlobes.git
 

## Steps to run the the python files in the submission folder
Step 1: Input into submission folder gg{year}.jsonl 

Step 2: Open conversion.py and change the year to match the year of the data. 

Step 3: Run conversion.py  

Step 4. Run gg2013.py 

Step 5. Run extra_tasks.py 

Step 6. Run final_format.py. Final_format.py will print out the human-readable format and save the autograder format to gg{year}answers.py





