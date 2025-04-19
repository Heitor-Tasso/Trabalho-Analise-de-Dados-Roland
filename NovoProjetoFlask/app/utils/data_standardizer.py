# utils/data_standardizer.py
import re
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class DataStandardizer:
    """Classe para padronização de dados do questionário socioeconômico"""
    
    def __init__(self):
        # Mapeamentos para cidades
        self.city_mapping = {
            'FRANCA': 'Franca',
            'franca': 'Franca',
            'RIBEIRAO PRETO': 'Ribeirão Preto',
            'RIBEIRAO': 'Ribeirão Preto',
            'Ribeirao Preto': 'Ribeirão Preto',
            'ribeirao preto': 'Ribeirão Preto',
            'Ribeirão': 'Ribeirão Preto',
            'BATATAIS': 'Batatais',
            'batatais': 'Batatais'
        }
        
        # Mapeamentos para cursos
        self.course_mapping = {
            'ADS': 'Análise e Desenvolvimento de Sistemas',
            'ANALISE E DESENVOLVIMENTO DE SISTEMAS': 'Análise e Desenvolvimento de Sistemas',
            'DESENVOLVIMENTO DE SOFTWARE MULTIPLATAFORMA': 'Desenvolvimento de Software Multiplataforma',
            'DSM': 'Desenvolvimento de Software Multiplataforma',
            'GESTÃO DE PRODUÇÃO INDUSTRIAL': 'Gestão de Produção Industrial',
            'GPI': 'Gestão de Produção Industrial',
            'GESTÃO EMPRESARIAL': 'Gestão Empresarial',
            'GESTÃO DE RECURSOS HUMANOS': 'Gestão de Recursos Humanos',
            'GESTÃO RH': 'Gestão de Recursos Humanos'
        }
        
        # Mapeamentos para períodos
        self.period_mapping = {
            'MATUTINO': 'Matutino',
            'NOTURNO': 'Noturno',
            'Ead': 'EAD',
            'ead': 'EAD'
        }
        
        # Palavras que devem permanecer em minúsculas em nomes de cidades
        self.lowercase_words = ['de', 'da', 'do', 'das', 'dos', 'e']
    
    def standardize_city(self, city_name):
        """Padroniza nome de cidade com capitalização e tratamento de acentos apropriados"""
        if not isinstance(city_name, str) or city_name == '':
            return city_name
        
        # Verificar no mapeamento direto primeiro
        if city_name.upper() in self.city_mapping:
            return self.city_mapping[city_name.upper()]
        
        # Limpar e padronizar
        clean_name = re.sub(r'[^\w\s]', '', city_name).strip()
        words = clean_name.split()
        
        if not words:
            return city_name
        
        # Aplicar regras de capitalização
        result = []
        for i, word in enumerate(words):
            if word.lower() in self.lowercase_words and i > 0:
                result.append(word.lower())
            else:
                result.append(word.capitalize())
        
        return ' '.join(result)
    
    def standardize_course(self, course_name):
        """Padroniza nome de curso"""
        if not isinstance(course_name, str):
            return course_name
        
        course_name = course_name.strip()
        
        # Verificar no mapeamento
        if course_name.upper() in self.course_mapping:
            return self.course_mapping[course_name.upper()]
        
        # Caso não esteja no mapeamento, aplicar title case
        return course_name.title()
    
    def standardize_period(self, period):
        """Padroniza período do curso"""
        if not isinstance(period, str):
            return period
        
        period = period.strip()
        
        # Verificar no mapeamento
        return self.period_mapping.get(period, period.title())
    
    def standardize_dataframe(self, df):
        """Padroniza todos os dados relevantes no DataFrame"""
        logger.info(f"Iniciando padronização do DataFrame com {len(df)} linhas")
        
        # Criar cópia para não modificar o original
        df_standardized = df.copy()
        
        # Padronizar cidades
        city_columns = ['Em qual cidade você reside?']
        for col in city_columns:
            if col in df_standardized.columns:
                df_standardized[col] = df_standardized[col].apply(self.standardize_city)
                unique_vals = df_standardized[col].unique()
                logger.info(f"Valores únicos para {col} após padronização: {unique_vals}")
        
        # Padronizar cursos
        course_columns = ['Qual o seu curso?']
        for col in course_columns:
            if col in df_standardized.columns:
                df_standardized[col] = df_standardized[col].apply(self.standardize_course)
        
        # Padronizar períodos
        period_columns = ['Qual o período que cursa?', 'Qual o período que cursa?*']
        for col in period_columns:
            if col in df_standardized.columns:
                df_standardized[col] = df_standardized[col].apply(self.standardize_period)
        
        return df_standardized
    