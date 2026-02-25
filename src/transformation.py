import pandas as pd
import os
from datetime import datetime
import logging

# Configuração de LOGS (Padrão profissional para rastrear erros)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def transformar_dados(input_path, output_path):
    logging.info("Iniciando a transformação dos dados...")
    
    # 1. Carregar os dados
    if not os.path.exists(input_path):
        logging.error(f"Arquivo não encontrado: {input_path}")
        return
    
    df = pd.read_csv(input_path)
    
    # 2. Transformação: Adicionar data de processamento
    df['data_processamento'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 3. Regra de Negócio: Converter preço para Real (simulando cotação de 6.0)
    cotacao_libra = 6.20 # Exemplo
    df['preco_brl'] = df['preco'] * cotacao_libra
    
    # 4. Criar pasta se não existir e salvar
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    logging.info(f"Dados transformados com sucesso e salvos em: {output_path}")
    print(df.head())

if __name__ == "__main__":
    PATH_RAW = "data/raw_books.csv"
    PATH_PROCESSED = "data/processed/cleaned_books.csv"
    
    transformar_dados(PATH_RAW, PATH_PROCESSED)