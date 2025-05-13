import requests
from bs4 import BeautifulSoup
import csv, urllib

def tiny_url(url):
    apiurl = "http://tinyurl.com/api-create.php?url="
    tinyurl = urllib.request.urlopen(apiurl + url).read()
    return tinyurl.decode("utf-8")

def scrap(url):
    response = requests.get(url)
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all the links on the webpage
    links = soup.find_all('a')
    
    with open('Jogos_xbox360_br.csv', 'a', newline='', encoding="utf-8") as csvfile:
        csvwriter  = csv.writer(csvfile, delimiter=';')
        
        for link in links:
            if '.zip' in link.text or '.rar' in link.text or '7z' in link.text:
                name = link.text.replace('.zip', '').strip().replace('.rar', '').strip().replace('.7z', '').strip()
                link = url + '/' + link['href']
                link = tiny_url(link)
                csvwriter.writerows([[name, link]])
                print(name + ':' + link) 
                
url = 'https://isodows.blogspot.com/2020/04/colecao-games-pt-br-via-torrent-xbox-360.html'
scrap(url)     