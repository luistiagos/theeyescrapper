import pandas as pd
import json

def convert_to_kb(size_str):
    if 'GiB' in size_str:
        size = float(size_str.replace(' GiB', '').strip()) * 1024 * 1024 * 1024
    elif 'MiB' in size_str:
        size = float(size_str.replace(' MiB', '').strip()) * 1024 * 1024
    elif 'KB' in size_str:
        size = float(size_str.replace(' KB', '').strip()) * 1024
    else:
        size = float(size_str.replace(' Bytes', '').strip()) 
    return int(size)

# Read CSV file using pandas
csv_file = 'mx360gcxpt1-x360-ztm.csv'
df = pd.read_csv(csv_file, delimiter=';', header=None, names=['name','link','size','format','origem'])

# Create the JSON output structure
json_output = {"files": {}}

# Iterate through the DataFrame rows
for index, row in df.iterrows():
    if 'name' not in row['name']:
        name = row['name']
        link = row['link']
        size = row['size']
        format_type = row['format']
        origem = row['origem']

        json_output["files"][f"/{name}"] = {
            "source": "original",
            "origem": origem,
            "size": convert_to_kb(size),
            "link": link,
            "format": format_type
        }

# Convert the JSON structure to a formatted string
json_str = json.dumps(json_output, indent=4)

# Print or save the JSON output
print(json_str)
