import pandas as pd
import json

nome_excel = "Questionario-Socioeconomico-Fatec25-OFICIAL-1a32"
# Carregar o arquivo Excel
excel_file = pd.read_excel(f'./arquivos_de_trabalho/{nome_excel}.xlsx', sheet_name='Sheet1', dtype=str)

# Converter para lista de dicionários (estrutura original)
json_data = excel_file.to_dict(orient='records')

# Salvar em um arquivo JSON
with open(f'./{nome_excel}.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=4)

print("Conversão concluída! Verifique o arquivo 'dados_formatados.json'.")
