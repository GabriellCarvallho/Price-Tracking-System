import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def extrair_dados_livros(url):
    print(f"Iniciando coleta em: {url}")
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Erro ao acessar site: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    livros = soup.find_all('article', class_='product_pod')
    
    lista_dados = []
    for livro in livros:
        titulo = livro.h3.a['title']
        # Buscamos o preço
        preco_texto = livro.find('p', class_='price_color').text
        
        # LIMPEZA: Remove o símbolo da moeda e qualquer caractere estranho
        # O replace('Â', '') ajuda se houver erro de encoding (os caracteres estranhos que apareceram no seu log)
        preco_limpo = preco_texto.replace('£', '').replace('Â', '').strip()
        
        try:
            lista_dados.append({"titulo": titulo, "preco": float(preco_limpo)})
        except ValueError:
            print(f"Erro ao converter preço do livro: {titulo}")
            continue # Pula para o próximo livro se este der erro
        df_resultado = pd.DataFrame(lista_dados)
        print(f"Total de livros coletados: {len(df_resultado)}")
    return df_resultado

if __name__ == "__main__":
    URL = "http://books.toscrape.com/index.html"
    df = extrair_dados_livros(URL)
    
    if df is not None:
        # Garante que a pasta data existe
        os.makedirs('data', exist_ok=True)
        df.to_csv('data/raw_books.csv', index=False)
        print("Dados salvos com sucesso em data/raw_books.csv")
        print(df.head())