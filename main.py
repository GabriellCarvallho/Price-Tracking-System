import os
import logging
from dotenv import load_dotenv
from src.extraction import extrair_dados_livros
from src.transformation import transformar_dados
from src.database import salvar_no_banco

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run():
    url = os.getenv("URL_BOOKS")
    path_raw = os.getenv("PATH_RAW")
    path_processed = os.getenv("PATH_PROCESSED")
    path_db = os.getenv("PATH_DB")

    logging.info("Iniciando Pipeline...")

    df = extrair_dados_livros(url)
    if df is not None and not df.empty:
        df.to_csv(path_raw, index=False)
        
        transformar_dados(path_raw, path_processed)
        
        salvar_no_banco(path_processed, path_db)
        
        logging.info("Pipeline executado com sucesso!")
    else:
        logging.error("Falha na coleta de dados.")

if __name__ == "__main__":
    run()