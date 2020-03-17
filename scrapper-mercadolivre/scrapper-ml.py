import requests, bs4, json, time
import csv

def getText(tag):
    if len(tag) == 1:
        return tag[0].getText().strip()
    return ""

def getPreco(item):
    priceFraction = getText(item.select('.price__fraction'))
    priceDecimalTag = item.select('.price__decimals')
    priceDecimal = 0
    if len(priceDecimalTag) == 1:
        priceDecimal = getText(item.select('.price__decimals'))
    return float(priceFraction + '.' + str(priceDecimal)) 

def isFreteGratis(item):
    textShippingTag = item.select('.text-shipping')
    return len(textShippingTag) == 1

def populaInfos(product):
    r = requests.get(product['url'], stream=True, headers={'User-agent': 'Mozilla/5.0'})
    html = bs4.BeautifulSoup(r.text, "html.parser")
    itensCond = getText(html.select('.item-conditions')).split('-');
    product['condicao'] = itensCond[0].strip()
    if len(itensCond) > 1:
        product['vendidos'] = itensCond[1].strip().split('\n\t\t\t\t')[0].strip()
    product['estrelas'] = getText(html.select('.review-summary-average'))  
    product['qtd-perguntas'] = len(html.select('.questions__list li'))
    if product['qtd-perguntas'] > 0:
        product['data-ultima-pergunta'] = getText(html.select('.questions__list li')[0].select('.questions__time'))
        
def scrapperPage(url, products):
    r = requests.get(url, stream=True, 
                    headers={'User-agent': 'Mozilla/5.0'})
    html = bs4.BeautifulSoup(r.text, "html.parser")
    itens = html.select('.rowItem')
    for item in itens:
        product = {
            "preco": getPreco(item),
            "freteGratis": isFreteGratis(item),
            "nome": getText(item.select('.main-title')),
            "url": item.select('.item__info-link')[0]['href'],
            "condicao": None,
            "vendidos": None,
            "estrelas": None,
            "qtd-perguntas": None,
            "data-ultima-pergunta": None
        }
        populaInfos(product)
        products.append(product)
    
    nextTag = html.find('span', string='Próxima')
    if (nextTag != None):
        nextUrl = html.find('span', string='Próxima').parent['href']
        scrapperPage(nextUrl, products)
    
    with open('anuncios.csv', 'w+', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['nome', 'preco', 'url', 'vendidos', 'estrelas', 'qtd-perguntas', 
                             'data-ultima-pergunta', 'freteGratis', 'condicao'])
        for linha in products:
            spamwriter.writerow([linha['nome'], linha['preco'], linha['url'], 
                                 linha['vendidos'], linha['estrelas'], linha['qtd-perguntas'],
                                 linha['data-ultima-pergunta'], linha['freteGratis'], linha['condicao']])

def main(produto):
    url = 'https://lista.mercadolivre.com.br/' + produto
    products = []
    scrapperPage(url, products)
    
 
main('relogio gemyus army')
