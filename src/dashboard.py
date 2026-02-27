import streamlit as st
import sqlite3
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="Monitor de Preços", layout="wide")



st.title("Monitor de preços - Visão Historica")
st.title("📊 Painel de Monitoramento de Preços")


st.markdown("Dados extraídos do site *Books to Scrape* via Pipeline ETL.")

# Conectar ao Banco de Dados
def carregar_dados():
    conn = sqlite3.connect('data/database_monitor.db')
    df = pd.read_sql_query("SELECT * FROM monitor_precos ORDER BY data_processamento ASC", conn)
    conn.close()
    return df

df = carregar_dados()


# KPIS iniciais

st.subheader("Resumo Atual")
col1, col2 = st.columns(2)
col1.metric("Total de registros no historico", len(df))
col2.metric("N* de livros únicos", len(df['titulo'].unique()))

st.divider()

# --- A MÁGICA: FILTRO DE EVOLUÇÃO ---
st.subheader("Análise de Evolução por Produto")
livro_escolhido = st.selectbox("Escolha um livro para ver a variação de preço:", df['titulo'].unique())

df_filtrado = df[df['titulo'] == livro_escolhido]

# Gráfico de Linha
st.line_chart(data=df_filtrado, x='data_processamento', y='preco_brl')

# Tabela do Histórico desse livro
st.write(f"Histórico de preços para: {livro_escolhido}")
st.dataframe(df_filtrado[['data_processamento', 'preco', 'preco_brl']])