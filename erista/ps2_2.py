import requests
from bs4 import BeautifulSoup
import csv  # Import CSV module

# URL of the page to scrape
url = 'https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation%202/'

# Send GET request to the website
response = requests.get(url)

# Parse the page content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all table rows containing file info
table_rows = soup.find_all('tr')

# Open a CSV file to write the data
with open('ps2_files.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter='#')  # Use # as the separator
    writer.writerow(['File Name', 'File Size'])  # Write header row

    # Loop through the table rows and extract file name and size
    for row in table_rows:
        columns = row.find_all('td')
        if len(columns) >= 2:  # Check if there are at least two columns (File Name and Size)
            file_name = columns[0].get_text(strip=True)
            file_size = columns[1].get_text(strip=True)
            writer.writerow([file_name, file_size])  # Write data row
