import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('switch_base.csv', sep=';')

# Define the substrings to search for
substrs = ['gofile', 'huggingface', 'archive', 'drive.google.com']

# Filter rows where LINK column contains any of the substrings
filtered_df = df[df['LINK'].str.contains('|'.join(substrs), case=False, na=False)]

# Example: print or save the filtered DataFrame
filtered_df.to_csv('filtered_switch_base.csv', index=False, sep=';')