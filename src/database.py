import sqlite3
import pandas as pd
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def salvar_no_banco(csv_path, db_path):
    logging.info("Iniciando carga no banco de dados...")
    
    # 1. Carregar dados processados
    if not os.path.exists(csv_path):
        logging.error(f"Arquivo processado não encontrado: {csv_path}")
        return
    
    df = pd.read_csv(csv_path)
    
    # 2. Conectar ao SQLite (Cria o arquivo se não existir)
    conn = sqlite3.connect(db_path)
    
    # 3. Salvar os dados (Replace substitui a tabela se ela já existir)
    try:
        df.to_sql('monitor_precos', conn, if_exists='replace', index=False)
        logging.info(f"Sucesso! {len(df)} linhas inseridas no banco: {db_path}")
    except Exception as e:
        logging.error(f"Erro ao salvar no banco: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    PATH_PROCESSED = "data/processed/cleaned_books.csv"
    PATH_DB = "data/database_monitor.db" # O banco ficará na pasta data
    
    salvar_no_banco(PATH_PROCESSED, PATH_DB)