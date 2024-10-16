import pandas as pd

file_path = 'output.csv'
df = pd.read_csv(file_path)

subset_df = df.head(10000)

subset_file_path = 'subset.csv'
subset_df.to_csv(subset_file_path, index=False)