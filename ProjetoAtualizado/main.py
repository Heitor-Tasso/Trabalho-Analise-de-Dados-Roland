import streamlit as st
import pandas as pd
import numpy as np
import os
from data_processing import process_excel_file, load_data, check_data_ready, create_directories
from lista_graficos import (
    generate_visao_geral,
    generate_perfil_estudantes,
    generate_socioeconomico,
    generate_trabalho_formacao,
    generate_tecnologia,
    generate_interesses_habitos,
    generate_motivacoes_expectativas,
    generate_analise_texto
)

# Configuração da página
st.set_page_config(
    page_title="Análise de Dados dos Estudantes FATEC",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Função para aplicar estilos personalizados
def apply_custom_css():
    st.markdown("""
        <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1, h2, h3 {
            color: #1E3A8A;
        }
        .stSidebar h1 {
            font-size: 1.5rem;
        }
        .stSidebar h2 {
            font-size: 1.2rem;
        }
        .upload-section {
            padding: 2rem;
            border-radius: 10px;
            background-color: #f8f9fa;
            margin-bottom: 2rem;
            text-align: center;
        }
        .success-message {
            padding: 1rem;
            border-radius: 5px;
            background-color: #d1e7dd;
            color: #0f5132;
            margin: 1rem 0;
        }
        .info-message {
            padding: 1rem;
            border-radius: 5px;
            background-color: #cff4fc;
            color: #055160;
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

# Função para a página de upload
def render_upload_page():
    st.title("📤 Upload de Dados do Questionário Socioeconômico")
    
    st.markdown("""
    <div class="upload-section">
        <h2>Bem-vindo ao Sistema de Análise de Dados Socioeconômicos da FATEC</h2>
        <p>Para começar, faça o upload do arquivo Excel com os dados do questionário.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Instruções")
        st.markdown("""
        1. Prepare seu arquivo Excel com os dados do questionário socioeconômico;
        2. Certifique-se de que o arquivo contenha uma coluna "ID" para identificar cada registro;
        3. Clique no botão ao lado para fazer o upload;
        4. Após o processamento, você será redirecionado para a visualização dos gráficos.
        
        **Nota**: Os dados serão armazenados temporariamente para análise e não serão compartilhados.
        """)
    
    with col2:
        uploaded_file = st.file_uploader("Escolha o arquivo Excel", type=['xlsx', 'xls'])
        
        if uploaded_file is not None:
            with st.spinner('Processando arquivo...'):
                success, message = process_excel_file(uploaded_file)
                
                if success:
                    st.session_state.data_processed = True
                    st.success(message)
                    st.markdown("""
                    <div class="success-message">
                        Dados processados com sucesso! 
                        Clique no botão abaixo para visualizar os gráficos.
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("Visualizar Gráficos", key="goto_vizualization"):
                        st.session_state.page = "visualization"
                        st.experimental_rerun()
                else:
                    st.error(message)

# Função para a página de visualização
def render_visualization_page():
    st.title("📊 Análise de Dados do Questionário Socioeconômico FATEC")
    
    # Carrega os dados
    try:
        df = load_data()
        if df.empty:
            st.error("Não foi possível carregar os dados. Por favor, faça o upload novamente.")
            if st.button("Voltar para Upload", key="back_to_upload"):
                st.session_state.page = "upload"
                st.experimental_rerun()
            return
            
        st.markdown(f"""
        <div class="info-message">
            <strong>Dados carregados com sucesso!</strong> Total de {df.shape[0]} registros.
        </div>
        """, unsafe_allow_html=True)
        
        # Botão para voltar à página de upload
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("⬅️ Upload de Novo Arquivo", key="new_upload"):
                st.session_state.page = "upload"
                st.experimental_rerun()
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        if st.button("Voltar para Upload", key="error_back"):
            st.session_state.page = "upload"
            st.experimental_rerun()
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
    
    # Geração dos gráficos para cada seção
    if section == "Visão Geral":
        st.header("Visão Geral dos Dados")
        graficos = generate_visao_geral(df)
        
        if graficos:
            # Layout com duas colunas
            col1, col2 = st.columns(2)
            
            with col1:
                if 'curso' in graficos and graficos['curso']:
                    st.plotly_chart(graficos['curso'], use_container_width=True)
                
                if 'genero' in graficos and graficos['genero']:
                    st.plotly_chart(graficos['genero'], use_container_width=True)
            
            with col2:
                if 'periodo' in graficos and graficos['periodo']:
                    st.plotly_chart(graficos['periodo'], use_container_width=True)
                
                if 'idade' in graficos and graficos['idade']:
                    st.plotly_chart(graficos['idade'], use_container_width=True)
            
            # Mapa em largura completa
            if 'mapa_estados' in graficos and graficos['mapa_estados']:
                st.subheader("Estado de Nascimento dos Estudantes")
                st.plotly_chart(graficos['mapa_estados'], use_container_width=True)
    
    elif section == "Perfil dos Estudantes":
        st.header("Perfil dos Estudantes")
        graficos = generate_perfil_estudantes(df)
        
        if graficos:
            col1, col2 = st.columns(2)
            
            with col1:
                if 'estado_civil' in graficos and graficos['estado_civil']:
                    st.plotly_chart(graficos['estado_civil'], use_container_width=True)
                
                if 'moradia' in graficos and graficos['moradia']:
                    st.plotly_chart(graficos['moradia'], use_container_width=True)
                
                if 'necessidades_especiais' in graficos and graficos['necessidades_especiais']:
                    st.plotly_chart(graficos['necessidades_especiais'], use_container_width=True)
            
            with col2:
                if 'filhos' in graficos and graficos['filhos']:
                    st.plotly_chart(graficos['filhos'], use_container_width=True)
                
                if 'tipo_domicilio' in graficos and graficos['tipo_domicilio']:
                    st.plotly_chart(graficos['tipo_domicilio'], use_container_width=True)
            
            # Cidades em largura completa
            if 'cidades' in graficos and graficos['cidades']:
                st.subheader("Principais Cidades de Residência")
                st.plotly_chart(graficos['cidades'], use_container_width=True)
    
    elif section == "Informações Socioeconômicas":
        st.header("Informações Socioeconômicas")
        graficos = generate_socioeconomico(df)
        
        if graficos:
            col1, col2 = st.columns(2)
            
            with col1:
                if 'renda' in graficos and graficos['renda']:
                    st.plotly_chart(graficos['renda'], use_container_width=True)
                
                if 'pessoas_domicilio' in graficos and graficos['pessoas_domicilio']:
                    st.plotly_chart(graficos['pessoas_domicilio'], use_container_width=True)
            
            with col2:
                if 'tempo_residencia' in graficos and graficos['tempo_residencia']:
                    st.plotly_chart(graficos['tempo_residencia'], use_container_width=True)
            
            # Gráficos em largura completa
            if 'itens_domicilio' in graficos and graficos['itens_domicilio']:
                st.subheader("Itens no Domicílio")
                st.plotly_chart(graficos['itens_domicilio'], use_container_width=True)
            
            if 'servicos_domicilio' in graficos and graficos['servicos_domicilio']:
                st.subheader("Serviços no Domicílio")
                st.plotly_chart(graficos['servicos_domicilio'], use_container_width=True)
    
    elif section == "Formação e Trabalho":
        st.header("Formação e Trabalho")
        graficos = generate_trabalho_formacao(df)
        
        if graficos:
            col1, col2 = st.columns(2)
            
            with col1:
                if 'trabalha' in graficos and graficos['trabalha']:
                    st.plotly_chart(graficos['trabalha'], use_container_width=True)
                
                if 'area_trabalho' in graficos and graficos['area_trabalho']:
                    st.plotly_chart(graficos['area_trabalho'], use_container_width=True)
                
                if 'formacao_escolar' in graficos and graficos['formacao_escolar']:
                    st.plotly_chart(graficos['formacao_escolar'], use_container_width=True)
            
            with col2:
                if 'vinculo' in graficos and graficos['vinculo']:
                    st.plotly_chart(graficos['vinculo'], use_container_width=True)
                
                if 'regime_trabalho' in graficos and graficos['regime_trabalho']:
                    st.plotly_chart(graficos['regime_trabalho'], use_container_width=True)
                
                if 'plano_saude' in graficos and graficos['plano_saude']:
                    st.plotly_chart(graficos['plano_saude'], use_container_width=True)
            
            # Gráfico em largura completa
            if 'escolaridade_pais' in graficos and graficos['escolaridade_pais']:
                st.subheader("Escolaridade dos Pais")
                st.plotly_chart(graficos['escolaridade_pais'], use_container_width=True)
            
            if 'curso_tecnico' in graficos and graficos['curso_tecnico']:
                st.subheader("Formação Técnica")
                st.plotly_chart(graficos['curso_tecnico'], use_container_width=True)
    
    elif section == "Uso de Tecnologia":
        st.header("Uso de Tecnologia")
        graficos = generate_tecnologia(df)
        
        if graficos:
            # Conhecimento em informática
            if 'conhecimento_informatica' in graficos and graficos['conhecimento_informatica']:
                st.subheader("Conhecimento em Informática")
                st.plotly_chart(graficos['conhecimento_informatica'], use_container_width=True)
            
            # Mapa de calor de conhecimento em aplicativos
            if 'conhecimento_apps' in graficos and graficos['conhecimento_apps']:
                st.subheader("Conhecimento em Aplicativos e Sistemas")
                st.pyplot(graficos['conhecimento_apps'])
            
            # Uso de dispositivos
            if 'uso_dispositivos' in graficos and graficos['uso_dispositivos']:
                st.subheader("Uso de Dispositivos por Local")
                st.plotly_chart(graficos['uso_dispositivos'], use_container_width=True)
            
            # Finalidade de uso
            if 'finalidade_uso' in graficos and graficos['finalidade_uso']:
                st.subheader("Finalidade de Uso dos Dispositivos")
                st.plotly_chart(graficos['finalidade_uso'], use_container_width=True)
            
            # Conhecimento de idiomas
            if 'conhecimento_idiomas' in graficos and graficos['conhecimento_idiomas']:
                st.subheader("Conhecimento em Idiomas")
                st.pyplot(graficos['conhecimento_idiomas'])
    
    elif section == "Interesses e Hábitos":
        st.header("Interesses e Hábitos")
        graficos = generate_interesses_habitos(df)
        
        if graficos:
            col1, col2 = st.columns(2)
            
            with col1:
                if 'livros_ano' in graficos and graficos['livros_ano']:
                    st.plotly_chart(graficos['livros_ano'], use_container_width=True)
                
                if 'voluntariado' in graficos and graficos['voluntariado']:
                    st.plotly_chart(graficos['voluntariado'], use_container_width=True)
            
            with col2:
                if 'generos_literarios' in graficos and graficos['generos_literarios']:
                    st.plotly_chart(graficos['generos_literarios'], use_container_width=True)
                
                if 'religiao' in graficos and graficos['religiao']:
                    st.plotly_chart(graficos['religiao'], use_container_width=True)
            
            # Fontes de informação (mapa de calor)
            if 'fontes_informacao' in graficos and graficos['fontes_informacao']:
                st.subheader("Frequência de Uso de Fontes de Informação")
                st.pyplot(graficos['fontes_informacao'])
            
            # Entretenimento cultural
            if 'entretenimento_cultural' in graficos and graficos['entretenimento_cultural']:
                st.subheader("Fontes de Entretenimento Cultural")
                st.plotly_chart(graficos['entretenimento_cultural'], use_container_width=True)
    
    elif section == "Motivações e Expectativas":
        st.header("Motivações e Expectativas")
        graficos = generate_motivacoes_expectativas(df)
        
        if graficos:
            col1, col2 = st.columns(2)
            
            with col1:
                if 'conheceu_fatec' in graficos and graficos['conheceu_fatec']:
                    st.plotly_chart(graficos['conheceu_fatec'], use_container_width=True)
                
                if 'expectativa_curso' in graficos and graficos['expectativa_curso']:
                    st.plotly_chart(graficos['expectativa_curso'], use_container_width=True)
                
                if 'estudou_fatec' in graficos and graficos['estudou_fatec']:
                    st.plotly_chart(graficos['estudou_fatec'], use_container_width=True)
            
            with col2:
                if 'motivo_curso' in graficos and graficos['motivo_curso']:
                    st.plotly_chart(graficos['motivo_curso'], use_container_width=True)
                
                if 'expectativa_formacao' in graficos and graficos['expectativa_formacao']:
                    st.plotly_chart(graficos['expectativa_formacao'], use_container_width=True)
                
                if 'curso_tecnico' in graficos and graficos['curso_tecnico']:
                    st.plotly_chart(graficos['curso_tecnico'], use_container_width=True)
            
            # Transporte em largura completa
            if 'transporte' in graficos and graficos['transporte']:
                st.subheader("Meio de Transporte")
                st.plotly_chart(graficos['transporte'], use_container_width=True)
    
    elif section == "Análise de Texto":
        st.header("Análise de Textos e Respostas Abertas")
        graficos = generate_analise_texto(df)
        
        if graficos:
            col1, col2 = st.columns(2)
            
            with col1:
                if 'nuvem_sonhos' in graficos and graficos['nuvem_sonhos']:
                    st.subheader("Distribuição de Palavras nos Sonhos")
                    st.pyplot(graficos['nuvem_sonhos'])
            
            with col2:
                if 'freq_palavras' in graficos and graficos['freq_palavras']:
                    st.subheader("Palavras Mais Frequentes")
                    st.plotly_chart(graficos['freq_palavras'], use_container_width=True)
            
            # Exibir alguns exemplos de respostas
            texto_col = 'Escreva algumas linhas sobre sua história e seus sonhos de vida'
            if texto_col in df.columns:
                st.subheader("Exemplos de Respostas")
                
                # Pegar apenas respostas não vazias
                respostas = df[df[texto_col].notna() & (df[texto_col] != '')][texto_col]
                
                if not respostas.empty:
                    # Selecionar até 5 respostas aleatórias
                    amostra = respostas.sample(min(5, len(respostas)))
                    
                    for i, resposta in enumerate(amostra):
                        with st.expander(f"Resposta {i+1}"):
                            st.write(resposta)
                else:
                    st.info("Não há respostas de texto para exibir.")

# Função para exportar análise para PDF (placeholder)
def export_analysis_pdf():
    st.warning("Funcionalidade de exportação para PDF será implementada em versões futuras.")

# Função principal
def main():
    # Aplica estilos personalizados
    apply_custom_css()
    
    # Verifica se diretórios existem
    create_directories()
    
    # Inicializa o estado da sessão se necessário
    if 'page' not in st.session_state:
        st.session_state.page = "upload"
    
    if 'data_processed' not in st.session_state:
        st.session_state.data_processed = check_data_ready()
    
    # Se dados estão prontos, podemos ir direto para visualização
    if st.session_state.data_processed and st.session_state.page == "upload":
        # Adiciona um botão para ir para visualização
        st.sidebar.success("Dados já processados disponíveis!")
        if st.sidebar.button("Visualizar Gráficos", key="sidebar_viz"):
            st.session_state.page = "visualization"
            st.experimental_rerun()
    
    # Renderiza a página apropriada
    if st.session_state.page == "upload":
        render_upload_page()
    else:  # visualization
        render_visualization_page()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "Desenvolvido para análise de dados socioeconômicos dos estudantes da FATEC - 2025"
    )
    
    # Sidebar - opções adicionais
    st.sidebar.markdown("---")
    st.sidebar.header("Ferramentas")
    
    if st.session_state.data_processed:
        if st.sidebar.button("Exportar Análise (PDF)", key="export_pdf"):
            export_analysis_pdf()
    
    # Botão para limpar dados processados
    if st.session_state.data_processed:
        if st.sidebar.button("Limpar Dados Processados", key="clear_data"):
            try:
                if os.path.exists('./database/colunas.csv'):
                    os.remove('./database/colunas.csv')
                if os.path.exists('./database/dados.json'):
                    os.remove('./database/dados.json')
                st.session_state.data_processed = False
                st.session_state.page = "upload"
                st.sidebar.success("Dados limpos com sucesso!")
                st.experimental_rerun()
            except Exception as e:
                st.sidebar.error(f"Erro ao limpar dados: {e}")

if __name__ == "__main__":
    main()