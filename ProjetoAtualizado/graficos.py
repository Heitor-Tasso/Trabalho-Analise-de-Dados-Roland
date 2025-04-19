import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import datetime

# Função para criar gráfico de barras com Plotly
def create_bar_chart(df, column, title, color_seq='Viridis', horizontal=True, height=400, width=600):
    """
    Cria um gráfico de barras para a coluna especificada
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
        column (str): Nome da coluna a ser analisada
        title (str): Título do gráfico
        color_seq (str): Sequência de cores do Plotly
        horizontal (bool): Se True, cria gráfico de barras horizontal
        height (int): Altura do gráfico
        width (int): Largura do gráfico
    
    Returns:
        fig: Figura do Plotly
    """
    if column not in df.columns:
        return None
        
    # Conta os valores únicos na coluna
    value_counts = df[column].value_counts().reset_index()
    value_counts.columns = [column, 'Contagem']
    
    # Ordena por contagem (decrescente)
    value_counts = value_counts.sort_values('Contagem', ascending=False)
    
    # Cria o gráfico
    if horizontal:
        fig = px.bar(
            value_counts, 
            y=column, 
            x='Contagem',
            title=title,
            color='Contagem',
            color_continuous_scale=color_seq,
            orientation='h'
        )
        
        fig.update_layout(
            xaxis_title="Contagem",
            yaxis_title="",
            height=height,
            width=width
        )
    else:
        fig = px.bar(
            value_counts, 
            x=column, 
            y='Contagem',
            title=title,
            color='Contagem',
            color_continuous_scale=color_seq
        )
        
        fig.update_layout(
            xaxis_title="",
            yaxis_title="Contagem",
            height=height,
            width=width
        )
    
    return fig

# Função para criar gráfico de pizza
def create_pie_chart(df, column, title, height=400, width=500):
    """
    Cria um gráfico de pizza para a coluna especificada
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
        column (str): Nome da coluna a ser analisada
        title (str): Título do gráfico
        height (int): Altura do gráfico
        width (int): Largura do gráfico
    
    Returns:
        fig: Figura do Plotly
    """
    if column not in df.columns:
        return None
        
    value_counts = df[column].value_counts()
    
    fig = px.pie(
        names=value_counts.index,
        values=value_counts.values,
        title=title
    )
    
    fig.update_layout(
        height=height,
        width=width
    )
    
    return fig

# Função para criar histograma de idade
def create_age_histogram(df, birth_date_column, title, height=400, width=600):
    """
    Cria um histograma das idades calculadas a partir da data de nascimento
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
        birth_date_column (str): Nome da coluna com a data de nascimento
        title (str): Título do gráfico
        height (int): Altura do gráfico
        width (int): Largura do gráfico
    
    Returns:
        fig: Figura do Plotly
    """
    if birth_date_column not in df.columns:
        return None
        
    # Verificar se já temos uma coluna de idade calculada
    idade_col = f"Idade ({birth_date_column})"
    
    if idade_col in df.columns:
        # Usar a coluna de idade já calculada
        idade_data = df[idade_col].dropna()
    else:
        # Converter coluna de data de nascimento para datetime
        df[birth_date_column] = pd.to_datetime(df[birth_date_column], errors='coerce')
        
        # Calcular idade
        today = datetime.datetime.now()
        idade_data = df[birth_date_column].apply(
            lambda x: (today - x).days // 365 if pd.notnull(x) else np.nan
        ).dropna()
    
    # Criar histograma
    fig = px.histogram(
        x=idade_data,
        title=title,
        labels={'x': 'Idade (anos)'},
        color_discrete_sequence=['darkblue']
    )
    
    fig.update_layout(
        xaxis_title="Idade (anos)",
        yaxis_title="Contagem",
        height=height,
        width=width
    )
    
    return fig

# Função para criar mapa de calor para perguntas com matriz
def create_heatmap(df, columns, title, figsize=(12, 8)):
    """
    Cria um mapa de calor para várias colunas relacionadas
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
        columns (list): Lista de colunas a serem analisadas
        title (str): Título do gráfico
        figsize (tuple): Tamanho da figura
    
    Returns:
        fig: Figura do Matplotlib
    """
    # Verificar quais colunas existem no DataFrame
    available_columns = [col for col in columns if col in df.columns]
    
    if not available_columns:
        return None
        
    # Processa os dados para o formato adequado
    data = {}
    for col in available_columns:
        data[col] = df[col].value_counts(normalize=True) * 100  # Percentual
    
    # Converte para DataFrame
    heatmap_df = pd.DataFrame(data).fillna(0)
    
    # Cria o mapa de calor
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(heatmap_df, annot=True, fmt='.1f', cmap='YlGnBu', ax=ax)
    plt.title(title)
    plt.tight_layout()
    
    return fig

# Função para criar nuvem de palavras
def create_wordcloud(df, text_column, title, width=800, height=400):
    """
    Cria uma nuvem de palavras a partir de um texto
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
        text_column (str): Nome da coluna com o texto
        title (str): Título do gráfico
        width (int): Largura da nuvem
        height (int): Altura da nuvem
    
    Returns:
        fig: Figura do Matplotlib
    """
    if text_column not in df.columns:
        return None
        
    # Concatena todos os textos da coluna
    all_text = ' '.join(df[text_column].dropna().astype(str))
    
    # Cria a nuvem de palavras
    wordcloud = WordCloud(
        width=width, 
        height=height, 
        background_color='white',
        max_words=150,
        contour_width=1,
        contour_color='steelblue'
    ).generate(all_text)
    
    # Plota a nuvem de palavras
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.set_title(title)
    ax.axis('off')
    
    return fig

# Função para criar um mapa do Brasil com estados coloridos
def create_choropleth_map(df, estado_column, title):
    """
    Cria um mapa do Brasil com estados coloridos pela frequência
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
        estado_column (str): Nome da coluna com os estados
        title (str): Título do gráfico
    
    Returns:
        fig: Figura do Plotly
    """
    if estado_column not in df.columns:
        return None
        
    # Mapeamento de nomes de estados para códigos ISO
    estado_to_iso = {
        'São Paulo': 'BR-SP', 'Acre': 'BR-AC', 'Alagoas': 'BR-AL', 'Amapá': 'BR-AP',
        'Amazonas': 'BR-AM', 'Bahia': 'BR-BA', 'Ceará': 'BR-CE', 'Distrito Federal': 'BR-DF',
        'Espírito Santo': 'BR-ES', 'Goiás': 'BR-GO', 'Maranhão': 'BR-MA', 'Mato Grosso': 'BR-MT',
        'Mato Grosso do Sul': 'BR-MS', 'Minas Gerais': 'BR-MG', 'Paraná': 'BR-PR',
        'Paraíba': 'BR-PB', 'Pará': 'BR-PA', 'Pernambuco': 'BR-PE', 'Piauí': 'BR-PI',
        'Rio de Janeiro': 'BR-RJ', 'Rio Grande do Norte': 'BR-RN', 'Rio Grande do Sul': 'BR-RS',
        'Rondônia': 'BR-RO', 'Roraima': 'BR-RR', 'Santa Catarina': 'BR-SC', 'Sergipe': 'BR-SE',
        'Tocantins': 'BR-TO',
        # Adicionando versões com siglas
        'SP': 'BR-SP', 'AC': 'BR-AC', 'AL': 'BR-AL', 'AP': 'BR-AP',
        'AM': 'BR-AM', 'BA': 'BR-BA', 'CE': 'BR-CE', 'DF': 'BR-DF',
        'ES': 'BR-ES', 'GO': 'BR-GO', 'MA': 'BR-MA', 'MT': 'BR-MT',
        'MS': 'BR-MS', 'MG': 'BR-MG', 'PR': 'BR-PR',
        'PB': 'BR-PB', 'PA': 'BR-PA', 'PE': 'BR-PE', 'PI': 'BR-PI',
        'RJ': 'BR-RJ', 'RN': 'BR-RN', 'RS': 'BR-RS',
        'RO': 'BR-RO', 'RR': 'BR-RR', 'SC': 'BR-SC', 'SE': 'BR-SE',
        'TO': 'BR-TO'
    }
    
    # Filtra e processa os dados dos estados
    estados_count = df[estado_column].value_counts().reset_index()
    estados_count.columns = ['Estado', 'Contagem']
    
    # Aplica o mapeamento para códigos ISO
    estados_count['ISO'] = estados_count['Estado'].map(estado_to_iso)
    
    # Remove estados sem correspondência ISO
    estados_count = estados_count.dropna(subset=['ISO'])
    
    # Cria o mapa
    fig = px.choropleth(
        estados_count,
        locations='ISO',
        color='Contagem',
        scope="south america",
        color_continuous_scale=px.colors.sequential.Viridis,
        title=title
    )
    
    fig.update_layout(
        geo=dict(
            showlakes=False,
            showcoastlines=True,
            projection_scale=3.5,
        ),
        height=600
    )
    
    return fig

# Função para criar gráficos de barras empilhadas para itens de domicílio
def create_stacked_bar(df, item_columns, title, height=600):
    """
    Cria um gráfico de barras empilhadas para itens de domicílio
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
        item_columns (list): Lista de colunas com os itens
        title (str): Título do gráfico
        height (int): Altura do gráfico
    
    Returns:
        fig: Figura do Plotly
    """
    # Verifica quais colunas existem no DataFrame
    available_columns = [col for col in item_columns if col in df.columns]
    
    if not available_columns:
        return None
        
    # Prepara os dados para visualização
    item_data = {}
    for col in available_columns:
        item_data[col] = df[col].value_counts()
    
    # Transforma os dados para o formato adequado
    item_df = pd.DataFrame(item_data)
    item_df = item_df.fillna(0).T  # Transpõe para ter itens nas linhas
    
    # Cria um gráfico de barras empilhadas
    fig = go.Figure()
    
    for col in item_df.columns:
        fig.add_trace(go.Bar(
            name=str(col),
            x=item_df.index,
            y=item_df[col],
            text=item_df[col]
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Item",
        yaxis_title="Contagem",
        barmode='stack',
        height=height
    )
    
    return fig

# Função para criar gráfico de barras para comparação (ex: escolaridade dos pais)
def create_comparison_bar(df, columns_dict, group_by, title, colors=None):
    """
    Cria um gráfico de barras para comparação entre grupos
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
        columns_dict (dict): Dicionário com as colunas e seus rótulos
        group_by (str): Nome da coluna para agrupar (aparecerá no eixo X)
        title (str): Título do gráfico
        colors (list): Lista de cores para as séries
    
    Returns:
        fig: Figura do Plotly
    """
    # Verifica quais colunas existem no DataFrame
    available_columns = {col: label for col, label in columns_dict.items() if col in df.columns}
    
    if not available_columns:
        return None
        
    # Prepara os dados para visualização
    all_data = []
    
    for col, label in available_columns.items():
        counts = df[col].value_counts().reset_index()
        counts.columns = [group_by, 'Contagem']
        counts['Categoria'] = label
        all_data.append(counts)
    
    # Combina todos os dados
    combined_df = pd.concat(all_data)
    
    # Cria o gráfico
    fig = px.bar(
        combined_df,
        x=group_by,
        y='Contagem',
        color='Categoria',
        barmode='group',
        title=title,
        color_discrete_sequence=colors
    )
    
    fig.update_layout(
        height=600
    )
    
    return fig


# Função para criar gráfico de top N itens
def create_top_n_chart(df, column, n=15, title=None, color='darkblue'):
    """
    Cria um gráfico de barras com os top N itens de uma coluna
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
        column (str): Nome da coluna a ser analisada
        n (int): Número de itens a mostrar
        title (str): Título do gráfico (opcional)
        color (str): Cor das barras
    
    Returns:
        fig: Figura do Plotly
    """
    if column not in df.columns:
        return None
        
    # Define o título se não for fornecido
    if title is None:
        title = f"Top {n} - {column}"
    
    # Conta os valores e pega os top N
    print("df[column] -=> ", df[column])
    counts = df[column].value_counts().head(n)
    print("counts -=> ", counts)
    
    
    fig = px.bar(
        x=counts.index,
        y=counts.values,
        title=title,
        labels={'x': column, 'y': 'Contagem'},
        color_discrete_sequence=[color]
    )
    
    # fig.update_layout(height=500)
    
    return fig

# Função para criar gráfico de frequência de palavras
def create_word_frequency(df, text_column, n=20, title=None, min_length=3):
    """
    Cria um gráfico de barras com as palavras mais frequentes
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
        text_column (str): Nome da coluna com o texto
        n (int): Número de palavras a mostrar
        title (str): Título do gráfico (opcional)
        min_length (int): Comprimento mínimo das palavras
    
    Returns:
        fig: Figura do Plotly
    """
    if text_column not in df.columns:
        return None
        
    # Define o título se não for fornecido
    if title is None:
        title = f"Palavras mais frequentes - {text_column}"
    
    # Concatena todos os textos da coluna
    all_text = ' '.join(df[text_column].dropna().astype(str))
    
    # Filtra palavras pelo comprimento
    words = [word.lower() for word in all_text.split() if len(word) > min_length]
    
    # Conta as palavras
    word_counts = Counter(words).most_common(n)
    
    fig = px.bar(
        x=[count[1] for count in word_counts],
        y=[count[0] for count in word_counts],
        orientation='h',
        labels={'x': 'Frequência', 'y': 'Palavra'},
        title=title,
        color_discrete_sequence=['darkblue']
    )
    
    fig.update_layout(height=600)
    
    return fig
