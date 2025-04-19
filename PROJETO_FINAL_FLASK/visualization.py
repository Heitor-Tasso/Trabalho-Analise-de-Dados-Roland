import pandas as pd
import numpy as np
import json
from collections import Counter
import re
import logging
import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Helper function to clean text (for word clouds and text analysis)
def clean_text(text):
    """Clean text for word cloud and analysis"""
    if not isinstance(text, str):
        return ""
    
    # Remove special characters and extra spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower()

# Helper function to standardize values in a Series
def standardize_series(series):
    """
    Standardize values in a pandas Series - ensure they're strings and properly formatted
    """
    if series.dtype == 'object':
        return series.astype(str).str.strip()
    return series

# Função para criar gráfico de barras com Highcharts
def create_bar_chart(df, column, title, color_seq='Viridis', horizontal=True):
    """
    Creates a bar chart configuration for Highcharts
    
    Args:
        df (pd.DataFrame): DataFrame with data
        column (str): Name of column to analyze
        title (str): Chart title
        color_seq (str): Color sequence (not directly used in Highcharts but kept for compatibility)
        horizontal (bool): If True, creates a horizontal bar chart
    
    Returns:
        dict: Highcharts configuration
    """
    try:
        if column not in df.columns:
            logger.warning(f"Column {column} not found in DataFrame")
            return None
        
        # Make sure we're working with clean data
        df_clean = df.copy()
        df_clean[column] = standardize_series(df_clean[column])
        
        # Count unique values in the column
        value_counts = df_clean[column].value_counts().reset_index()
        value_counts.columns = [column, 'Contagem']
        
        # Log for debugging
        logger.debug(f"Values for {column}: {value_counts.to_dict()}")
        
        # Sort by count (descending)
        value_counts = value_counts.sort_values('Contagem', ascending=False)
        
        # Convert data to lists for Highcharts
        categories = value_counts[column].tolist()
        series_data = value_counts['Contagem'].tolist()
        
        # Garantir que não temos categorias undefined ou null
        valid_categories = []
        valid_data = []
        
        for i, category in enumerate(categories):
            if category and str(category).lower() not in ['undefined', 'null', 'nan', '']:
                valid_categories.append(category)
                valid_data.append(series_data[i])
        
        # Se não sobrou nenhuma categoria válida, retornar None
        if not valid_categories:
            logger.warning(f"No valid categories found for column {column}")
            return None
        
        # Atualizar as listas
        categories = valid_categories
        series_data = valid_data
        
        # Para gráficos horizontais, preparamos dados com legendas individuais
        if horizontal:
            # Criar array de objetos para usar como series.data com legendas individuais
            data_points = []
            
            for i, (category, value) in enumerate(zip(categories, series_data)):
                # Cada ponto terá seu próprio nome e configuração para legenda
                data_points.append({
                    'name': str(category),        # Nome na legenda
                    'y': value,                   # Valor numérico
                    'showInLegend': True,         # Mostrar na legenda
                    'legendIndex': i,             # Ordem na legenda
                    'events': {
                        'legendItemClick': """
                            function() {
                                const visible = this.visible !== false;
                                this.setVisible(!visible);
                                return false;  // Prevenir comportamento padrão
                            }
                        """
                    }
                })
            
            # Configuração para gráfico de barras horizontal
            config = {
                'chart': {
                    'type': 'bar',                # Tipo 'bar' para barras horizontais
                    'height': 400
                    # 'marginLeft': 180             # Margin esquerda ampla para acomodar a legenda
                },
                'title': {
                    'text': title
                },
                'xAxis': {
                    'min': 0,
                    'title': {
                        'text': 'Contagem'
                    }
                },
                'yAxis': {
                    'type': 'category',           # Tipo categoria para o eixo Y
                    'title': {
                        'text': None
                    },
                    'labels': {
                        'style': {
                            'fontSize': '12px',
                            'fontWeight': 'normal'
                        }
                    },
                    'categories': [p['name'] for p in data_points]  # Explicitamente definir categorias
                },
                'legend': {
                    'enabled': True,
                    'align': 'left',
                    'verticalAlign': 'middle',
                    'layout': 'vertical',
                    'x': -60,                    # Deslocar mais à esquerda para evitar sobreposição
                    'y': 30,
                    'width': 90,                 # Largura fixa para evitar texto cortado
                    'title': {
                        'text': column            # Usar o nome da coluna como título da legenda
                    },
                    'backgroundColor': 'rgba(255, 255, 255, 0.95)',
                    'shadow': True,
                    'itemMarginTop': 5,           # Espaçamento entre itens da legenda
                    'itemMarginBottom': 5,
                    'padding': 8,
                    'itemStyle': {
                        'textOverflow': 'ellipsis',
                        'overflow': 'hidden',
                        'width': '120px'
                    }
                },
                'plotOptions': {
                    'bar': {
                        'dataLabels': {
                            'enabled': True,
                            'format': '{y}'
                        },
                        'colorByPoint': True,     # Cada barra com cor diferente
                        'groupPadding': 0.1,
                        'pointPadding': 0.1,
                        'borderWidth': 0
                    },
                    'series': {
                        'showInLegend': False,    # A série não aparece na legenda, somente os pontos
                        'events': {
                            'legendItemClick': """
                                function(e) {
                                    e.preventDefault();
                                    return false;  // Prevenir comportamento padrão
                                }
                            """
                        }
                    }
                },
                'series': [{
                    'name': 'Contagem',
                    'data': data_points,          # Usar os objetos preparados com eventos próprios
                    'showInLegend': False         # A série não deve aparecer na legenda
                }],
                'tooltip': {
                    'pointFormat': '{point.y}'
                },
                'credits': {
                    'enabled': False
                }
            }
        else:
            # Para gráficos de colunas verticais, mesma abordagem com legendas individuais
            data_points = []
            
            for i, (category, value) in enumerate(zip(categories, series_data)):
                data_points.append({
                    'name': str(category),
                    'y': value,
                    'showInLegend': True,
                    'legendIndex': i,
                    'events': {
                        'legendItemClick': """
                            function() {
                                const visible = this.visible !== false;
                                this.setVisible(!visible);
                                return false;
                            }
                        """
                    }
                })
            
            # Configuração para gráfico de colunas vertical
            config = {
                'chart': {
                    'type': 'column',
                    'height': 400
                    # 'marginLeft': 160              # Ainda precisamos de margem para a legenda
                },
                'title': {
                    'text': title
                },
                'xAxis': {
                    'type': 'category',            # Tipo categoria também para o eixo X
                    'categories': [p['name'] for p in data_points],
                    'title': {
                        'text': None
                    }
                },
                'yAxis': {
                    'title': {
                        'text': 'Contagem'
                    },
                    'min': 0
                },
                'legend': {
                    'enabled': True,
                    'align': 'left',
                    'verticalAlign': 'middle',
                    'layout': 'vertical',
                    'x': -60,
                    'y': 30,
                    'width': 90,
                    'title': {
                        'text': column
                    },
                    'backgroundColor': 'rgba(255, 255, 255, 0.95)',
                    'shadow': True,
                    'itemMarginTop': 5,
                    'itemMarginBottom': 5,
                    'padding': 8
                },
                'plotOptions': {
                    'column': {
                        'dataLabels': {
                            'enabled': True
                        },
                        'colorByPoint': True
                    },
                    'series': {
                        'showInLegend': False,
                        'events': {
                            'legendItemClick': """
                                function(e) {
                                    e.preventDefault();
                                    return false;
                                }
                            """
                        }
                    }
                },
                'series': [{
                    'name': 'Contagem',
                    'data': data_points,
                    'showInLegend': False
                }],
                'credits': {
                    'enabled': False
                },
                'tooltip': {
                    'pointFormat': '<b>{point.y}</b>'
                }
            }
        
        return config
    except Exception as e:
        logger.error(f"Error creating bar chart for {column}: {str(e)}")
        return None
    

# Função para criar gráfico de pizza
def create_pie_chart(df, column, title):
    """
    Creates a pie chart configuration for Highcharts
    
    Args:
        df (pd.DataFrame): DataFrame with data
        column (str): Name of column to analyze
        title (str): Chart title
    
    Returns:
        dict: Highcharts configuration
    """
    try:
        if column not in df.columns:
            logger.warning(f"Column {column} not found in DataFrame")
            return None
        
        # Make sure we're working with clean data
        df_clean = df.copy()
        df_clean[column] = standardize_series(df_clean[column])
        
        # Count values
        value_counts = df_clean[column].value_counts()
        
        # Prepare data for Highcharts
        data = []
        for name, count in value_counts.items():
            data.append({
                'name': str(name),
                'y': int(count)
            })
        
        # Create Highcharts configuration
        config = {
            'chart': {
                'type': 'pie',
                'height': 400
            },
            'title': {
                'text': title
            },
            'tooltip': {
                'pointFormat': '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            'accessibility': {
                'point': {
                    'valueSuffix': '%'
                }
            },
            'plotOptions': {
                'pie': {
                    'allowPointSelect': True,
                    'cursor': 'pointer',
                    'dataLabels': {
                        'enabled': True,
                        'format': '<b>{point.name}</b>: {point.percentage:.1f} %'
                    }
                }
            },
            'series': [{
                'name': column,
                'colorByPoint': True,
                'data': data
            }],
            'credits': {
                'enabled': False
            }
        }
        
        return config
    except Exception as e:
        logger.error(f"Error creating pie chart for {column}: {str(e)}")
        return None

# Função para criar histograma de idade
def create_age_histogram(df, birth_date_column, title):
    """
    Creates a histogram configuration for Highcharts based on age data
    
    Args:
        df (pd.DataFrame): DataFrame with data
        birth_date_column (str): Name of column with birth date
        title (str): Chart title
    
    Returns:
        dict: Highcharts configuration
    """
    try:
        if birth_date_column not in df.columns:
            logger.warning(f"Column {birth_date_column} not found in DataFrame")
            return None
        
        # Check if we already have a calculated age column
        idade_col = f"Idade ({birth_date_column})"
        
        if idade_col in df.columns:
            # Use already calculated age column
            idade_data = df[idade_col].dropna()
        else:
            # Convert birth date column to datetime
            df[birth_date_column] = pd.to_datetime(df[birth_date_column], errors='coerce')
            
            # Calculate age
            today = pd.Timestamp.now()
            idade_data = df[birth_date_column].apply(
                lambda x: (today - x).days // 365 if pd.notnull(x) else np.nan
            ).dropna()
        
        # Convert to list for histogram binning
        ages = idade_data.tolist()
        
        # Calculate histogram bins
        min_age = int(min(ages)) if ages else 0
        max_age = int(max(ages)) if ages else 100
        
        # Create histogram data
        hist_data = np.histogram(ages, bins=range(min_age, max_age + 5, 5))
        categories = [f"{i}-{i+4}" for i in range(min_age, max_age + 1, 5)]
        counts = hist_data[0].tolist()
        
        # Create Highcharts configuration
        config = {
            'chart': {
                'type': 'column',
                'height': 400
            },
            'title': {
                'text': title
            },
            'xAxis': {
                'categories': categories,
                'title': {
                    'text': 'Idade (anos)'
                }
            },
            'yAxis': {
                'title': {
                    'text': 'Contagem'
                }
            },
            'plotOptions': {
                'column': {
                    'colorByPoint': False,
                    'color': '#4285F4'  # Google blue color
                }
            },
            'series': [{
                'name': 'Estudantes',
                'data': counts
            }],
            'tooltip': {
                'headerFormat': '<span style="font-size:10px">{point.key}</span><table>',
                'pointFormat': '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                               '<td style="padding:0"><b>{point.y}</b></td></tr>',
                'footerFormat': '</table>',
                'shared': True,
                'useHTML': True
            },
            'credits': {
                'enabled': False
            }
        }
        
        return config
    except Exception as e:
        logger.error(f"Error creating age histogram for {birth_date_column}: {str(e)}")
        return None

# Função para criar gráfico de top N itens
def create_top_n_chart(df, column, n=15, title=None, color='darkblue'):
    """
    Creates a bar chart configuration for Highcharts showing top N items
    
    Args:
        df (pd.DataFrame): DataFrame with data
        column (str): Name of column to analyze
        n (int): Number of items to show
        title (str): Chart title (optional)
        color (str): Bar color (mapped to Highcharts color)
    
    Returns:
        dict: Highcharts configuration
    """
    try:
        if column not in df.columns:
            logger.warning(f"Column {column} not found in DataFrame")
            return None
        
        # Define title if not provided
        if title is None:
            title = f"Top {n} - {column}"
        
        # Make sure we're working with clean data
        df_clean = df.copy()
        df_clean[column] = standardize_series(df_clean[column])
        
        # Count values and get top N
        logger.info(f"Column '{column}' data type: {df_clean[column].dtype}")
        logger.info(f"Column '{column}' first few values: {df_clean[column].head().tolist()}")
        
        value_counts = df_clean[column].value_counts().head(n)
        
        # Debug info
        logger.info(f"Top values for '{column}': {value_counts.to_dict()}")
        
        # Prepare data for Highcharts
        categories = value_counts.index.tolist()
        data = value_counts.values.tolist()
        
        # Create Highcharts configuration
        config = {
            'chart': {
                'type': 'column',
                'height': 500
            },
            'title': {
                'text': title
            },
            'xAxis': {
                'categories': categories,
                'labels': {
                    'rotation': -45,
                    'style': {
                        'fontSize': '11px'
                    }
                }
            },
            'yAxis': {
                'title': {
                    'text': 'Contagem'
                }
            },
            'legend': {
                'enabled': False
            },
            'plotOptions': {
                'column': {
                    'colorByPoint': False,
                    'color': '#0a58ca',  # Convert 'darkblue' to a web color
                    'dataLabels': {
                        'enabled': True,
                        'rotation': -90,
                        'color': '#FFFFFF',
                        'align': 'right',
                        'y': 10
                    }
                }
            },
            'series': [{
                'name': 'Contagem',
                'data': data
            }],
            'credits': {
                'enabled': False
            }
        }
        
        return config
    except Exception as e:
        logger.error(f"Error creating top_n chart for {column}: {str(e)}")
        return None

# Função para criar gráfico de barras empilhadas para itens de domicílio
def create_stacked_bar(df, item_columns, title):
    """
    Creates a stacked bar chart configuration for Highcharts
    
    Args:
        df (pd.DataFrame): DataFrame with data
        item_columns (list): List of columns with items
        title (str): Chart title
    
    Returns:
        dict: Highcharts configuration
    """
    try:
        # Check which columns exist in the DataFrame
        available_columns = [col for col in item_columns if col in df.columns]
        
        if not available_columns:
            logger.warning(f"None of the columns {item_columns} found in DataFrame")
            return None
        
        # Prepare data for visualization
        item_data = {}
        for col in available_columns:
            item_data[col] = df[col].value_counts()
        
        # Transform data to appropriate format
        item_df = pd.DataFrame(item_data)
        item_df = item_df.fillna(0).T  # Transpose to have items in rows
        
        # Prepare data for Highcharts
        categories = item_df.index.tolist()
        series = []
        
        for col in item_df.columns:
            series.append({
                'name': str(col),
                'data': item_df[col].tolist()
            })
        
        # Create a stacked bar chart configuration
        config = {
            'chart': {
                'type': 'column',
                'height': 600
            },
            'title': {
                'text': title
            },
            'xAxis': {
                'categories': categories,
                'title': {
                    'text': 'Item'
                }
            },
            'yAxis': {
                'min': 0,
                'title': {
                    'text': 'Contagem'
                },
                'stackLabels': {
                    'enabled': True,
                    'style': {
                        'fontWeight': 'bold',
                        'color': 'gray'
                    }
                }
            },
            'legend': {
                'align': 'right',
                'verticalAlign': 'top',
                'layout': 'vertical',
                'x': 0,
                'y': 100
            },
            'tooltip': {
                'headerFormat': '<b>{point.x}</b><br/>',
                'pointFormat': '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
            },
            'plotOptions': {
                'column': {
                    'stacking': 'normal',
                    'dataLabels': {
                        'enabled': True
                    }
                }
            },
            'series': series,
            'credits': {
                'enabled': False
            }
        }
        
        return config
    except Exception as e:
        logger.error(f"Error creating stacked bar chart: {str(e)}")
        return None

# Função para criar mapa do Brasil com estados coloridos
def create_choropleth_map(df, estado_column, title):
    """
    Creates a map of Brazil with states colored by frequency for Highcharts
    
    Args:
        df (pd.DataFrame): DataFrame with data
        estado_column (str): Name of column with states
        title (str): Chart title
    
    Returns:
        dict: Highcharts configuration
    """
    try:
        if estado_column not in df.columns:
            logger.warning(f"Column {estado_column} not found in DataFrame")
            return None
        
        # Mapping of state names to ISO codes
        estado_to_iso = {
            'São Paulo': 'BR-SP', 'Acre': 'BR-AC', 'Alagoas': 'BR-AL', 'Amapá': 'BR-AP',
            'Amazonas': 'BR-AM', 'Bahia': 'BR-BA', 'Ceará': 'BR-CE', 'Distrito Federal': 'BR-DF',
            'Espírito Santo': 'BR-ES', 'Goiás': 'BR-GO', 'Maranhão': 'BR-MA', 'Mato Grosso': 'BR-MT',
            'Mato Grosso do Sul': 'BR-MS', 'Minas Gerais': 'BR-MG', 'Paraná': 'BR-PR',
            'Paraíba': 'BR-PB', 'Pará': 'BR-PA', 'Pernambuco': 'BR-PE', 'Piauí': 'BR-PI',
            'Rio de Janeiro': 'BR-RJ', 'Rio Grande do Norte': 'BR-RN', 'Rio Grande do Sul': 'BR-RS',
            'Rondônia': 'BR-RO', 'Roraima': 'BR-RR', 'Santa Catarina': 'BR-SC', 'Sergipe': 'BR-SE',
            'Tocantins': 'BR-TO',
            # Adding abbreviation versions
            'SP': 'BR-SP', 'AC': 'BR-AC', 'AL': 'BR-AL', 'AP': 'BR-AP',
            'AM': 'BR-AM', 'BA': 'BR-BA', 'CE': 'BR-CE', 'DF': 'BR-DF',
            'ES': 'BR-ES', 'GO': 'BR-GO', 'MA': 'BR-MA', 'MT': 'BR-MT',
            'MS': 'BR-MS', 'MG': 'BR-MG', 'PR': 'BR-PR',
            'PB': 'BR-PB', 'PA': 'BR-PA', 'PE': 'BR-PE', 'PI': 'BR-PI',
            'RJ': 'BR-RJ', 'RN': 'BR-RN', 'RS': 'BR-RS',
            'RO': 'BR-RO', 'RR': 'BR-RR', 'SC': 'BR-SC', 'SE': 'BR-SE',
            'TO': 'BR-TO'
        }
        
        # Filter and process state data
        estados_count = df[estado_column].value_counts()
        
        # Prepare data for Highcharts
        data = []
        for estado, count in estados_count.items():
            iso_code = estado_to_iso.get(estado)
            if iso_code:
                # Use only the state code without 'BR-' prefix for Highcharts
                state_code = iso_code.replace('BR-', '')
                data.append([state_code, int(count)])
        
        # Create map configuration for Highcharts
        config = {
            'chart': {
                'map': 'countries/br/br-all',
                'height': 600
            },
            'title': {
                'text': title
            },
            'mapNavigation': {
                'enabled': True,
                'buttonOptions': {
                    'verticalAlign': 'bottom'
                }
            },
            'colorAxis': {
                'min': 0,
                'minColor': '#E6E7E8',
                'maxColor': '#005645'
            },
            'series': [{
                'data': data,
                'name': 'Quantidade',
                'states': {
                    'hover': {
                        'color': '#a4edba'
                    }
                },
                'dataLabels': {
                    'enabled': True,
                    'format': '{point.name}'
                }
            }],
            'credits': {
                'enabled': False
            }
        }
        
        return config
    except Exception as e:
        logger.error(f"Error creating choropleth map for {estado_column}: {str(e)}")
        return None

# Função para criar gráfico de comparação (ex: escolaridade dos pais)
def create_comparison_bar(df, columns_dict, group_by, title, colors=None):
    """
    Creates a comparison bar chart for Highcharts
    
    Args:
        df (pd.DataFrame): DataFrame with data
        columns_dict (dict): Dictionary with columns and their labels
        group_by (str): Name of column to group by (will appear on X axis)
        title (str): Chart title
        colors (list): List of colors for series
    
    Returns:
        dict: Highcharts configuration
    """
    try:
        # Check which columns exist in the DataFrame
        available_columns = {col: label for col, label in columns_dict.items() if col in df.columns}
        
        if not available_columns:
            logger.warning(f"None of the columns {columns_dict.keys()} found in DataFrame")
            return None
        
        # Prepare data for visualization
        categories = set()
        series_data = {}
        
        for col, label in available_columns.items():
            counts = df[col].value_counts()
            series_data[label] = counts
            categories.update(counts.index)
        
        # Ensure consistent categories across series
        categories = sorted(list(categories))
        
        # Create series for Highcharts
        series = []
        for label, counts in series_data.items():
            data = [counts.get(cat, 0) for cat in categories]
            series.append({
                'name': label,
                'data': data
            })
        
        # Default colors if not provided
        if not colors or len(colors) < len(series):
            colors = ['#7cb5ec', '#434348', '#90ed7d', '#f7a35c', '#8085e9',
                     '#f15c80', '#e4d354', '#2b908f', '#f45b5b', '#91e8e1']
        
        # Create Highcharts configuration
        config = {
            'chart': {
                'type': 'column',
                'height': 600
            },
            'title': {
                'text': title
            },
            'xAxis': {
                'categories': categories,
                'title': {
                    'text': group_by
                }
            },
            'yAxis': {
                'title': {
                    'text': 'Contagem'
                }
            },
            'plotOptions': {
                'column': {
                    'pointPadding': 0.2,
                    'borderWidth': 0
                }
            },
            'series': series,
            'colors': colors[:len(series)],
            'credits': {
                'enabled': False
            }
        }
        
        return config
    except Exception as e:
        logger.error(f"Error creating comparison bar chart: {str(e)}")
        return None

# Functions to generate charts for each section
def generate_visao_geral_charts(df):
    """
    Generate charts for the 'Visão Geral' section
    
    Args:
        df (pd.DataFrame): DataFrame with data
    
    Returns:
        dict: Dictionary with generated charts configurations
    """
    charts = {}
    
    # Chart of distribution by course
    charts['curso'] = create_bar_chart(
        df, 'Qual o seu curso?', 'Distribuição por Curso'
    )
    
    # Chart of distribution by period
    periodo_col = 'Qual o período que cursa?*' if 'Qual o período que cursa?*' in df.columns else 'Qual o período que cursa?'
    charts['periodo'] = create_pie_chart(
        df, periodo_col, 'Distribuição por Período'
    )
    
    # Chart of distribution by gender
    charts['genero'] = create_bar_chart(
        df, 'Qual é o seu gênero?', 'Distribuição por Gênero'
    )
    
    # Age histogram
    data_nasc_col = 'Qual a sua data de nascimento?' if 'Qual a sua data de nascimento?' in df.columns else None
    if data_nasc_col:
        charts['idade'] = create_age_histogram(
            df, data_nasc_col, 'Distribuição de Idade'
        )
    
    # Map of students by birth state
    estado_col = 'Qual o estado você nasceu?*' if 'Qual o estado você nasceu?*' in df.columns else 'Qual o estado você nasceu?'
    # if estado_col in df.columns:
    #     charts['mapa_estados'] = create_choropleth_map(
    #         df, estado_col, 'Distribuição por Estado de Nascimento'
    #     )
    
    return charts

def generate_perfil_estudantes_charts(df):
    """
    Generate charts for the 'Perfil dos Estudantes' section
    
    Args:
        df (pd.DataFrame): DataFrame with data
    
    Returns:
        dict: Dictionary with generated charts configurations
    """
    charts = {}
    
    # Chart of marital status
    charts['estado_civil'] = create_bar_chart(
        df, 'Qual é o seu estado civil?', 'Estado Civil'
    )
    
    # Chart of number of children
    charts['filhos'] = create_bar_chart(
        df, 'Quantos filhos você tem?', 'Quantidade de Filhos'
    )
    
    # Chart of housing situation
    charts['moradia'] = create_bar_chart(
        df, 'Com quem você mora atualmente?', 'Situação de Moradia'
    )
    
    # Chart of housing type
    charts['tipo_domicilio'] = create_bar_chart(
        df, 'Qual é a situação do domicílio em que você reside?', 'Tipo de Domicílio'
    )
    
    # Chart of special needs
    if 'Você possui alguma necessidade especial?' in df.columns:
        charts['necessidades_especiais'] = create_pie_chart(
            df, 'Você possui alguma necessidade especial?', 'Necessidades Especiais'
        )
    
    # Chart of city of residence (top 15)
    if 'Em qual cidade você reside?' in df.columns:
        charts['cidades'] = create_top_n_chart(
            df, 'Em qual cidade você reside?', 15, 'Top 15 Cidades de Residência'
        )
    
    return charts

def generate_socioeconomico_charts(df):
    """
    Generate charts for the 'Informações Socioeconômicas' section
    
    Args:
        df (pd.DataFrame): DataFrame with data
    
    Returns:
        dict: Dictionary with generated charts configurations
    """
    charts = {}
    
    # Chart of income range
    charts['renda'] = create_bar_chart(
        df, 'Qual é a faixa de renda mensal da sua família?', 'Faixa de Renda Familiar'
    )
    
    # Chart of residence time
    charts['tempo_residencia'] = create_pie_chart(
        df, 'Há quanto tempo você mora neste domicílio?', 'Tempo de Residência'
    )
    
    # Chart of number of people in household
    if 'Quantas pessoas, incluindo você, moram no seu domicílio?' in df.columns:
        charts['pessoas_domicilio'] = create_bar_chart(
            df, 'Quantas pessoas, incluindo você, moram no seu domicílio?', 
            'Quantidade de Pessoas no Domicílio', horizontal=False
        )
    
    # Chart of items in household
    item_columns = [
        'Televisor', 'Vídeo cassete e(ou) DVD', 'Rádio', 'Automóvel', 'Motocicleta',
        'Máquina de lavar roupa e(ou) tanquinho', 'Geladeira', 'Celular e(ou) Smartphone',
        'Microcomputador de mesa/Desktop', 'Notebook'
    ]
    
    charts['itens_domicilio'] = create_stacked_bar(
        df, item_columns, 'Quantidade de Itens por Domicílio'
    )
    
    return charts

def generate_trabalho_formacao_charts(df):
    """
    Generate charts for the 'Formação e Trabalho' section
    
    Args:
        df (pd.DataFrame): DataFrame with data
    
    Returns:
        dict: Dictionary with generated charts configurations
    """
    charts = {}
    
    # Chart of work situation
    charts['trabalha'] = create_pie_chart(
        df, 'Você trabalha?', 'Situação de Trabalho'
    )
    
    # Chart of employment relationship
    charts['vinculo'] = create_bar_chart(
        df, 'Qual é seu vínculo com o emprego?', 'Vínculo Empregatício'
    )
    
    # Chart of work area
    charts['area_trabalho'] = create_bar_chart(
        df, 'Qual a área do seu trabalho?', 'Área de Trabalho'
    )
    
    # Chart of work regime
    charts['regime_trabalho'] = create_bar_chart(
        df, 'Qual é o seu regime de trabalho?', 'Regime de Trabalho'
    )
    
    # Chart of educational background
    charts['formacao_escolar'] = create_bar_chart(
        df, 'Na sua vida escolar, você estudou....', 'Formação Escolar'
    )
    
    # Chart of health insurance
    charts['plano_saude'] = create_bar_chart(
        df, 'Você tem plano de saúde privado?', 'Plano de Saúde'
    )
    
    # Chart of parents' education
    colunas_escolaridade = {
        'Qual é o grau de escolaridade da sua mãe?': 'Mãe',
        'Qual é o grau de escolaridade do seu pai?': 'Pai'
    }
    
    charts['escolaridade_pais'] = create_comparison_bar(
        df, colunas_escolaridade, 'Escolaridade', 
        'Comparação da Escolaridade entre Pai e Mãe',
        colors=['#ff6b6b', '#48dbfb']  # Custom colors for mother and father
    )
    
    # Chart of technical training
    if 'Você já fez algum curso técnico?' in df.columns:
        charts['curso_tecnico'] = create_bar_chart(
            df, 'Você já fez algum curso técnico?', 'Formação Técnica'
        )
    
    return charts

def generate_tecnologia_charts(df):
    """
    Generate charts for the 'Uso de Tecnologia' section
    
    Args:
        df (pd.DataFrame): DataFrame with data
    
    Returns:
        dict: Dictionary with generated charts configurations
    """
    charts = {}
    
    # Chart of computer knowledge
    charts['conhecimento_informatica'] = create_bar_chart(
        df, 'Como você classifica seu conhecimento em informática?', 
        'Nível de Conhecimento em Informática'
    )
    
    # Knowledge of specific applications - can't directly convert heatmaps to Highcharts
    # Create stacked column chart instead for app knowledge
    app_columns = [
        'Windowns', 'Linux', 'Editores de textos (word, writer, ...)',
        'Planilhas Eletrônicas (Excel, Cal, ...)', 'Apresentadores (PowerPoint, Impress, ...)',
        'Sistemas de Gestão Empresarial', 'Inglês'
    ]
    
    # For app knowledge, create a grouped bar chart
    available_apps = [col for col in app_columns if col in df.columns]
    if available_apps:
        # Prepare data
        levels = ['Nenhum', 'Pouco', 'Intermediário', 'Avançado']
        series_data = []
        
        for level in levels:
            data = []
            for app in available_apps:
                count = (df[app] == level).sum()
                data.append(count)
            
            series_data.append({
                'name': level,
                'data': data
            })
        
        charts['conhecimento_apps'] = {
            'chart': {
                'type': 'column',
                'height': 500
            },
            'title': {
                'text': 'Nível de Conhecimento em Aplicativos e Sistemas'
            },
            'xAxis': {
                'categories': available_apps,
                'labels': {
                    'rotation': -45
                }
            },
            'yAxis': {
                'min': 0,
                'title': {
                    'text': 'Número de Estudantes'
                }
            },
            'legend': {
                'align': 'right',
                'verticalAlign': 'top',
                'layout': 'vertical'
            },
            'tooltip': {
                'pointFormat': '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b><br/>',
                'shared': True
            },
            'plotOptions': {
                'column': {
                    'stacking': 'normal'
                }
            },
            'series': series_data,
            'credits': {
                'enabled': False
            }
        }
    
    # Chart of device usage by location (create a grouped bar chart)
    # Similar to what we did for app knowledge but with device and location data
    devices = {
        "Desktop": ['Em casa', 'No trabalho', 'Na escola', 'Em outros lugares'],
        "Notebook": ['Em casa2', 'No trabalho2', 'Na escola2', 'Em outros lugares2'],
        "Smartphone": ['Em casa3', 'No trabalho3', 'Na escola3', 'Em outros lugares3']
    }
    
    # Prepare device usage data
    all_device_data = []
    locations = ['Em casa', 'No trabalho', 'Na escola', 'Em outros lugares']
    
    for device, cols in devices.items():
        device_data = []
        
        for i, loc in enumerate(locations):
            col = cols[i] if i < len(cols) else None
            if col and col in df.columns:
                yes_count = (df[col] == 'Sim').sum()
                device_data.append(yes_count)
            else:
                device_data.append(0)
        
        all_device_data.append({
            'name': device,
            'data': device_data
        })
    
    if all_device_data:
        charts['uso_dispositivos'] = {
            'chart': {
                'type': 'column',
                'height': 400
            },
            'title': {
                'text': 'Uso de Dispositivos por Local'
            },
            'xAxis': {
                'categories': ['Em casa', 'No trabalho', 'Na escola', 'Em outros lugares']
            },
            'yAxis': {
                'min': 0,
                'title': {
                    'text': 'Número de Estudantes'
                }
            },
            'tooltip': {
                'pointFormat': '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b><br/>',
                'shared': True
            },
            'plotOptions': {
                'column': {
                    'pointPadding': 0.2,
                    'borderWidth': 0
                }
            },
            'series': all_device_data,
            'credits': {
                'enabled': False
            }
        }
    
    # Chart of language knowledge (similar approach to app knowledge)
    idioma_columns = [
        'Inglês', 'Espanhol', 'Outros Idiomas'
    ]
    
    available_idiomas = [col for col in idioma_columns if col in df.columns]
    if available_idiomas:
        # Prepare data for language knowledge
        levels = ['Praticamente nulo', 'Leio mas não escrevo e nem falo', 
                 'Leio e escrevo mas não falo', 'Leio, escrevo e falo razoavelmente',
                 'Leio, escrevo e falo bem']
        
        idioma_series = []
        
        for level in levels:
            data = []
            for idioma in available_idiomas:
                count = (df[idioma] == level).sum()
                data.append(count)
            
            idioma_series.append({
                'name': level,
                'data': data
            })
        
        charts['conhecimento_idiomas'] = {
            'chart': {
                'type': 'column',
                'height': 500
            },
            'title': {
                'text': 'Nível de Conhecimento em Idiomas'
            },
            'xAxis': {
                'categories': available_idiomas
            },
            'yAxis': {
                'min': 0,
                'title': {
                    'text': 'Número de Estudantes'
                },
                'stackLabels': {
                    'enabled': True,
                    'style': {
                        'fontWeight': 'bold',
                        'color': 'gray'
                    }
                }
            },
            'legend': {
                'align': 'right',
                'verticalAlign': 'top',
                'layout': 'vertical'
            },
            'tooltip': {
                'pointFormat': '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b><br/>',
                'shared': True
            },
            'plotOptions': {
                'column': {
                    'stacking': 'normal'
                }
            },
            'series': idioma_series,
            'credits': {
                'enabled': False
            }
        }
    
    return charts

def generate_interesses_habitos_charts(df):
    """
    Generate charts for the 'Interesses e Hábitos' section
    
    Args:
        df (pd.DataFrame): DataFrame with data
    
    Returns:
        dict: Dictionary with generated charts configurations
    """
    charts = {}
    
    # Chart of annual reading
    charts['livros_ano'] = create_bar_chart(
        df, 'Não considerando os livros acadêmicos, quantos livros você lê por ano (em média)?', 
        'Quantidade de Livros Lidos por Ano'
    )
    
    # Chart of literary genres
    charts['generos_literarios'] = create_bar_chart(
        df, 'Se você lê livros literários, qual(is) o(s) gênero(s) preferido(s)?', 
        'Gêneros Literários Preferidos'
    )
    
    # Information sources (convert heatmap to stacked column chart)
    info_columns = [
        'TV', 'Internet2', 'Revistas', 'Jornais', 'Rádio2', 'Redes Sociais', 'Conversas com Amigos'
    ]
    
    available_sources = [col for col in info_columns if col in df.columns]
    if available_sources:
        # Prepare data for information sources
        frequencies = ['Nunca', 'Pouco', 'Às vezes', 'Muito', 'Sempre']
        
        source_series = []
        
        for freq in frequencies:
            data = []
            for source in available_sources:
                count = (df[source] == freq).sum()
                data.append(count)
            
            source_series.append({
                'name': freq,
                'data': data
            })
        
        charts['fontes_informacao'] = {
            'chart': {
                'type': 'column',
                'height': 500
            },
            'title': {
                'text': 'Frequência de Uso de Fontes de Informação'
            },
            'xAxis': {
                'categories': available_sources,
                'labels': {
                    'rotation': -45
                }
            },
            'yAxis': {
                'min': 0,
                'title': {
                    'text': 'Número de Estudantes'
                }
            },
            'legend': {
                'align': 'right',
                'verticalAlign': 'top'
            },
            'tooltip': {
                'pointFormat': '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b><br/>',
                'shared': True
            },
            'plotOptions': {
                'column': {
                    'stacking': 'normal'
                }
            },
            'series': source_series,
            'credits': {
                'enabled': False
            }
        }
    
    # Chart of voluntary activities
    charts['voluntariado'] = create_pie_chart(
        df, 'Você dedica parte do seu tempo para atividades voluntárias?', 
        'Participação em Atividades Voluntárias'
    )
    
    # Chart of religion
    charts['religiao'] = create_bar_chart(
        df, 'Qual religião você professa?', 'Religião'
    )
    
    # Chart of cultural entertainment (column chart for multiple choice)
    if 'Quais fontes de entretenimento cultural você usa?' in df.columns:
        # For columns with multiple choices separated by commas
        entertainment_options = []
        
        for entry in df['Quais fontes de entretenimento cultural você usa?'].dropna():
            options = [option.strip() for option in str(entry).split(',')]
            entertainment_options.extend(options)
        
        # Count occurrences and get top values
        entertainment_counts = Counter(entertainment_options).most_common()
        
        # Prepare data for Highcharts
        categories = [item[0] for item in entertainment_counts]
        data = [item[1] for item in entertainment_counts]
        
        charts['entretenimento_cultural'] = {
            'chart': {
                'type': 'column',
                'height': 400
            },
            'title': {
                'text': 'Fontes de Entretenimento Cultural'
            },
            'xAxis': {
                'categories': categories,
                'title': {
                    'text': 'Entretenimento'
                }
            },
            'yAxis': {
                'title': {
                    'text': 'Contagem'
                }
            },
            'plotOptions': {
                'column': {
                    'colorByPoint': True
                }
            },
            'series': [{
                'name': 'Contagem',
                'data': data,
                'showInLegend': False
            }],
            'credits': {
                'enabled': False
            }
        }
    
    return charts

def generate_motivacoes_expectativas_charts(df):
    """
    Generate charts for the 'Motivações e Expectativas' section
    
    Args:
        df (pd.DataFrame): DataFrame with data
    
    Returns:
        dict: Dictionary with generated charts configurations
    """
    charts = {}
    
    # Chart of how they learned about FATEC
    col_conheceu = 'Estamos quase no fim! Como você ficou sabendo da FATEC Franca?'
    if col_conheceu in df.columns:
        charts['conheceu_fatec'] = create_bar_chart(
            df, col_conheceu, 'Como Conheceu a FATEC'
        )
    
    # Chart of reason for course choice
    charts['motivo_curso'] = create_bar_chart(
        df, 'Por que você escolheu este curso?', 'Motivo da Escolha do Curso'
    )
    
    # Chart of expectation regarding the course
    charts['expectativa_curso'] = create_bar_chart(
        df, 'Qual sua maior expectativa quanto ao curso?', 'Expectativa Quanto ao Curso'
    )
    
    # Chart of expectation after graduation
    charts['expectativa_formacao'] = create_bar_chart(
        df, 'Qual sua expectativa após se formar?', 'Expectativa Após Formação'
    )
    
    # Chart of whether they previously studied at FATEC
    charts['estudou_fatec'] = create_pie_chart(
        df, 'Você já estudou nesta instituição?', 'Estudou na FATEC Anteriormente'
    )
    
    # Chart of technical course
    charts['curso_tecnico'] = create_bar_chart(
        df, 'Você já fez algum curso técnico?', 'Curso Técnico'
    )
    
    # Chart of transportation mode
    charts['transporte'] = create_bar_chart(
        df, 'Qual meio de transporte você utiliza para ir à faculdade?', 'Meio de Transporte'
    )
    
    return charts

def generate_analise_texto_charts(df):
    """
    Generate charts for the 'Análise de Texto' section
    
    Args:
        df (pd.DataFrame): DataFrame with data
    
    Returns:
        dict: Dictionary with generated charts configurations and text samples
    """
    charts = {}
    texto_col = 'Escreva algumas linhas sobre sua história e seus sonhos de vida'
    
    if texto_col in df.columns:
        # Since we can't easily create a wordcloud with Highcharts,
        # we'll just provide text examples for this section
        respostas = df[df[texto_col].notna() & (df[texto_col] != '')][texto_col]
        if not respostas.empty:
            # Select up to 5 random responses
            amostra = respostas.sample(min(5, len(respostas))).tolist()
            charts['respostas'] = amostra
            
            # If we want to add a simple word frequency chart
            # Get all words from all responses
            all_words = []
            for response in respostas:
                words = clean_text(response).split()
                # Filter out short words (less than 3 characters)
                words = [word for word in words if len(word) > 3]
                all_words.extend(words)
            
            # Count word frequencies
            word_counts = Counter(all_words).most_common(20)
            
            # Only create chart if we have words
            if word_counts:
                # Prepare data for Highcharts
                word_categories = [word[0] for word in word_counts]
                word_freqs = [word[1] for word in word_counts]
                
                charts['freq_palavras'] = {
                    'chart': {
                        'type': 'column',
                        'height': 400
                    },
                    'title': {
                        'text': 'Palavras Mais Frequentes'
                    },
                    'xAxis': {
                        'categories': word_categories,
                        'title': {
                            'text': 'Palavras'
                        },
                        'labels': {
                            'rotation': -45
                        }
                    },
                    'yAxis': {
                        'title': {
                            'text': 'Frequência'
                        }
                    },
                    'plotOptions': {
                        'column': {
                            'colorByPoint': True,
                            'dataLabels': {
                                'enabled': True
                            }
                        }
                    },
                    'series': [{
                        'name': 'Frequência',
                        'data': word_freqs,
                        'showInLegend': False
                    }],
                    'credits': {
                        'enabled': False
                    }
                }
    
    return charts
