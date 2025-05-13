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
    
    with open('ps2gamess.csv', 'a', newline='', encoding="utf-8") as csvfile:
        csvwriter  = csv.writer(csvfile, delimiter=';')
        
        for link in links:
            if '.zip' in link.text:
                name = link.text.replace('.zip', '').strip()
                link = url + '/' + link['href']
                csvwriter.writerows([[name, link]])
                print(name + ':' + link) 
                
url = 'https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation%202/'
scrap(url)     