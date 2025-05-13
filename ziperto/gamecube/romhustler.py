import requests, bs4, json, time, re, csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


urlPrincipal = 'https://romhustler.org/roms/saturn'


def scrapper(driver, url, rom_writer):
    driver.get(url)
    WebDriverWait(driver, 60).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="roms_table"]/div[2]/div[1]/a')))
    html = driver.page_source
    soup = bs4.BeautifulSoup(html, 'html.parser')
    host = 'https://romhustler.org/'
    
    for link in soup.select('.title a'):
        if link.text != 'Game Name':
            colunas = [link.text]
            print(link.text)
            
            driver.get(host + link.attrs['href'])
            WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="section"]/div/div[3]/div/div/div[1]/div/div[3]/div[2]')))
            ssoup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
            driver.get(host + ssoup.select('.overview ul li a').attrs['href']) 
            WebDriverWait(driver, 50).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="ignore"]')))
            ssoup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
            downloadLink = url + ssoup.select('.downloadLink').attrs['href']
            colunas.append(downloadLink)
            print(downloadLink)
            
            if len(colunas) > 1:
                rom_writer.writerow(colunas)
                
            driver.execute_script('window.history.go(-2)')
            WebDriverWait(driver, 50).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="roms_table"]')))

option = Options()
option.headless = False
driver = webdriver.Firefox(options=option)

url = urlPrincipal
driver.get(url)
WebDriverWait(driver, 50).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="roms_table"]')))
soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')

try:
    with open('roms.csv', mode='a', newline='', encoding="utf-8") as roms_file:
        rom_writer = csv.writer(roms_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        scrapper(driver, url, rom_writer)
       
          
finally:
    driver.quit()
