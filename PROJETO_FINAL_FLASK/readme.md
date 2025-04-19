# Análise Socioeconômica FATEC

Um aplicativo web Flask para análise de dados socioeconômicos dos estudantes da FATEC. Este projeto permite que professores e administradores façam upload de arquivos Excel contendo respostas de questionários socioeconômicos e visualizem dados através de gráficos interativos.

## Características

- Upload e processamento de arquivos Excel com dados de questionários
- Dashboard interativo com várias seções de visualização
- Gráficos gerados dinamicamente utilizando Highcharts.js
- Padronização de dados para garantir consistência
- Interface responsiva com Bootstrap 5
- Armazenamento temporário de dados processados

## Estrutura do Projeto

```
app/
├── app.py                         # Configuração principal do Flask e rotas
├── config.py                      # Configurações da aplicação
├── data_processing.py             # Funções de processamento e padronização de dados
├── visualization.py               # Funções para geração de gráficos e visualizações
├── static/                        # Arquivos estáticos
│   ├── css/                       # Estilos CSS
│   │   ├── style.css              # Template base
│   │   └── charts.css             # Página de erro 500
│   ├── js/                        # Scripts JavaScript
│   │   ├── main.js                # Template base
│   │   └── chat-standardizer.js   # Página de erro 500
│   └── img/                       # Imagens
├── templates/                     # Templates HTML
│   ├── base.html                  # Template base
│   ├── upload.html                # Página de upload
│   ├── dashboard.html             # Dashboard principal
│   ├── 404.html                   # Página de erro 404
│   └── 500.html                   # Página de erro 500
├── database/                      # Diretório para armazenamento temporário
└── uploads/                       # Diretório para arquivos enviados

```
