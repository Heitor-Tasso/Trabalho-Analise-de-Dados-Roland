import pandas as pd
import numpy as np
import json
import io
import datetime
import os
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Função para criar diretórios necessários caso não existam
def create_directories():
    """Create necessary directories if they don't exist"""
    os.makedirs('./database', exist_ok=True)
    os.makedirs('./uploads', exist_ok=True)

# Função para padronizar valores
def standardize_values(df):
    """
    Standardize common fields to ensure consistent data.
    For example, 'Franca', 'FRANCA', 'franca' all become 'Franca'.
    """
    try:
        # Dictionary of columns to standardize and their standard values
        standardization_dict = {
            'Em qual cidade você reside?': {
                'FRANCA': 'Franca',
                'franca': 'Franca',
                'RIBEIRAO PRETO': 'Ribeirão Preto',
                'RIBEIRAO': 'Ribeirão Preto',
                'Ribeirao Preto': 'Ribeirão Preto',
                'ribeirao preto': 'Ribeirão Preto',
                'Ribeirão': 'Ribeirão Preto',
                'BATATAIS': 'Batatais',
                'batatais': 'Batatais'
            },
            'Qual o seu curso?': {
                'ADS': 'Análise e Desenvolvimento de Sistemas',
                'ANALISE E DESENVOLVIMENTO DE SISTEMAS': 'Análise e Desenvolvimento de Sistemas',
                'DESENVOLVIMENTO DE SOFTWARE MULTIPLATAFORMA': 'Desenvolvimento de Software Multiplataforma',
                'DSM': 'Desenvolvimento de Software Multiplataforma',
                'GESTÃO DE PRODUÇÃO INDUSTRIAL': 'Gestão de Produção Industrial',
                'GPI': 'Gestão de Produção Industrial',
                'GESTÃO EMPRESARIAL': 'Gestão Empresarial',
                'GESTÃO DE RECURSOS HUMANOS': 'Gestão de Recursos Humanos',
                'GESTÃO RH': 'Gestão de Recursos Humanos'
            },
            'Qual o período que cursa?': {
                'MATUTINO': 'Matutino',
                'NOTURNO': 'Noturno',
                'Ead': 'EAD',
                'ead': 'EAD'
            }
        }

        # Log the dataframe before standardization
        logger.info(f"DataFrame before standardization: {len(df)} rows")
        
        # Apply standardization to specified columns
        for col, standard_values in standardization_dict.items():
            if col in df.columns:
                # First, normalize by title case and remove excess whitespace
                df[col] = df[col].astype(str).str.strip().str.title()
                
                # Then apply specific standardization
                df[col] = df[col].replace(standard_values)
                
                # Log the unique values for debugging
                unique_vals = df[col].unique()
                logger.info(f"Unique values for {col} after standardization: {unique_vals}")
        
        # For columns with city names, apply a more general standardization
        city_columns = ['Em qual cidade você reside?']
        for col in city_columns:
            if col in df.columns:
                # General standardization for any city name
                df[col] = df[col].apply(lambda x: standardize_city_name(x) if pd.notnull(x) else x)
                
        # Log some stats after standardization
        if 'Em qual cidade você reside?' in df.columns:
            franca_count = (df['Em qual cidade você reside?'] == 'Franca').sum()
            logger.info(f"Count of 'Franca' after standardization: {franca_count}")
            
            # Get top cities for debugging
            top_cities = df['Em qual cidade você reside?'].value_counts().head(10)
            logger.info(f"Top cities: {top_cities.to_dict()}")
        
        return df
    
    except Exception as e:
        logger.error(f"Error in standardize_values: {str(e)}")
        raise

def standardize_city_name(city_name):
    """Standardize a city name with proper capitalization and accent handling"""
    if not isinstance(city_name, str) or city_name == '':
        return city_name
    
    # Remove excess whitespace and special characters
    clean_name = re.sub(r'[^\w\s]', '', city_name).strip()
    
    # Correct capitalization for city names
    words = clean_name.split()
    if not words:
        return city_name
    
    # Capitalize each word, except for prepositions, articles, etc.
    lowercase_words = ['de', 'da', 'do', 'das', 'dos', 'e']
    
    result = []
    for i, word in enumerate(words):
        if word.lower() in lowercase_words and i > 0:
            result.append(word.lower())
        else:
            result.append(word.capitalize())
    
    return ' '.join(result)

# Função para processar o arquivo Excel enviado
def process_excel_file(uploaded_file):
    """
    Process the uploaded Excel file and create the necessary files
    """
    try:
        logger.info(f"Processing file: {uploaded_file}")
        
        # Read the Excel file
        excel_data = pd.read_excel(uploaded_file, dtype=str)
        
        # Standardize common values
        excel_data = standardize_values(excel_data)
        
        # Convert to list of dictionaries (original structure)
        json_data = excel_data.to_dict(orient='records')
        
        # Extract column names
        columns = list(excel_data.columns)
        
        # Create necessary directories
        create_directories()
        
        # Create the CSV file with headers
        pd.DataFrame(columns=columns).to_csv('./database/colunas.csv', index=False, encoding='utf-8')
        
        # Create dictionary where the key is the ID and the value is the list of data in column order
        resultado_json = {}
        for item in json_data:
            id_item = str(item.get('ID', ''))
            if id_item:  # Only add if there's a valid ID
                # Ensure all fields are present and in the correct order
                dados = [item.get(coluna, '') for coluna in columns[1:]]
                resultado_json[id_item] = dados
        
        # Save the result in a JSON file
        with open('./database/dados.json', 'w', encoding='utf-8') as json_file:
            json.dump(resultado_json, json_file, ensure_ascii=False, indent=4)
        
        logger.info("File processed successfully")
        return True, "Arquivo processado com sucesso!"
    
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        return False, f"Erro ao processar o arquivo: {str(e)}"

def load_data():
    """
    Load processed data from CSV and JSON files
    """
    try:
        # Load column names from CSV
        cols = pd.read_csv('./database/colunas.csv').columns.tolist()
        
        # Load data from JSON
        with open('./database/dados.json', 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        # Build the DataFrame
        data = []
        for id_item, valores in json_data.items():
            if len(valores) == len(cols[1:]):  # Check data consistency
                row = {cols[0]: id_item}
                for i, col in enumerate(cols[1:]):
                    row[col] = valores[i]
                data.append(row)
        
        df = pd.DataFrame(data)
        
        # Sort columns according to the original CSV
        df = df[cols]
        
        # Convert specific data types
        date_cols = [col for col in df.columns if 'data' in col.lower()]
        for col in date_cols:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Calculate ages for birth date columns
        for col in date_cols:
            if 'nascimento' in col.lower():
                df[f'Idade ({col})'] = df[col].apply(
                    lambda x: (datetime.datetime.now() - x).days // 365 if pd.notnull(x) else np.nan
                )
        
        # Log some data stats for debugging
        logger.info(f"Loaded data with {len(df)} rows and {len(df.columns)} columns")
        
        # Apply standardization again to ensure consistency
        df = standardize_values(df)
        
        return df.set_index("ID") if "ID" in df.columns else df
    
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise

# Função para verificar se os dados estão prontos
def check_data_ready():
    """
    Check if the necessary data files exist
    """
    return os.path.exists('./database/colunas.csv') and os.path.exists('./database/dados.json')
