# services/chart_generator.py
import logging
import pandas as pd

logger = logging.getLogger(__name__)

class BarChartGenerator:
    """Classe para geração de gráficos de barras com Highcharts"""
    
    def __init__(self, df=None):
        self.df = df
    
    def set_dataframe(self, df):
        """Define o DataFrame a ser usado"""
        self.df = df
    
    def generate(self, column, title, horizontal=True):
        """Gera configuração de gráfico de barras para Highcharts"""
        try:
            if column not in self.df.columns:
                logger.warning(f"Coluna {column} não encontrada no DataFrame")
                return None
            
            # Limpar e padronizar dados
            df_clean = self.df.copy()
            
            # Garantir que estamos trabalhando com strings limpas
            if df_clean[column].dtype == 'object':
                df_clean[column] = df_clean[column].astype(str).str.strip()
            
            # Contar valores únicos na coluna
            value_counts = df_clean[column].value_counts().reset_index()
            value_counts.columns = [column, 'Contagem']
            
            # Ordenar por contagem (decrescente)
            value_counts = value_counts.sort_values('Contagem', ascending=False)
            
            # Filtrar valores inválidos
            valid_mask = ~value_counts[column].isin(['undefined', 'null', 'nan', ''])
            value_counts = value_counts[valid_mask]
            
            if value_counts.empty:
                logger.warning(f"Nenhum valor válido encontrado para {column}")
                return None
            
            # Extrair categorias e contagens como listas
            categories = value_counts[column].tolist()
            counts = value_counts['Contagem'].tolist()
            
            # Criar data points com legendas individuais
            data_points = []
            for i, (category, value) in enumerate(zip(categories, counts)):
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
            
            # Criar configuração base para o gráfico
            config = {
                'chart': {
                    'type': 'bar' if horizontal else 'column',
                    'height': 400,
                    'marginLeft': 180 if horizontal else 40
                },
                'title': {
                    'text': title
                },
                'xAxis': {
                    'min': 0 if horizontal else None,
                    'title': {
                        'text': 'Contagem' if horizontal else None
                    },
                    'type': None if horizontal else 'category',
                    'categories': None if horizontal else [p['name'] for p in data_points]
                },
                'yAxis': {
                    'type': 'category' if horizontal else None,
                    'title': {
                        'text': None if horizontal else 'Contagem'
                    },
                    'labels': {
                        'style': {
                            'fontSize': '12px',
                            'fontWeight': 'normal'
                        }
                    },
                    'categories': [p['name'] for p in data_points] if horizontal else None
                },
                'legend': {
                    'enabled': True,
                    'align': 'left',
                    'verticalAlign': 'middle',
                    'layout': 'vertical',
                    'x': -160,
                    'y': 0,
                    'width': 140,
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
                    },
                    'bar' if horizontal else 'column': {
                        'dataLabels': {
                            'enabled': True,
                            'format': '{y}'
                        },
                        'colorByPoint': True,
                        'groupPadding': 0.1,
                        'pointPadding': 0.1,
                        'borderWidth': 0
                    }
                },
                'series': [{
                    'name': 'Contagem',
                    'data': data_points,
                    'showInLegend': False
                }],
                'tooltip': {
                    'pointFormat': '{point.y}'
                },
                'credits': {
                    'enabled': False
                }
            }
            
            return config
            
        except Exception as e:
            logger.error(f"Erro ao criar gráfico de barras para {column}: {str(e)}")
            return None
        