import requests
from bs4 import BeautifulSoup
import urllib.request
import csv, time
import ouobypass as ouo
from selenium import webdriver
import undetected_chromedriver as uc
import pandas as pd

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


def scrap(driver, titlestart=None):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    lis = soup.find('ul', {'class':'lcp_catlist'}).find_all('li')
    run = True
    with open('switchroms_list.csv', 'a', newline='', encoding="utf-8") as csvfile:
        csvwriter  = csv.writer(csvfile, delimiter=';')
        for li in lis:
            a = li.find('a')
            if a != None:
                if 'nsp' in a['href'] or 'xci' in a['href']:
                    if run == False and titlestart in a.text:
                        run = True
                        continue
                    if run:
                        try:
                            csvwriter.writerows([[a.text, a['href']]])
                        except Exception as e:
                            print('error', str(e))
         
def list_games():
    driver = createDrive(False)
    for i in range(1,6):
        print('PAGE:' + str(i))
        url = 'https://nsw2u.net/switch-posts?lcp_page0=' + str(i)
        driver.get(url)
        scrap(driver)
    driver.quit()
    
def missing_games():
    df_upd = pd.read_csv('switchgames.csv', sep=';')
    df_orig = pd.read_csv('switchroms_list.csv', sep=';')
    df_upd['title'] = df_upd['title'].apply(lambda x: x[:x.find('Base')] if 'Base' in x else x)
    df_upd['title'] = df_upd['title'].apply(lambda x: x.strip())
    df_orig['title'] = df_orig['title'].apply(lambda x: x.strip())
    df_res = df_orig[~df_orig['title'].isin(df_upd['title'])]
    df_res.to_csv('switchnew.csv', index=False)

