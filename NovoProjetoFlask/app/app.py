# Exemplo de como modificar process_excel_file em data_processing.py para usar o novo sistema

from utils.data_standardizer import DataStandardizer
import pandas as pd
import json
import os
import logging

logger = logging.getLogger(__name__)

def process_excel_file(uploaded_file):
    """
    Process the uploaded Excel file and create the necessary files
    """
    try:
        logger.info(f"Processing file: {uploaded_file}")
        
        # Read the Excel file
        excel_data = pd.read_excel(uploaded_file, dtype=str)
        
        # Usar a nova classe de padronização
        standardizer = DataStandardizer()
        excel_data = standardizer.standardize_dataframe(excel_data)
        
        # Convert to list of dictionaries (original structure)
        json_data = excel_data.to_dict(orient='records')
        
        # Extract column names
        columns = list(excel_data.columns)
        
        # Create necessary directories
        os.makedirs('./database', exist_ok=True)
        
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
    