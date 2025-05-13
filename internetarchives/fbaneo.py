import requests
from bs4 import BeautifulSoup
import urllib.request
import csv

def tiny_url(url):
    url = url.replace(" ", "%20")
    apiurl = "http://tinyurl.com/api-create.php?url="
    tinyurl = urllib.request.urlopen(apiurl + url).read()
    return tinyurl.decode("utf-8")

def scrap(url):
    response = requests.get(url)
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all the links on the webpage
    links = soup.find_all('a')
    
    with open('arcadegames.csv', 'a', newline='', encoding="utf-8") as csvfile:
        csvwriter  = csv.writer(csvfile, delimiter=';')
        
        for link in links:
            if '.zip' in link.text:
                name = link.text.replace('.zip', '').strip()
                game = scrapGameName(name)
                link = url + '/' + link['href'] #tiny_url(url + '/' + link['href'])
                csvwriter.writerows([[game, link]])
                print(game + ':' + link)        
            
def scrapGameName(name):
    url = f'http://adb.arcadeitalia.net/dettaglio_mame.php?game_name={name}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    game = soup.find('div', {'id':'game_description'})
    if game == None:
        return name
    return soup.find('div', {'id':'game_description'}).text
    
#url = 'https://archive.org/download/fbnarcade-fullnonmerged/arcade/'
#scrap(url)

print(tiny_url('https://archive.org/download/jogos_antigosdepc/DOOM Enhanced(1.0) (58062) (GOG).rar'))