import pandas as pd
import numpy as np
import json
import streamlit as st
import io
import datetime
import os

# Função para criar diretórios necessários caso não existam
def create_directories():
    os.makedirs('./database', exist_ok=True)

# Função para processar o arquivo Excel enviado
def process_excel_file(uploaded_file):
    """
    Processa o arquivo Excel enviado e cria os arquivos necessários
    """
    try:
        # Lê o arquivo Excel
        excel_data = pd.read_excel(uploaded_file, dtype=str)
        
        # Converte para lista de dicionários (estrutura original)
        json_data = excel_data.to_dict(orient='records')
        
        # Extrair os nomes das colunas
        columns = list(excel_data.columns)
        
        # Criar o arquivo CSV com os cabeçalhos
        create_directories()
        pd.DataFrame(columns=columns).to_csv('./database/colunas.csv', index=False, encoding='utf-8')
        
        # Cria o dicionário onde a chave é o ID e o valor é a lista de dados na ordem das colunas
        resultado_json = {}
        for item in json_data:
            id_item = str(item.get('ID', ''))
            if id_item:  # Só adiciona se tiver um ID válido
                # Garantir que todos os campos estejam presentes e na ordem correta
                dados = [item.get(coluna, '') for coluna in columns[1:]]
                resultado_json[id_item] = dados
        
        # Salvar o resultado em um arquivo JSON
        with open('./database/dados.json', 'w', encoding='utf-8') as json_file:
            json.dump(resultado_json, json_file, ensure_ascii=False, indent=4)
        
        return True, "Arquivo processado com sucesso!"
    except Exception as e:
        return False, f"Erro ao processar o arquivo: {str(e)}"

@st.cache_data
def load_data():
    """
    Carrega os dados processados dos arquivos CSV e JSON
    """
    try:
        # Carregar nomes das colunas do CSV
        cols = pd.read_csv('./database/colunas.csv').columns.tolist()
        
        # Carregar dados do JSON
        with open('./database/dados.json', 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        # Construir o DataFrame
        data = []
        for id_item, valores in json_data.items():
            if len(valores) == len(cols[1:]):  # Verificar consistência de dados
                row = {cols[0]: id_item}
                for i, col in enumerate(cols[1:]):
                    row[col] = valores[i]
                data.append(row)
        
        df = pd.DataFrame(data)
        
        # Ordenar colunas conforme o CSV original
        df = df[cols]
        
        # Converter tipos de dados específicos
        date_cols = [col for col in df.columns if 'data' in col.lower()]
        for col in date_cols:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Calcular idades para colunas de data de nascimento
        for col in date_cols:
            if 'nascimento' in col.lower():
                df[f'Idade ({col})'] = df[col].apply(
                    lambda x: (datetime.datetime.now() - x).days // 365 if pd.notnull(x) else np.nan
                )
        
        return df.set_index("ID")
    
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()

# Função para verificar se os dados estão prontos
def check_data_ready():
    """
    Verifica se os arquivos de dados necessários existem
    """
    return os.path.exists('./database/colunas.csv') and os.path.exists('./database/dados.json')
