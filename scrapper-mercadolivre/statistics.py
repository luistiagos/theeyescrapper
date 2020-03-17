import pandas as pd

anuncios = pd.read_csv('anuncios.csv', encoding = "ISO-8859-1", engine="python", sep=";")

print(anuncios[anuncios.vendidos > 0].groupby('preco').groupby('nome').vendidos.sum())