import requests
from bs4 import BeautifulSoup
import urllib.request
import csv
import ouobypass as ouo
from selenium import webdriver
import undetected_chromedriver as uc

def createDrive(headless=True):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
    options.headless = headless
    #CHROME_DRIVER_PATH = 'C:\chromedriver\chromedriver.exe'
    #driver = uc.Chrome(executable_path=CHROME_DRIVER_PATH, options=options)
    driver = uc.Chrome(version_main=113, executable_path='Webdrivers',options=options)
    return driver

def subscrap(url, title):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    with open('switchroms.csv', 'a', newline='', encoding="utf-8") as csvfile:
        csvwriter  = csv.writer(csvfile, delimiter=';')
        for a in soup.find_all('a'):
            try:
                if 'ouo.io' in a['href']:
                    td = a.parent.parent.find('td')
                    if td == None:
                        td = a.parent.find('td')
                    if td != None:
                        subtitle = td.text
                        urlouo = ouo.ouo_bypass(a['href'])
                        url = urlouo['bypassed_link']
                        if url != None:
                            t = title + ' ' + subtitle
                            csvwriter.writerows([[t, url]])
                            print(title + ' ' + url)
            except Exception as e:
                #print('error 2', str(e))
                pass


def scrap(url, titlestart=None):
    #response = requests.get(url)
    driver = createDrive(False)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    entry = soup.find('div', {'class':'entry-content'})
    table = entry.find_all('table')[-1]
    divs = table.find('tr').find('td').find_all('div')
    run = False
    for div in divs:
        lis = div.find_all('li')
        for li in lis:
            a = li.find('a')
            if a != None:
                if 'nsp' in a['href'] or 'xci' in a['href']:
                    if run == False and titlestart in a.text:
                        run = True
                        continue
                    if run:
                        try:
                            subscrap(a['href'], a.text)
                            #if 'Chubby Cat 2' in a['title']:
                            #    run = True
                        except Exception as e:
                            print('error', str(e))
         
def main():
    url = 'https://nsw2u.com/switch-posts'
    scrap(url)
        
    
main()
