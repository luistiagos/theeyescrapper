import requests
from bs4 import BeautifulSoup
import csv

def scrap(url):
    response = requests.get(url)
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all the links on the webpage
    links = soup.find_all('a')
    
    with open('Jogos_ps1.csv', 'a', newline='', encoding="utf-8") as csvfile:
        csvwriter  = csv.writer(csvfile, delimiter=';')
        
        for link in links:
            if '.zip' in link.text:
                name = link.text.replace('.zip', '').strip()
                link = url + '/' + link['href']
                csvwriter.writerows([[name, link]])
                print(name + ':' + link) 
                
url = 'https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation/'
scrap(url)     