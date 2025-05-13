import requests
import pandas as pd

def shortl(url):
    payload = { "url": url }
    headers = {
	    "content-type": "application/x-www-form-urlencoded",
	    "X-RapidAPI-Key": "uxTxNF5cpumshsykIcPvFdnfHZWBp1SKXxYjsnZlfLHKit8EOR",
	    "X-RapidAPI-Host": "url-shortener-service.p.rapidapi.com"
    }
    response = requests.post(url, data=payload, headers=headers)
    return response.json()

def modify_links(csv_file):
    df = pd.read_csv(csv_file, sep=';')

    df['modified_link'] = df.apply(lambda row: shortl(row['link']), axis=1)

    modified_csv_file = 'modified_links.csv'
    df.to_csv(modified_csv_file, index=False)

    print(f"Modified links saved to {modified_csv_file}")
    
    
modify_links('xbox360.csv')