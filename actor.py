# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import re

# Importing the dataset
dataset = pd.read_csv('subset.csv')

found = []
for i in range(0, len(dataset['text'])):
	if (type(dataset['text'][i]) is not type("str")):
	    print(int(i + 2))
	    corpus.append("error")
	    continue
	pattern = r"best actor"
	name_pattern = r"[A-Z][a-zA-Z'-]+(?:\s[A-Z][a-zA-Z'-]+)*"
	match = re.search(pattern, dataset['text'][i], re.IGNORECASE)
	if match:
		found.append(dataset['text'][i])
