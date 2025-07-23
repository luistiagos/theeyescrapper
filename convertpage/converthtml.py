import csv

def gerar_html(csv_path, template_path, titulo):
    # Lê o CSV e monta as linhas da tabela
    linhas_html = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            path = row['path']
            link = row['link']
            size = row['size'].replace('MiB', 'MB').replace('GiB', 'GB')
            linha = f'<tr><td><a href="{link}" referrerpolicy="no-referrer">{path}</a></td><td>{size}</td></tr>'
            linhas_html.append(linha)
    
    # Lê o template
    with open(template_path, 'r', encoding='utf-8') as f:
        html_template = f.read()

    # Injeta as linhas dentro do <tbody id="tableBody">
    html_completo = html_template.replace(
        '<!-- INJETAR TITULO -->', titulo).replace(
            '<!-- INJETAR SUBTITULO -->', titulo).replace(
        '<!-- INJETAR AQUI -->',
        '\n'.join(linhas_html)
    )

    output_path = csv_path.replace('.csv', '.html')

    # Salva o novo HTML
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_completo)

# Exemplo de uso
gerar_html('3do-iso.csv', 'template.html', '3DO Interactive Multiplayer')  # Ajuste o caminho do CSV e do template conforme necessário
print('HTML gerado com sucesso!')
