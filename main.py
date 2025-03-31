import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from data_processing import load_data
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import datetime

# Configuração da página
st.set_page_config(
    page_title="Análise de Dados dos Estudantes FATEC",
    page_icon="📊",
    layout="wide"
)

# Função para criar gráfico de barras com Plotly
def create_bar_chart(df, column, title, color_seq='Viridis'):
    """Cria um gráfico de barras para a coluna especificada"""
    if df[column].dtype == 'object':
        # Conta os valores únicos na coluna
        value_counts = df[column].value_counts().reset_index()
        value_counts.columns = [column, 'Contagem']
        
        # Cria o gráfico
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
            height=400,
            width=600
        )
        
        return fig
    else:
        st.warning(f"A coluna {column} não é do tipo objeto.")
        return None

# Função para criar gráfico de pizza
def create_pie_chart(df, column, title):
    """Cria um gráfico de pizza para a coluna especificada"""
    value_counts = df[column].value_counts()
    
    fig = px.pie(
        names=value_counts.index,
        values=value_counts.values,
        title=title
    )
    
    fig.update_layout(
        height=400,
        width=500
    )
    
    return fig

# Função para criar histograma de idade
def create_age_histogram(df, birth_date_column, title):
    """Cria um histograma das idades calculadas a partir da data de nascimento"""
    # Converter coluna de data de nascimento para datetime
    df[birth_date_column] = pd.to_datetime(df[birth_date_column], errors='coerce')
    
    # Calcular idade
    today = datetime.datetime.now()
    df['Idade'] = df[birth_date_column].apply(
        lambda x: (today - x).days // 365 if pd.notnull(x) else np.nan
    )
    
    # Criar histograma
    fig = px.histogram(
        df.dropna(subset=['Idade']), 
        x='Idade',
        title=title,
        labels={'Idade': 'Idade (anos)'},
        color_discrete_sequence=['darkblue']
    )
    
    fig.update_layout(
        xaxis_title="Idade (anos)",
        yaxis_title="Contagem",
        height=400,
        width=600
    )
    
    return fig

# Função para criar mapa de calor para perguntas com matriz
def create_heatmap(df, columns, title):
    """Cria um mapa de calor para várias colunas relacionadas"""
    # Processa os dados para o formato adequado
    data = {}
    for col in columns:
        data[col] = df[col].value_counts(normalize=True) * 100  # Percentual
    
    # Converte para DataFrame
    heatmap_df = pd.DataFrame(data).fillna(0)
    
    # Cria o mapa de calor
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(heatmap_df, annot=True, fmt='.1f', cmap='YlGnBu', ax=ax)
    plt.title(title)
    plt.tight_layout()
    
    return fig

# Função para criar nuvem de palavras
def create_wordcloud(df, text_column, title):
    """Cria uma nuvem de palavras a partir de um texto"""
    # Concatena todos os textos da coluna
    all_text = ' '.join(df[text_column].dropna().astype(str))
    
    # Cria a nuvem de palavras
    wordcloud = WordCloud(
        width=800, 
        height=400, 
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

# Função principal
def main():
    st.title("📊 Análise de Dados do Questionário FATEC")
    
    # Carrega os dados
    try:
        df = load_data()
        st.success(f"Dados carregados com sucesso! Total de {df.shape[0]} registros.")
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return
    
    # Sidebar para navegação
    st.sidebar.title("Navegação")
    sections = [
        "Visão Geral",
        "Perfil dos Estudantes",
        "Informações Socioeconômicas",
        "Formação e Trabalho",
        "Uso de Tecnologia",
        "Interesses e Hábitos",
        "Motivações e Expectativas",
        "Análise de Texto"
    ]
    
    section = st.sidebar.radio("Ir para:", sections)
    
    # Visão Geral
    if section == "Visão Geral":
        st.header("Visão Geral dos Dados")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = create_bar_chart(df, 'Qual o seu curso?', 'Distribuição por Curso')
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            fig = create_pie_chart(df, 'Qual o período que cursa?*', 'Distribuição por Período')
            st.plotly_chart(fig, use_container_width=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            fig = create_bar_chart(df, 'Qual é o seu gênero?', 'Distribuição por Gênero')
            st.plotly_chart(fig, use_container_width=True)
            
        with col4:
            try:
                fig = create_age_histogram(df, 'Qual a sua data de nascimento?', 'Distribuição de Idade')
                st.plotly_chart(fig, use_container_width=True)
            except:
                st.warning("Não foi possível gerar o histograma de idade. Verifique o formato da data.")
        
        # Mapa dos estudantes por estado de nascimento
        st.subheader("Estado de Nascimento dos Estudantes")
        estados_count = df['Qual o estado você nasceu?*'].value_counts().reset_index()
        estados_count.columns = ['Estado', 'Contagem']
        
        # Cria o mapa do Brasil (simplificado)
        fig = px.choropleth(
            estados_count,
            locations='Estado',
            color='Contagem',
            scope="south america",
            color_continuous_scale=px.colors.sequential.Viridis,
            locationmode='ISO-3',
            title='Distribuição por Estado de Nascimento'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Perfil dos Estudantes
    elif section == "Perfil dos Estudantes":
        st.header("Perfil dos Estudantes")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = create_bar_chart(df, 'Qual é o seu estado civil?', 'Estado Civil')
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            fig = create_bar_chart(df, 'Quantos filhos você tem?', 'Quantidade de Filhos')
            st.plotly_chart(fig, use_container_width=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            fig = create_bar_chart(df, 'Com quem você mora atualmente?', 'Situação de Moradia')
            st.plotly_chart(fig, use_container_width=True)
            
        with col4:
            fig = create_bar_chart(df, 'Qual é a situação do domicílio em que você reside?', 'Tipo de Domicílio')
            st.plotly_chart(fig, use_container_width=True)
        
        # Cidade de residência (top 15)
        st.subheader("Principais Cidades de Residência")
        
        cidade_counts = df['Em qual cidade você reside?'].value_counts().head(15)
        fig = px.bar(
            x=cidade_counts.index,
            y=cidade_counts.values,
            title="Top 15 Cidades de Residência",
            labels={'x': 'Cidade', 'y': 'Contagem'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Informações Socioeconômicas
    elif section == "Informações Socioeconômicas":
        st.header("Informações Socioeconômicas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = create_bar_chart(df, 'Qual é a faixa de renda mensal da sua família?', 'Faixa de Renda Familiar')
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            fig = create_pie_chart(df, 'Há quanto tempo você mora neste domicílio?', 'Tempo de Residência')
            st.plotly_chart(fig, use_container_width=True)
        
        # Itens no domicílio
        st.subheader("Itens no Domicílio")
        
        # Seleciona as colunas dos itens
        item_columns = [
            'Televisor', 'Vídeo cassete e(ou) DVD', 'Rádio', 'Automóvel', 'Motocicleta',
            'Máquina de lavar roupa e(ou) tanquinho', 'Geladeira', 'Celular e(ou) Smartphone',
            'Microcomputador de mesa/Desktop', 'Notebook'
        ]
        
        # Prepara os dados para visualização
        item_data = {}
        for col in item_columns:
            if col in df.columns:
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
            title="Quantidade de Itens por Domicílio",
            xaxis_title="Item",
            yaxis_title="Contagem",
            barmode='stack',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Itens adicionais (sim/não)
        st.subheader("Serviços no Domicílio")
        
        service_columns = [
            'Telefone fixo', 'Internet', 'TV por assinatura e(ou) Serviços de Streaming',
            'Empregada mensalista'
        ]
        
        service_data = {}
        for col in service_columns:
            if col in df.columns:
                service_data[col] = df[col].value_counts(normalize=True) * 100
        
        service_df = pd.DataFrame(service_data).fillna(0)
        
        # Cria o gráfico
        fig = px.bar(
            service_df.T,
            labels={'index': 'Serviço', 'value': 'Percentual (%)'},
            title="Percentual de Domicílios com Serviços",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Formação e Trabalho
    elif section == "Formação e Trabalho":
        st.header("Formação e Trabalho")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = create_pie_chart(df, 'Você trabalha?', 'Situação de Trabalho')
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            fig = create_bar_chart(df, 'Qual é seu vínculo com o emprego?', 'Vínculo Empregatício')
            st.plotly_chart(fig, use_container_width=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            fig = create_bar_chart(df, 'Qual a área do seu trabalho?', 'Área de Trabalho')
            st.plotly_chart(fig, use_container_width=True)
            
        with col4:
            fig = create_bar_chart(df, 'Qual é o seu regime de trabalho?', 'Regime de Trabalho')
            st.plotly_chart(fig, use_container_width=True)
        
        # Formação escolar e plano de saúde
        col5, col6 = st.columns(2)
        
        with col5:
            fig = create_bar_chart(df, 'Na sua vida escolar, você estudou....', 'Formação Escolar')
            st.plotly_chart(fig, use_container_width=True)
            
        with col6:
            fig = create_bar_chart(df, 'Você tem plano de saúde privado?', 'Plano de Saúde')
            st.plotly_chart(fig, use_container_width=True)
        
        # Escolaridade dos pais
        st.subheader("Escolaridade dos Pais")
        
        # Prepara os dados
        escolaridade_mae = df['Qual é o grau de escolaridade da sua mãe?'].value_counts().reset_index()
        escolaridade_mae.columns = ['Escolaridade', 'Contagem']
        escolaridade_mae['Pai/Mãe'] = 'Mãe'
        
        escolaridade_pai = df['Qual é o grau de escolaridade do seu pai?'].value_counts().reset_index()
        escolaridade_pai.columns = ['Escolaridade', 'Contagem']
        escolaridade_pai['Pai/Mãe'] = 'Pai'
        
        escolaridade_df = pd.concat([escolaridade_mae, escolaridade_pai])
        
        # Cria o gráfico
        fig = px.bar(
            escolaridade_df,
            x='Escolaridade',
            y='Contagem',
            color='Pai/Mãe',
            barmode='group',
            title='Comparação da Escolaridade entre Pai e Mãe',
            color_discrete_sequence=['#ff6b6b', '#48dbfb']
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Uso de Tecnologia
    elif section == "Uso de Tecnologia":
        st.header("Uso de Tecnologia")
        
        # Conhecimento em informática
        st.subheader("Conhecimento em Informática")
        fig = create_bar_chart(df, 'Como você classifica seu conhecimento em informática?', 'Nível de Conhecimento em Informática')
        st.plotly_chart(fig, use_container_width=True)
        
        # Conhecimento em aplicativos específicos
        st.subheader("Conhecimento em Aplicativos e Sistemas")
        
        app_columns = [
            'Windowns', 'Linux', 'Editores de textos (word, writer, ...)',
            'Planilhas Eletrônicas (Excel, Cal, ...)', 'Apresentadores (PowerPoint, Impress, ...)',
            'Sistemas de Gestão Empresarial', 'Inglês'
        ]
        
        # Verifica quais colunas existem no DataFrame
        available_columns = [col for col in app_columns if col in df.columns]
        
        if available_columns:
            try:
                fig = create_heatmap(df, available_columns, 'Nível de Conhecimento em Aplicativos e Sistemas')
                st.pyplot(fig)
            except:
                st.warning("Não foi possível gerar o mapa de calor para conhecimento em aplicativos.")
        
        # Uso de dispositivos
        st.subheader("Uso de Dispositivos")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### Desktop")
            desktop_cols = ['Em casa', 'No trabalho', 'Na escola', 'Em outros lugares']
            for col in desktop_cols:
                if col in df.columns:
                    counts = df[col].value_counts(normalize=True) * 100
                    st.write(f"**{col}**: Sim ({counts.get('Sim', 0):.1f}%), Não ({counts.get('Não', 0):.1f}%)")
        
        with col2:
            st.markdown("### Notebook")
            notebook_cols = ['Em casa2', 'No trabalho2', 'Na escola2', 'Em outros lugares2']
            for i, col in enumerate(notebook_cols):
                if col in df.columns:
                    counts = df[col].value_counts(normalize=True) * 100
                    st.write(f"**{desktop_cols[i].replace('2', '')}**: Sim ({counts.get('Sim', 0):.1f}%), Não ({counts.get('Não', 0):.1f}%)")
        
        with col3:
            st.markdown("### Smartphone")
            smartphone_cols = ['Em casa3', 'No trabalho3', 'Na escola3', 'Em outros lugares3']
            for i, col in enumerate(smartphone_cols):
                if col in df.columns:
                    counts = df[col].value_counts(normalize=True) * 100
                    st.write(f"**{desktop_cols[i].replace('3', '')}**: Sim ({counts.get('Sim', 0):.1f}%), Não ({counts.get('Não', 0):.1f}%)")
        
        # Finalidade de uso dos dispositivos
        st.subheader("Finalidade de Uso dos Dispositivos")
        
        # Dispositivos e suas finalidades
        devices = {
            "Desktop": [
                'Para trabalhos profissionais', 'Para trabalhos escolares',
                'Para entretenimento (música, redes sociais,...)', 'Para comunicação por e-mail',
                'Para operações bancárias', 'Para compras eletrônicas'
            ],
            "Notebook": [
                'Para trabalhos profissionais2', 'Para trabalhos escolares2',
                'Para entretenimento (música, redes sociais,...)2', 'Para comunicação por e-mail2',
                'Para operações bancárias2', 'Para compras eletrônicas2'
            ],
            "Smartphone": [
                'Para trabalhos profissionais3', 'Para trabalhos escolares3',
                'Para entretenimento (música, redes sociais,...)3', 'Para comunicação por e-mail3',
                'Para operações bancárias3', 'Para compras eletrônicas3'
            ]
        }
        
        # Processa os dados para visualização
        device_usage = []
        
        for device, cols in devices.items():
            for col in cols:
                if col in df.columns:
                    # Extrai o propósito (remove números e sufixos)
                    purpose = col.replace('2', '').replace('3', '')
                    yes_count = df[col].value_counts().get('Sim', 0)
                    device_usage.append({
                        'Dispositivo': device,
                        'Finalidade': purpose,
                        'Contagem': yes_count
                    })
        
        # Converte para DataFrame
        device_usage_df = pd.DataFrame(device_usage)
        
        # Cria o gráfico
        if not device_usage_df.empty:
            fig = px.bar(
                device_usage_df,
                x='Finalidade',
                y='Contagem',
                color='Dispositivo',
                barmode='group',
                title='Finalidade de Uso por Tipo de Dispositivo',
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            
            fig.update_layout(
                xaxis={'categoryorder':'total descending'},
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Não foi possível gerar o gráfico de finalidade de uso dos dispositivos.")
    
    # Interesses e Hábitos
    elif section == "Interesses e Hábitos":
        st.header("Interesses e Hábitos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = create_bar_chart(df, 'Não considerando os livros acadêmicos, quantos livros você lê por ano (em média)?', 'Quantidade de Livros Lidos por Ano')
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            fig = create_bar_chart(df, 'Se você lê livros literários, qual(is) o(s) gênero(s) preferido(s)?', 'Gêneros Literários Preferidos')
            st.plotly_chart(fig, use_container_width=True)
        
        # Fontes de informação
        st.subheader("Frequência de Uso de Fontes de Informação")
        
        info_columns = [
            'TV', 'Internet2', 'Revistas', 'Jornais', 'Rádio2', 'Redes Sociais', 'Conversas com Amigos'
        ]
        
        # Verifica quais colunas existem no DataFrame
        available_columns = [col for col in info_columns if col in df.columns]
        
        if available_columns:
            try:
                fig = create_heatmap(df, available_columns, 'Frequência de Uso de Fontes de Informação')
                st.pyplot(fig)
            except:
                st.warning("Não foi possível gerar o mapa de calor para fontes de informação.")
        
        col3, col4 = st.columns(2)
        
        with col3:
            fig = create_pie_chart(df, 'Você dedica parte do seu tempo para atividades voluntárias?', 'Participação em Atividades Voluntárias')
            st.plotly_chart(fig, use_container_width=True)
            
        with col4:
            fig = create_bar_chart(df, 'Qual religião você professa?', 'Religião')
            st.plotly_chart(fig, use_container_width=True)
        
        # Entretenimento cultural
        st.subheader("Fontes de Entretenimento Cultural")
        
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
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Dados sobre fontes de entretenimento cultural não disponíveis.")
    
    # Motivações e Expectativas
    elif section == "Motivações e Expectativas":
        st.header("Motivações e Expectativas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = create_bar_chart(df, 'Estamos quase no fim! Como você ficou sabendo da FATEC Franca?', 'Como Conheceu a FATEC')
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            fig = create_bar_chart(df, 'Por que você escolheu este curso?', 'Motivo da Escolha do Curso')
            st.plotly_chart(fig, use_container_width=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            fig = create_bar_chart(df, 'Qual sua maior expectativa quanto ao curso?', 'Expectativa Quanto ao Curso')
            st.plotly_chart(fig, use_container_width=True)
            
        with col4:
            fig = create_bar_chart(df, 'Qual sua expectativa após se formar?', 'Expectativa Após Formação')
            st.plotly_chart(fig, use_container_width=True)
        
        # Outras informações acadêmicas
        st.subheader("Outras Informações Acadêmicas")
        
        col5, col6, col7 = st.columns(3)
        
        with col5:
            fig = create_pie_chart(df, 'Você já estudou nesta instituição?', 'Estudou na FATEC Anteriormente')
            st.plotly_chart(fig, use_container_width=True)
            
        with col6:
            fig = create_bar_chart(df, 'Você já fez algum curso técnico?', 'Curso Técnico')
            st.plotly_chart(fig, use_container_width=True)
            
        with col7:
            fig = create_bar_chart(df, 'Qual meio de transporte você utiliza para ir à faculdade?', 'Meio de Transporte')
            st.plotly_chart(fig, use_container_width=True)
    
    # Análise de Texto
    elif section == "Análise de Texto":
        st.header("Análise de Textos e Respostas Abertas")
        
        # Verificar se temos a coluna de texto sobre história e sonhos
        if 'Escreva algumas linhas sobre sua história e seus sonhos de vida' in df.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Distribuição de Palavras nos Sonhos")
                fig = create_wordcloud(
                    df,
                    'Escreva algumas linhas sobre sua história e seus sonhos de vida',
                    'Nuvem de Palavras - Sonhos e Histórias'
                )
                st.pyplot(fig)
                
            with col2:
                st.subheader("Palavras Mais Frequentes")
                all_text = ' '.join(df['Escreva algumas linhas sobre sua história e seus sonhos de vida'].dropna().astype(str))
                words = [word for word in all_text.split() if len(word) > 3]
                word_counts = Counter(words).most_common(20)
                
                fig = px.bar(
                    x=[count[1] for count in word_counts],
                    y=[count[0] for count in word_counts],
                    orientation='h',
                    labels={'x': 'Frequência', 'y': 'Palavra'},
                    color_discrete_sequence=['darkblue']
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Coluna de texto não encontrada no conjunto de dados")

if __name__ == "__main__":
    main()
