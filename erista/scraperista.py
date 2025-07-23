import requests
from bs4 import BeautifulSoup
import csv, urllib
from urllib.parse import urlparse, urlunparse

def tiny_url(url):
    apiurl = "http://tinyurl.com/api-create.php?url="
    tinyurl = urllib.request.urlopen(apiurl + url).read()
    return tinyurl.decode("utf-8")

def get_origem(url):
    # Quebra a URL em partes
    parsed = urlparse(url)
    # Remove a última parte do caminho
    new_path = '/'.join(parsed.path.strip('/').split('/')[:-1])
    # Remonta a URL
    return urlunparse((parsed.scheme, parsed.netloc, '/' + new_path, '', '', ''))

def scrap(filename, url, format):
    response = requests.get(url)
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all the links on the webpage
    links = soup.find_all('a')
    #begin = False

    with open(filename, 'a', newline='', encoding="utf-8") as csvfile:
        csvwriter  = csv.writer(csvfile, delimiter=';')
        csvwriter.writerow(['path','link','size','format','origem'])

        for link in links:
            if 'wbfs' in link.text or 'zip' in link.text or 'chd' in link.text or '7z' in link.text or 'rvz' in link.text:
                name = link.text #link.text.replace('.zip', '').strip()
                #if not begin and 'Rock Band - Metal Track Pack (USA, Canada).zip' in name.strip():
                #    begin = True
                
                #if not begin:
                #    continue

                size = link.parent.parent.find_all('td')[1].text
                link = url + link['href']
                #try:
                #    link = tiny_url(link)
                #except:
                #    pass
                origem = get_origem(url)
                csvwriter.writerows([[name, link, size, format, origem]])
                print(name + ':' + link) 
                
url = 'https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy%20Advance/'
scrap('gba.csv', url, 'ZIP')    