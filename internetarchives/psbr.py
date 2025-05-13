import requests
from bs4 import BeautifulSoup
import urllib.request
import csv

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
    
    with open('teknoparrot.csv', 'a', newline='', encoding="utf-8") as csvfile:
        csvwriter  = csv.writer(csvfile, delimiter=';')
        
        for link in links:
            if '.zip' in link.text or '.7z' in link.text:
                name = link.text
                link = tiny_url(url + '/' + link['href'])#url + '/' + link['href']
                csvwriter.writerows([[name, link]])
                print(name + ':' + link)        
            
    
url = 'https://archive.org/download/TeknoparrotGamesFull'
scrap(url)