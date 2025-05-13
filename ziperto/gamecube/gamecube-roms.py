import requests, bs4, json, time, re, csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


urlPrincipal = 'https://www.ziperto.com/nintendo/wii-iso/'

def isLinkValid(link): 
    return link[len(link)-1] != '/' and link not in ['https://www.ziperto.com/winrar-cracked', 
            'https://www.7-zip.org/download.html',
            'https://www.ziperto.com/winrar-cracked-v5-40-final-2016-free-download-3264bi',
            'https://www.ziperto.com/dolphin-gamecube-wii-emulator/'] 

def scrapper(driver, url, rom_writer):
    driver.get(url)
    WebDriverWait(driver, 60).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="page"]/div')))
    html = driver.page_source
    soup = bs4.BeautifulSoup(html, 'html.parser')
    currPage = 0
    if(len(soup.select('.current')) > 0):
        currPage = int(soup.select('.current')[0].text)
    
    for link in soup.select('.article .post'):
        driver.get(link.findAll('a', {"rel" : "bookmark"})[0]['href'])
        WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="page"]/div')))
            
        ssoup = bs4.BeautifulSoup(driver.page_source, 'html.parser')    
        if ssoup.find(text=re.compile('Part – 1')) == None and ssoup.find(text=re.compile('Part 1')) == None:
            colunas = [ssoup.select('.title')[0].text]
            print(ssoup.select('.title')[0].text)
            if len(ssoup.select('.post-single-content strong a')) > 0:
                for tag in ssoup.select('.post-single-content strong a'):
                    if ('href' in tag.attrs) and isLinkValid(tag.attrs['href']):
                        colunas.append(tag.attrs['href'])
                        print(tag.attrs['href'])       
                        
            if len(colunas) > 1:
                rom_writer.writerow(colunas)
                        
        driver.execute_script('window.history.go(-1)')
        WebDriverWait(driver, 60).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="page"]/div')))
    
    return currPage

def saveCurrPage(curpage):
    f= open("currpage.txt","w+")
    try:
        f.write(str(curpage))
    finally:    
        f.close()

option = Options()
option.headless = True
driver = webdriver.Firefox(options=option)

url = urlPrincipal
driver.get(url)
WebDriverWait(driver, 60).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="page"]/div')))
soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')

currPage = int(soup.select('.current')[0].text)
maxPage = int(soup.select('.nav-links a')[2].text)

try:
    while currPage <= maxPage:
        with open('roms.csv', mode='a', newline='', encoding="utf-8") as roms_file:
            rom_writer = csv.writer(roms_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            currPage = scrapper(driver, url, rom_writer)
            currPage = currPage + 1
            url = 'https://www.ziperto.com/nintendo/wii-iso/page/' + str(currPage) + '/'
            saveCurrPage(currPage)
finally:
    driver.quit()
