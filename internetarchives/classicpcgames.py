import requests

url = "https://archive.org/details/classicpcgames?output=json"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    captures = data['archived_snapshots']
    
    for timestamp, info in captures.items():
        print("Timestamp:", timestamp)
        print("URL:", info['url'])
else:
    print("Não foi possível obter os dados.")
