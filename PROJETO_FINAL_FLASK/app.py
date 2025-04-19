from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import os
import pandas as pd
import json
import uuid
from werkzeug.utils import secure_filename
from data_processing import process_excel_file, load_data, check_data_ready, create_directories
from visualization import (
    generate_visao_geral_charts,
    generate_perfil_estudantes_charts,
    generate_socioeconomico_charts,
    generate_trabalho_formacao_charts,
    generate_tecnologia_charts,
    generate_interesses_habitos_charts,
    generate_motivacoes_expectativas_charts,
    generate_analise_texto_charts
)
from config import config
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create Flask application
app = Flask(__name__)

# Load configuration
env = os.environ.get('FLASK_ENV', 'default')
app.config.from_object(config[env])

# Initialize app with configuration
config[env].init_app(app)

# Routes
@app.route('/')
def home():
    # Check if data is already processed
    data_ready = check_data_ready()
    return render_template('upload.html', data_ready=data_ready)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('Nenhum arquivo selecionado', 'danger')
        return redirect(url_for('home'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('Nenhum arquivo selecionado', 'danger')
        return redirect(url_for('home'))
    
    if file and (file.filename.endswith('.xlsx') or file.filename.endswith('.xls')):
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)
        
        # Process the file
        logger.info(f"Processing uploaded file: {filename}")
        success, message = process_excel_file(upload_path)
        
        if success:
            flash(message, 'success')
            return redirect(url_for('dashboard', section='visao_geral'))
        else:
            flash(f'Erro: {message}', 'danger')
            return redirect(url_for('home'))
    else:
        flash('Arquivo deve ser do tipo Excel (.xlsx ou .xls)', 'danger')
        return redirect(url_for('home'))

@app.route('/dashboard')
@app.route('/dashboard/<section>')
def dashboard(section='visao_geral'):
    # Check if data is ready
    if not check_data_ready():
        flash('Nenhum dado processado. Faça o upload de um arquivo primeiro.', 'danger')
        return redirect(url_for('home'))
    
    # Load data
    try:
        df = load_data()
        if df.empty:
            flash('Erro ao carregar dados. O arquivo pode estar vazio ou mal formatado.', 'danger')
            return redirect(url_for('home'))
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        flash(f'Erro ao carregar dados: {str(e)}', 'danger')
        return redirect(url_for('home'))
    
    # Basic stats for dashboard header
    stats = {
        'total_records': len(df),
        'courses': df['Qual o seu curso?'].nunique() if 'Qual o seu curso?' in df.columns else 0,
        'genders': df['Qual é o seu gênero?'].nunique() if 'Qual é o seu gênero?' in df.columns else 0
    }
    
    # Return the appropriate template based on section
    sections = {
        'visao_geral': 'Visão Geral',
        'perfil_estudantes': 'Perfil dos Estudantes',
        'socioeconomico': 'Informações Socioeconômicas',
        'trabalho_formacao': 'Formação e Trabalho',
        'tecnologia': 'Uso de Tecnologia',
        'interesses_habitos': 'Interesses e Hábitos',
        'motivacoes_expectativas': 'Motivações e Expectativas',
        'analise_texto': 'Análise de Texto'
    }
    
    return render_template(
        'dashboard.html',
        section=section,
        section_title=sections.get(section, 'Dashboard'),
        sections=sections,
        stats=stats
    )

@app.route('/get_charts/<section>')
def get_charts(section):
    """API to get chart data for a specific section"""
    if not check_data_ready():
        return jsonify({'error': 'No data available'}), 404
    
    try:
        df = load_data()
        if df.empty:
            return jsonify({'error': 'Empty dataset'}), 404
        
        # Log section request
        logger.info(f"Generating charts for section: {section}")
        
        # Generate charts for the requested section
        charts = {}
        
        if section == 'visao_geral':
            charts = generate_visao_geral_charts(df)
        elif section == 'perfil_estudantes':
            charts = generate_perfil_estudantes_charts(df)
        elif section == 'socioeconomico':
            charts = generate_socioeconomico_charts(df)
        elif section == 'trabalho_formacao':
            charts = generate_trabalho_formacao_charts(df)
        elif section == 'tecnologia':
            charts = generate_tecnologia_charts(df)
        elif section == 'interesses_habitos':
            charts = generate_interesses_habitos_charts(df)
        elif section == 'motivacoes_expectativas':
            charts = generate_motivacoes_expectativas_charts(df)
        elif section == 'analise_texto':
            charts = generate_analise_texto_charts(df)
        else:
            return jsonify({'error': 'Invalid section'}), 400
        
        # Log chart generation success
        chart_keys = list(charts.keys())
        logger.info(f"Successfully generated {len(chart_keys)} charts for section {section}: {chart_keys}")
        
        return jsonify(charts)
    
    except Exception as e:
        logger.error(f"Error generating charts for {section}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/clear_data', methods=['POST'])
def clear_data():
    """Clear processed data"""
    try:
        if os.path.exists('./database/colunas.csv'):
            os.remove('./database/colunas.csv')
        if os.path.exists('./database/dados.json'):
            os.remove('./database/dados.json')
        logger.info("Data cleared successfully")
        flash('Dados limpos com sucesso!', 'success')
    except Exception as e:
        logger.error(f"Error clearing data: {str(e)}")
        flash(f'Erro ao limpar dados: {str(e)}', 'danger')
    
    return redirect(url_for('home'))

@app.route('/debug_data')
def debug_data():
    """Debug endpoint to view raw data (development only)"""
    if not app.debug:
        return "Debug mode is not enabled", 403
    
    try:
        df = load_data()
        # Return the first 50 rows as HTML with additional debug info
        html_output = "<h2>Debug Data</h2>"
        
        # Add information about cities
        if 'Em qual cidade você reside?' in df.columns:
            html_output += "<h3>City Count Debug</h3>"
            city_counts = df['Em qual cidade você reside?'].value_counts().head(20)
            html_output += f"<pre>{city_counts.to_string()}</pre>"
        
        # Add general dataframe info
        html_output += "<h3>DataFrame Info</h3>"
        buffer = pd.io.StringIO()
        df.info(buf=buffer)
        html_output += f"<pre>{buffer.getvalue()}</pre>"
        
        # Add first rows
        html_output += "<h3>First 50 Rows</h3>"
        html_output += df.head(50).to_html()
        
        return html_output
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/version')
def version():
    """Return app version info"""
    return jsonify({
        'app': 'Análise Socioeconômica FATEC',
        'version': '2.0.0',
        'visualization_library': 'Highcharts',
        'framework': 'Flask'
    })

@app.errorhandler(404)
def page_not_found(e):
    logger.warning(f"404 error: {request.path}")
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f"500 error: {str(e)}")
    return render_template('500.html'), 500

if __name__ == '__main__':
    logger.info("Starting application")
    create_directories()
    app.run(debug=True)
