import streamlit as st
from graficos import *
from data_processing import load_data

def generate_visao_geral(df):
    """
    Gera os gráficos da seção Visão Geral
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
    
    Returns:
        dict: Dicionário com os gráficos gerados
    """
    graficos = {}
    
    # Gráfico de distribuição por curso
    graficos['curso'] = create_bar_chart(
        df, 'Qual o seu curso?', 'Distribuição por Curso'
    )
    
    # Gráfico de distribuição por período
    periodo_col = 'Qual o período que cursa?*' if 'Qual o período que cursa?*' in df.columns else 'Qual o período que cursa?'
    graficos['periodo'] = create_pie_chart(
        df, periodo_col, 'Distribuição por Período'
    )
    
    # Gráfico de distribuição por gênero
    graficos['genero'] = create_bar_chart(
        df, 'Qual é o seu gênero?', 'Distribuição por Gênero'
    )
    
    # Histograma de idade
    data_nasc_col = 'Qual a sua data de nascimento?' if 'Qual a sua data de nascimento?' in df.columns else None
    if data_nasc_col:
        graficos['idade'] = create_age_histogram(
            df, data_nasc_col, 'Distribuição de Idade'
        )
    
    # Mapa dos estudantes por estado de nascimento
    estado_col = 'Qual o estado você nasceu?*' if 'Qual o estado você nasceu?*' in df.columns else 'Qual o estado você nasceu?'
    if estado_col in df.columns:
        graficos['mapa_estados'] = create_choropleth_map(
            df, estado_col, 'Distribuição por Estado de Nascimento'
        )
    
    return graficos

def generate_perfil_estudantes(df):
    """
    Gera os gráficos da seção Perfil dos Estudantes
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
    
    Returns:
        dict: Dicionário com os gráficos gerados
    """
    graficos = {}
    
    # Gráfico de estado civil
    graficos['estado_civil'] = create_bar_chart(
        df, 'Qual é o seu estado civil?', 'Estado Civil'
    )
    
    # Gráfico de quantidade de filhos
    graficos['filhos'] = create_bar_chart(
        df, 'Quantos filhos você tem?', 'Quantidade de Filhos'
    )
    
    # Gráfico de situação de moradia
    graficos['moradia'] = create_bar_chart(
        df, 'Com quem você mora atualmente?', 'Situação de Moradia'
    )
    
    # Gráfico de tipo de domicílio
    graficos['tipo_domicilio'] = create_bar_chart(
        df, 'Qual é a situação do domicílio em que você reside?', 'Tipo de Domicílio'
    )
    
    # Gráfico de necessidades especiais
    if 'Você possui alguma necessidade especial?' in df.columns:
        graficos['necessidades_especiais'] = create_pie_chart(
            df, 'Você possui alguma necessidade especial?', 'Necessidades Especiais'
        )
    
    # Gráfico de cidade de residência (top 15)
    if 'Em qual cidade você reside?' in df.columns:
        graficos['cidades'] = create_top_n_chart(
            df, 'Em qual cidade você reside?', 15, 'Top 15 Cidades de Residência'
        )
    
    return graficos

def generate_socioeconomico(df):
    """
    Gera os gráficos da seção Informações Socioeconômicas
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
    
    Returns:
        dict: Dicionário com os gráficos gerados
    """
    graficos = {}
    
    # Gráfico de faixa de renda
    graficos['renda'] = create_bar_chart(
        df, 'Qual é a faixa de renda mensal da sua família?', 'Faixa de Renda Familiar'
    )
    
    # Gráfico de tempo de residência
    graficos['tempo_residencia'] = create_pie_chart(
        df, 'Há quanto tempo você mora neste domicílio?', 'Tempo de Residência'
    )
    
    # Gráfico de quantidade de pessoas no domicílio
    if 'Quantas pessoas, incluindo você, moram no seu domicílio?' in df.columns:
        graficos['pessoas_domicilio'] = create_bar_chart(
            df, 'Quantas pessoas, incluindo você, moram no seu domicílio?', 
            'Quantidade de Pessoas no Domicílio', horizontal=False
        )
    
    # Gráfico de itens no domicílio
    item_columns = [
        'Televisor', 'Vídeo cassete e(ou) DVD', 'Rádio', 'Automóvel', 'Motocicleta',
        'Máquina de lavar roupa e(ou) tanquinho', 'Geladeira', 'Celular e(ou) Smartphone',
        'Microcomputador de mesa/Desktop', 'Notebook'
    ]
    
    graficos['itens_domicilio'] = create_stacked_bar(
        df, item_columns, 'Quantidade de Itens por Domicílio'
    )
    
    # Gráfico de serviços no domicílio
    service_columns = [
        'Telefone fixo', 'Internet', 'TV por assinatura e(ou) Serviços de Streaming',
        'Empregada mensalista'
    ]
    
    # Prepara os dados para visualização
    service_data = {}
    for col in service_columns:
        if col in df.columns:
            service_data[col] = df[col].value_counts(normalize=True) * 100
    
    if service_data:
        service_df = pd.DataFrame(service_data).fillna(0)
        
        # Cria o gráfico
        fig = px.bar(
            service_df.T,
            labels={'index': 'Serviço', 'value': 'Percentual (%)'},
            title="Percentual de Domicílios com Serviços",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        
        graficos['servicos_domicilio'] = fig
    
    return graficos

def generate_trabalho_formacao(df):
    """
    Gera os gráficos da seção Formação e Trabalho
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
    
    Returns:
        dict: Dicionário com os gráficos gerados
    """
    graficos = {}
    
    # Gráfico de situação de trabalho
    graficos['trabalha'] = create_pie_chart(
        df, 'Você trabalha?', 'Situação de Trabalho'
    )
    
    # Gráfico de vínculo empregatício
    graficos['vinculo'] = create_bar_chart(
        df, 'Qual é seu vínculo com o emprego?', 'Vínculo Empregatício'
    )
    
    # Gráfico de área de trabalho
    graficos['area_trabalho'] = create_bar_chart(
        df, 'Qual a área do seu trabalho?', 'Área de Trabalho'
    )
    
    # Gráfico de regime de trabalho
    graficos['regime_trabalho'] = create_bar_chart(
        df, 'Qual é o seu regime de trabalho?', 'Regime de Trabalho'
    )
    
    # Gráfico de formação escolar
    graficos['formacao_escolar'] = create_bar_chart(
        df, 'Na sua vida escolar, você estudou....', 'Formação Escolar'
    )
    
    # Gráfico de plano de saúde
    graficos['plano_saude'] = create_bar_chart(
        df, 'Você tem plano de saúde privado?', 'Plano de Saúde'
    )
    
    # Gráfico de escolaridade dos pais
    colunas_escolaridade = {
        'Qual é o grau de escolaridade da sua mãe?': 'Mãe',
        'Qual é o grau de escolaridade do seu pai?': 'Pai'
    }
    
    graficos['escolaridade_pais'] = create_comparison_bar(
        df, colunas_escolaridade, 'Escolaridade', 
        'Comparação da Escolaridade entre Pai e Mãe',
        colors=['#ff6b6b', '#48dbfb']
    )
    
    # Gráfico de formação técnica
    if 'Você já fez algum curso técnico?' in df.columns:
        graficos['curso_tecnico'] = create_bar_chart(
            df, 'Você já fez algum curso técnico?', 'Formação Técnica'
        )
    
    return graficos

def generate_tecnologia(df):
    """
    Gera os gráficos da seção Uso de Tecnologia
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
    
    Returns:
        dict: Dicionário com os gráficos gerados
    """
    graficos = {}
    
    # Gráfico de conhecimento em informática
    graficos['conhecimento_informatica'] = create_bar_chart(
        df, 'Como você classifica seu conhecimento em informática?', 
        'Nível de Conhecimento em Informática'
    )
    
    # Gráfico de conhecimento em aplicativos específicos
    app_columns = [
        'Windowns', 'Linux', 'Editores de textos (word, writer, ...)',
        'Planilhas Eletrônicas (Excel, Cal, ...)', 'Apresentadores (PowerPoint, Impress, ...)',
        'Sistemas de Gestão Empresarial', 'Inglês'
    ]
    
    graficos['conhecimento_apps'] = create_heatmap(
        df, app_columns, 'Nível de Conhecimento em Aplicativos e Sistemas'
    )
    
    # Gráfico de dispositivos - uso por local
    devices = {
        "Desktop": ['Em casa', 'No trabalho', 'Na escola', 'Em outros lugares'],
        "Notebook": ['Em casa2', 'No trabalho2', 'Na escola2', 'Em outros lugares2'],
        "Smartphone": ['Em casa3', 'No trabalho3', 'Na escola3', 'Em outros lugares3']
    }
    
    # Prepara os dados para gráfico de uso de dispositivos
    all_device_data = []
    
    for device, locations in devices.items():
        for loc in locations:
            if loc in df.columns:
                # Limpa o nome do local (remove números)
                location_name = ''.join([c for c in loc if not c.isdigit()])
                yes_count = df[loc].value_counts().get('Sim', 0)
                total = len(df)
                percentage = (yes_count / total) * 100 if total > 0 else 0
                
                all_device_data.append({
                    'Dispositivo': device,
                    'Local': location_name,
                    'Percentual': percentage
                })
    
    if all_device_data:
        device_df = pd.DataFrame(all_device_data)
        
        # Cria o gráfico
        fig = px.bar(
            device_df,
            x='Local',
            y='Percentual',
            color='Dispositivo',
            barmode='group',
            title='Uso de Dispositivos por Local (%)',
            labels={'Percentual': 'Percentual de Uso (%)'}
        )
        
        graficos['uso_dispositivos'] = fig
    
    # Gráfico de finalidade de uso dos dispositivos
    purposes = [
        "Para trabalhos profissionais", "Para trabalhos escolares",
        "Para entretenimento (música, redes sociais,...)", "Para comunicação por e-mail",
        "Para operações bancárias", "Para compras eletrônicas"
    ]
    
    # Números para diferentes dispositivos
    device_suffixes = {'': 'Desktop', '2': 'Notebook', '3': 'Smartphone'}
    
    # Prepara os dados
    purpose_data = []
    
    for purpose in purposes:
        for suffix, device_name in device_suffixes.items():
            col_name = f"{purpose}{suffix}"
            if col_name in df.columns:
                yes_count = df[col_name].value_counts().get('Sim', 0)
                total = len(df)
                percentage = (yes_count / total) * 100 if total > 0 else 0
                
                purpose_data.append({
                    'Dispositivo': device_name,
                    'Finalidade': purpose,
                    'Percentual': percentage
                })
    
    if purpose_data:
        purpose_df = pd.DataFrame(purpose_data)
        
        # Cria o gráfico
        fig = px.bar(
            purpose_df,
            x='Finalidade',
            y='Percentual',
            color='Dispositivo',
            barmode='group',
            title='Finalidade de Uso por Tipo de Dispositivo (%)',
            labels={'Percentual': 'Percentual de Uso (%)'}
        )
        
        # Ajusta o layout para melhor visualização
        fig.update_layout(
            xaxis={'categoryorder': 'total descending'},
            height=600
        )
        
        graficos['finalidade_uso'] = fig
    
    # Conhecimento de idiomas
    idioma_columns = [
        'Inglês', 'Espanhol', 'Outros Idiomas'
    ]
    
    graficos['conhecimento_idiomas'] = create_heatmap(
        df, idioma_columns, 'Nível de Conhecimento em Idiomas'
    )
    
    return graficos

def generate_interesses_habitos(df):
    """
    Gera os gráficos da seção Interesses e Hábitos
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
    
    Returns:
        dict: Dicionário com os gráficos gerados
    """
    graficos = {}
    
    # Gráfico de leitura anual
    graficos['livros_ano'] = create_bar_chart(
        df, 'Não considerando os livros acadêmicos, quantos livros você lê por ano (em média)?', 
        'Quantidade de Livros Lidos por Ano'
    )
    
    # Gráfico de gêneros literários
    graficos['generos_literarios'] = create_bar_chart(
        df, 'Se você lê livros literários, qual(is) o(s) gênero(s) preferido(s)?', 
        'Gêneros Literários Preferidos'
    )
    
    # Gráfico de fontes de informação
    info_columns = [
        'TV', 'Internet2', 'Revistas', 'Jornais', 'Rádio2', 'Redes Sociais', 'Conversas com Amigos'
    ]
    
    graficos['fontes_informacao'] = create_heatmap(
        df, info_columns, 'Frequência de Uso de Fontes de Informação'
    )
    
    # Gráfico de atividades voluntárias
    graficos['voluntariado'] = create_pie_chart(
        df, 'Você dedica parte do seu tempo para atividades voluntárias?', 
        'Participação em Atividades Voluntárias'
    )
    
    # Gráfico de religião
    graficos['religiao'] = create_bar_chart(
        df, 'Qual religião você professa?', 'Religião'
    )
    
    # Gráfico de entretenimento cultural
    if 'Quais fontes de entretenimento cultural você usa?' in df.columns:
        # Para colunas com múltiplas escolhas separadas por vírgulas
        entertainment_options = []
        
        for entry in df['Quais fontes de entretenimento cultural você usa?'].dropna():
            options = [option.strip() for option in str(entry).split(',')]
            entertainment_options.extend(options)
        
        # Conta as ocorrências
        entertainment_counts = Counter(entertainment_options)
        
        # Cria o gráfico
        fig = px.bar(
            x=list(entertainment_counts.keys()),
            y=list(entertainment_counts.values()),
            title="Fontes de Entretenimento Cultural",
            labels={'x': 'Entretenimento', 'y': 'Contagem'},
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        
        graficos['entretenimento_cultural'] = fig
    
    return graficos

def generate_motivacoes_expectativas(df):
    """
    Gera os gráficos da seção Motivações e Expectativas
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
    
    Returns:
        dict: Dicionário com os gráficos gerados
    """
    graficos = {}
    
    # Gráfico de como conheceu a FATEC
    col_conheceu = 'Estamos quase no fim! Como você ficou sabendo da FATEC Franca?'
    if col_conheceu in df.columns:
        graficos['conheceu_fatec'] = create_bar_chart(
            df, col_conheceu, 'Como Conheceu a FATEC'
        )
    
    # Gráfico de motivo da escolha do curso
    graficos['motivo_curso'] = create_bar_chart(
        df, 'Por que você escolheu este curso?', 'Motivo da Escolha do Curso'
    )
    
    # Gráfico de expectativa quanto ao curso
    graficos['expectativa_curso'] = create_bar_chart(
        df, 'Qual sua maior expectativa quanto ao curso?', 'Expectativa Quanto ao Curso'
    )
    
    # Gráfico de expectativa após formação
    graficos['expectativa_formacao'] = create_bar_chart(
        df, 'Qual sua expectativa após se formar?', 'Expectativa Após Formação'
    )
    
    # Gráfico de estudou na FATEC anteriormente
    graficos['estudou_fatec'] = create_pie_chart(
        df, 'Você já estudou nesta instituição?', 'Estudou na FATEC Anteriormente'
    )
    
    # Gráfico de curso técnico
    graficos['curso_tecnico'] = create_bar_chart(
        df, 'Você já fez algum curso técnico?', 'Curso Técnico'
    )
    
    # Gráfico de meio de transporte
    graficos['transporte'] = create_bar_chart(
        df, 'Qual meio de transporte você utiliza para ir à faculdade?', 'Meio de Transporte'
    )
    
    return graficos

def generate_analise_texto(df):
    """
    Gera os gráficos da seção Análise de Texto
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
    
    Returns:
        dict: Dicionário com os gráficos gerados
    """
    graficos = {}
    
    # Coluna de texto sobre história e sonhos
    texto_col = 'Escreva algumas linhas sobre sua história e seus sonhos de vida'
    
    if texto_col in df.columns:
        # Nuvem de palavras
        graficos['nuvem_sonhos'] = create_wordcloud(
            df, texto_col, 'Nuvem de Palavras - Sonhos e Histórias'
        )
        
        # Frequência de palavras
        graficos['freq_palavras'] = create_word_frequency(
            df, texto_col, 20, 'Palavras Mais Frequentes'
        )
    
    return graficos