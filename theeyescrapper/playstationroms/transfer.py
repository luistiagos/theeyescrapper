import requests, bs4, json, time
import urllib.request
import sys
import csv


with open('ROMS_NTSC.csv', 'w+', newline='') as fw:
    writer = csv.writer(fw)
    with open('NTSC.csv', 'r', newline='') as fr:
        lines = fr.readlines()
        for rom in lines:
            writer.writerow([rom[:rom.index(';')], rom[rom.index(';')+1:]])

print('Complete')