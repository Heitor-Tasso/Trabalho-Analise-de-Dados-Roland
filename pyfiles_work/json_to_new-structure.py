import json
import csv

# Carregar os dados do JSON
with open("./Questionario-Socioeconomico-Fatec25-OFICIAL-1a32.json", "r", encoding="utf-8") as file:
    json_data = json.load(file)

# Extrair os nomes das colunas a partir do primeiro item
if not json_data:
    columns = []
else:
    columns = list(json_data[0].keys())

# Criar o arquivo CSV com os cabeçalhos
with open('./database/colunas.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(columns)

# Criar o dicionário onde a chave é o ID e o valor é a lista de dados na ordem das colunas
resultado_json = {}
for item in json_data:
    id_item = item['ID']
    # Garantir que todos os campos estejam presentes e na ordem correta
    dados = [item.get(coluna, '') for coluna in columns]
    resultado_json[id_item] = dados[1::]

# Salvar o resultado em um arquivo JSON
with open('./database/dados.json', 'w', encoding='utf-8') as json_file:
    json.dump(resultado_json, json_file, ensure_ascii=False, indent=4)

print("Processo concluído! Arquivos 'colunas.csv' e 'dados.json' foram gerados.")
