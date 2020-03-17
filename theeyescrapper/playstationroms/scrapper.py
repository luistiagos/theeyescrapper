import requests, bs4, json, time
import urllib.request
import sys
import csv

def tiny_url(url):
    apiurl = "http://tinyurl.com/api-create.php?url="
    tinyurl = urllib.request.urlopen(apiurl + url).read()
    return tinyurl.decode("utf-8")


def scrapper(url):
  res = requests.get(url)
  res.raise_for_status()
  soup = bs4.BeautifulSoup(res.text, "html.parser")
  list = []  

  for link in soup.findAll('a'):
    if '.zip' in link.get('href') or '.rar' in link.get('href'):
      href = tiny_url(url + link.get('href')) 
      list.append([link.contents[0], href])
      print(href)
  
  return list

list = scrapper('https://the-eye.eu/public/rom/Sega%20Dreamcast/')


with open('ROMS_DREAMCAST.csv', 'w+', newline='') as file:
    writer = csv.writer(file)
    for rom in list:
        writer.writerow(rom)

print('Complete')