import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse, urlunparse

def get_origem(url):
    # Quebra a URL em partes
    parsed = urlparse(url)
    # Remove a última parte do caminho
    new_path = '/'.join(parsed.path.strip('/').split('/')[:-1])
    # Remonta a URL
    return urlunparse((parsed.scheme, parsed.netloc, '/' + new_path, '', '', ''))


def scrap(file, base_url, format='zip'):
    origem = get_origem(base_url)
    # Faz a requisição HTTP
    response = requests.get(base_url)
    response.raise_for_status()

    # Faz o parse do HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontra a TABELA principal
    table = soup.find('table')

    # Lista para guardar os dados
    data = []

    # Percorre as linhas da tabela (ignorando cabeçalho)
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        if len(cols) >= 2:
            link_tag = cols[0].find('a')
            if link_tag and link_tag.get('href'):
                file_name = link_tag.text.strip()
                if file_name.lower().endswith('.zip') or file_name.lower().endswith('.chd') or file_name.lower().endswith('.iso'):
                    file_url = urljoin(base_url, link_tag.get('href').strip())
                    file_size = cols[2].text.strip() if len(cols) > 2 else 'Desconhecido'

                    data.append({
                        'path': file_name,
                        'link': file_url,
                        'size': file_size,
                        'format': format,
                        'origem': origem
                    })

    # Escreve o CSV
    with open(file, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['path', 'link', 'size', 'format', 'origem']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for item in data:
            writer.writerow(item)

    print(f"CSV gerado com sucesso: {file}")

# URL da página
base_url = 'https://archive.org/download/DreamcastCHD2020_P-Z'
file = 'dreamcastchd.csv'
scrap(file, base_url)