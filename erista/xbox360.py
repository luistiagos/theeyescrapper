import requests
from bs4 import BeautifulSoup
import csv

def scrap(url):
    response = requests.get(url)
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all the links on the webpage
    links = soup.find_all('a')
    
    with open('Playstation 3 Traduzidos.csv', 'a', newline='', encoding="utf-8") as csvfile:
        csvwriter  = csv.writer(csvfile, delimiter=';')
        
        for link in links:
            if '.zip' in link.text and ('Brazil' in link.text or 'Pt,' in link.text):
                name = link.text.replace('.zip', '').strip()
                size = link.parent.parent.find_all('td')[1].text
                link = url + '/' + link['href']
                format = 'ZIP'
                csvwriter.writerows([[name, link, size, format, url]])
                print(name + ':' + link) 
                
url = 'https://myrient.erista.me/files/No-Intro/Sony%20-%20PlayStation%203%20(PSN)%20(Content)/'
scrap(url)     