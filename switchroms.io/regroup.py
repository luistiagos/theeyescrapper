import pandas as pd

# Load the CSV file with semicolon separator
#df = pd.read_csv('output.csv', sep=';')

# Filter rows where TYPE is "NSP ROM" or "XCI ROM"
#filtered_df = df[df['TYPE'].isin(['NSP ROM'])]

# Save the filtered DataFrame to a new CSV file
#filtered_df.to_csv('filtered_output.csv', sep=';', index=False)

# Load the CSV file with semicolon separator
file_path = "filtered_output.csv"  # Change this to your file path
df = pd.read_csv(file_path, sep=';')

# Group by 'NAME' and collect links into a list
grouped = df.groupby('NAME')['LINK'].apply(list).reset_index()

# Determine the maximum number of links per NAME
max_links = grouped['LINK'].apply(len).max()

# Create columns link1, link2, ..., based on the number of links
link_columns = {f'link{i+1}': [] for i in range(max_links)}

# Fill each new column with the corresponding link or None if not available
for links in grouped['LINK']:
    for i in range(max_links):
        if i < len(links):
            link_columns[f'link{i+1}'].append(links[i])
        else:
            link_columns[f'link{i+1}'].append(None)

# Construct the final DataFrame
final_df = grouped.drop(columns='LINK')
for col, values in link_columns.items():
    final_df[col] = values

# Optional: Save to a new CSV
final_df.to_csv("grouped_links_output.csv", sep=';', index=False)

print("CSV saved as 'grouped_links_output.csv'")