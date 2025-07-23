import time
import requests
from bs4 import BeautifulSoup
import csv
import json

output_file = 'output.csv'

def scrap(url):
    response = requests.get(url)
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all the links on the webpage
    listpost = soup.find('div', class_='list-post')

    with open(output_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['Game', 'Type', 'Size', 'Server', 'URL']) 

        for lnk in listpost.find_all('a'):
            if 'href' in lnk.attrs:
                rom = {'name': lnk.find('div', class_='body-content').find('h3').text.strip(), 'resources': []}    
                rom = scrap_item(lnk['href'], rom)
                if not rom:
                    continue

                print(rom['name'])
                for res in rom['resources']:
                    writer.writerow([
                        rom['name'],
                        res.get('type', ''),
                        res.get('size', ''),
                        res.get('server', ''),
                        res.get('url', '')
                    ])

    #return data


def get_url(url, tries=3):
    try: 
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all the links on the webpage
        link = soup.find('div', id='download-active').find('a')['href']
        return link
    except Exception as e:
        if tries <= 0:
            print(f"Failed to process {url} after multiple attempts.")
            return None
        tries -= 1
        print(f"Error processing {url}: {e}")
        time.sleep(5)
        return get_url(url, tries) 


def download_page(url, rom, tries=3):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all the links on the webpage
        links = soup.find('div', class_='download-list').find_all('a')
        rom['resources'] = []
        for link in links:
            if 'href' in link.attrs:
                url_rom = get_url(link['href'])
                if not url_rom:
                    continue
                content = link.find('span').text.strip()
                attrs = content.split('|')
                tipe = attrs[0].strip()
                size = attrs[1].strip() if len(attrs) > 1 else ''
                server = attrs[2].strip() if len(attrs) > 2 else ''
                resource = {'type': tipe, 'size': size, 'server': server, 'url': url_rom}
                rom['resources'].append(resource)

        return rom
    except Exception as e:
        if tries <= 0:
            print(f"Failed to process {url} after multiple attempts.")
            return rom
        tries -= 1
        print(f"Error processing {url}: {e}")
        time.sleep(5)
        return download_page(url, rom, tries)


def scrap_item(url, rom, tries=3):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all the links on the webpage
        button = soup.find('button', class_='get-more-btn')
        link = button.parent if button else None
        if link:
            rom = download_page(link['href'], rom)
        return rom
    except Exception as e:
        if tries <= 0:
            print(f"Failed to process {url} after multiple attempts.")
            return rom
        tries -= 1
        print(f"Error processing {url}: {e}")
        time.sleep(5)
        scrap_item(url, rom, tries)


def to_csv(data):
    # Write CSV
    with open(output_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['Game', 'Type', 'Size', 'Server', 'URL'])  # Header

        for game in data:
            game_name = game['name']
            for res in game['resources']:
                writer.writerow([
                    game_name,
                    res.get('type', ''),
                    res.get('size', ''),
                    res.get('server', ''),
                    res.get('url', '')
                ])

    print(f'CSV file "{output_file}" created successfully.')


def main():                
    url = 'https://switchroms.io/nintendo-switch-games/'
  
    with open(output_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['Game', 'Type', 'Size', 'Server', 'URL'])  # Header

    #print('Page: ', url)
    #scrap(url)   
    for i in range(23, 24):
        page = f'{url}page/{i}/'
        print('Page: ', page)
        scrap(page)
            #for item in data_page:
            #    data.append(item)
    
    #with open('output.json', 'w', encoding='utf-8') as f:
    #    json.dump(data, f, ensure_ascii=False, indent=2)
    
    #print('JSON file "output.json" created successfully.')
    
    #to_csv(data)

main()