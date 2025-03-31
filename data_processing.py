import pandas as pd
import json
import os

def load_data():
    # Carregar nomes das colunas do CSV
    cols = pd.read_csv('./database/colunas.csv').columns.tolist()
    
    # Carregar dados do JSON
    with open('./database/dados.json', 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    # Construir o DataFrame
    data = []
    for id_item, valores in json_data.items():
        if len(valores) == len(cols[1:]):  # Verificar consistência de dados
            row = {cols[0]: int(id_item)}
            row.update(zip(cols[1:], valores))
            data.append(row)
    
    df = pd.DataFrame(data)
    
    # Ordenar colunas conforme o CSV original
    df = df[cols]
    
    # Converter tipos de dados específicos
    date_cols = [col for col in df.columns if 'data' in col.lower()]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    
    return df
