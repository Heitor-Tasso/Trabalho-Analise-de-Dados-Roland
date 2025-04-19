#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

def create_directory_structure(base_dir):
    """Create the new directory structure for the project."""
    # Define the directory structure
    directories = [
        # Main modules
        'app',
        'app/routes',
        'app/services',
        'app/models',
        'app/config',
        'app/utils',
        
        # Static files
        'app/static',
        'app/static/css',
        'app/static/js',
        'app/static/js/charts',
        'app/static/js/utils',
        'app/static/img',
        
        # Templates
        'app/templates',
        'app/templates/base',
        'app/templates/dashboard',
        'app/templates/dashboard/partials',
        'app/templates/upload',
        'app/templates/errors',
        
        # Tests
        'app/tests'
    ]
    
    # Create directories
    for directory in directories:
        dir_path = os.path.join(base_dir, directory)
        os.makedirs(dir_path, exist_ok=True)
        print(f"Created directory: {dir_path}")

def create_init_files(base_dir):
    """Create __init__.py files for Python packages."""
    python_packages = [
        'app/routes',
        'app/services',
        'app/models',
        'app/config',
        'app/utils',
        'app/tests'
    ]
    
    for package in python_packages:
        init_file = os.path.join(base_dir, package, '__init__.py')
        with open(init_file, 'w') as f:
            f.write('# Initialize package\n')
        print(f"Created init file: {init_file}")

def migrate_existing_files(base_dir, source_dir):
    """Migrate existing files to the new structure."""
    file_mapping = {
        # Python files
        'app.py': 'app/app.py',
        'config.py': 'app/config/settings.py',
        'data_processing.py': 'app/services/data_processor.py',
        'visualization.py': 'app/services/chart_generator.py',
        
        # Templates
        'base.html': 'app/templates/base/layout.html',
        'dashboard.html': 'app/templates/dashboard/index.html',
        'upload.html': 'app/templates/upload/index.html',
        '404.html': 'app/templates/errors/404.html',
        '500.html': 'app/templates/errors/500.html',
        
        # Static files
        'style.css': 'app/static/css/main.css',
        'charts.css': 'app/static/css/charts.css',
        'main.js': 'app/static/js/main.js',
        'chart-standardizer.js': 'app/static/js/charts/formatter.js'
    }
    
    for source_file, target_file in file_mapping.items():
        source_path = os.path.join(source_dir, source_file)
        target_path = os.path.join(base_dir, target_file)
        
        if os.path.exists(source_path):
            # Ensure target directory exists
            target_dir = os.path.dirname(target_path)
            os.makedirs(target_dir, exist_ok=True)
            
            # Copy file
            shutil.copy2(source_path, target_path)
            print(f"Migrated: {source_file} -> {target_file}")
        else:
            print(f"Warning: Source file not found: {source_path}")

def create_new_files(base_dir):
    """Create new files for the refactored structure."""
    new_files = {
        # Routes
        'app/routes/__init__.py': '# Initialize routes package\nfrom . import dashboard, upload, api\n',
        'app/routes/dashboard.py': '# Dashboard routes\nfrom flask import Blueprint, render_template, request, jsonify\n\ndashboard_bp = Blueprint("dashboard", __name__)\n\n@dashboard_bp.route("/")\n@dashboard_bp.route("/<section>")\ndef dashboard(section="visao_geral"):\n    """Dashboard route with section navigation"""\n    return render_template("dashboard/index.html", section=section)\n\n@dashboard_bp.route("/get_charts/<section>")\ndef get_charts(section):\n    """API to get chart data for a specific section"""\n    # Implementation will be migrated from app.py\n    pass\n',
        'app/routes/upload.py': '# Upload routes\nfrom flask import Blueprint, render_template, request, redirect, url_for, flash\n\nupload_bp = Blueprint("upload", __name__)\n\n@upload_bp.route("/")\ndef home():\n    """Home page with upload form"""\n    return render_template("upload/index.html")\n\n@upload_bp.route("/upload", methods=["POST"])\ndef upload_file():\n    """Handle file upload"""\n    # Implementation will be migrated from app.py\n    pass\n',
        'app/routes/api.py': '# API routes\nfrom flask import Blueprint, jsonify\n\napi_bp = Blueprint("api", __name__)\n\n@api_bp.route("/version")\ndef version():\n    """Return app version info"""\n    return jsonify({\n        "app": "Análise Socioeconômica FATEC",\n        "version": "2.0.0",\n        "visualization_library": "Highcharts",\n        "framework": "Flask"\n    })\n',
        
        # Services
        'app/services/analytics.py': '# Analytics service\nimport pandas as pd\nimport numpy as np\nimport re\nfrom collections import Counter\n\ndef analyze_text_responses(df, text_column):\n    """Analyze text responses"""\n    # Implementation will be migrated from visualization.py\n    pass\n\ndef analyze_demographics(df):\n    """Analyze demographic data"""\n    # Implementation will be migrated from visualization.py\n    pass\n',
        
        # Models
        'app/models/questionnaire.py': '# Questionnaire model\nclass Questionnaire:\n    """Model for socioeconomic questionnaire"""\n    \n    def __init__(self, data=None):\n        self.data = data\n        \n    def from_dataframe(self, df):\n        """Load data from pandas DataFrame"""\n        self.data = df\n        return self\n    \n    def get_section_data(self, section):\n        """Get data for a specific section"""\n        # Implementation based on section\n        pass\n',
        
        # Utils
        'app/utils/file_handlers.py': '# File handling utilities\nimport os\nimport pandas as pd\nimport json\n\ndef save_processed_data(df, output_dir="./database"):\n    """Save processed data to files"""\n    # Implementation will be migrated from data_processing.py\n    pass\n\ndef load_processed_data(input_dir="./database"):\n    """Load processed data from files"""\n    # Implementation will be migrated from data_processing.py\n    pass\n',
        'app/utils/data_standardizer.py': '# Data standardization utilities\nimport re\nimport pandas as pd\nimport logging\n\nlogger = logging.getLogger(__name__)\n\ndef standardize_city_names(df, city_column):\n    """Standardize city names"""\n    # Implementation will be migrated from data_processing.py\n    pass\n\ndef standardize_course_names(df, course_column):\n    """Standardize course names"""\n    # Implementation will be migrated from data_processing.py\n    pass\n',
        
        # Static JS files
        'app/static/js/charts/config.js': '/**\n * Highcharts base configuration\n */\nfunction initHighchartsConfig() {\n    // Base configuration will be migrated from main.js\n    Highcharts.setOptions({\n        // Configuration options\n    });\n}\n',
        'app/static/js/charts/plugins.js': '/**\n * Custom Highcharts plugins and extensions\n */\n\n// Export functionality\nfunction initExportFeatures() {\n    // Implementation will be migrated from main.js\n}\n\n// Accessibility features\nfunction initAccessibilityFeatures() {\n    // Implementation will be migrated from main.js\n}\n',
        'app/static/js/utils/export.js': '/**\n * Export utilities\n */\n\n// Export all charts as ZIP\nfunction exportAllCharts() {\n    // Implementation will be migrated from main.js\n}\n\n// Export single chart\nfunction exportChart(chart, filename) {\n    // Implementation will be migrated from main.js\n}\n',
        'app/static/js/utils/accessibility.js': '/**\n * Accessibility utilities\n */\n\n// Toggle colorblind mode\nfunction toggleColorBlindMode(enable) {\n    // Implementation will be migrated from main.js\n}\n\n// Check if colorblind mode is enabled\nfunction isColorBlindModeEnabled() {\n    // Implementation will be migrated from main.js\n    return localStorage.getItem("colorBlindMode") === "true";\n}\n',
        
        # CSS files
        'app/static/css/print.css': '/**\n * Print styles\n */\n@media print {\n    /* Print styles will be migrated from style.css */\n    body {\n        background-color: white !important;\n    }\n    \n    header, footer, .sidebar, .card-header, form, .btn {\n        display: none !important;\n    }\n    \n    .card {\n        box-shadow: none !important;\n        border: none !important;\n    }\n    \n    .chart-container {\n        break-inside: avoid !important;\n    }\n}\n',
        
        # Template files
        'app/templates/base/header.html': '<!-- Header template -->\n<header>\n    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">\n        <div class="container">\n            <a class="navbar-brand" href="{{ url_for(\'upload.home\') }}">\n                <i class="fas fa-chart-bar"></i> Análise Socioeconômica FATEC\n            </a>\n            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">\n                <span class="navbar-toggler-icon"></span>\n            </button>\n            <!-- Navigation will be migrated from base.html -->\n        </div>\n    </nav>\n</header>\n',
        'app/templates/base/footer.html': '<!-- Footer template -->\n<footer class="bg-light py-3 mt-5">\n    <div class="container text-center">\n        <p class="mb-0">Desenvolvido para análise de dados socioeconômicos dos estudantes da FATEC - 2025</p>\n    </div>\n</footer>\n',

        # Main app file
        'app/app.py': '#!/usr/bin/env python3\nfrom flask import Flask, render_template\nimport os\nimport logging\nfrom config.settings import config\nfrom routes import dashboard_bp, upload_bp, api_bp\nfrom utils.file_handlers import create_directories\n\n# Configure logging\nlogging.basicConfig(\n    level=logging.INFO,\n    format=\'%(asctime)s - %(name)s - %(levelname)s - %(message)s\',\n    handlers=[\n        logging.FileHandler(\'app.log\'),\n        logging.StreamHandler()\n    ]\n)\nlogger = logging.getLogger(__name__)\n\ndef create_app(config_name=\'default\'):\n    """Factory function to create the Flask application"""\n    # Create Flask application\n    app = Flask(__name__)\n    \n    # Load configuration\n    app.config.from_object(config[config_name])\n    \n    # Initialize app with configuration\n    config[config_name].init_app(app)\n    \n    # Register blueprints\n    app.register_blueprint(upload_bp, url_prefix=\'/\')\n    app.register_blueprint(dashboard_bp, url_prefix=\'/dashboard\')\n    app.register_blueprint(api_bp, url_prefix=\'/api\')\n    \n    # Register error handlers\n    @app.errorhandler(404)\n    def page_not_found(e):\n        logger.warning(f"404 error: {request.path}")\n        return render_template(\'errors/404.html\'), 404\n\n    @app.errorhandler(500)\n    def server_error(e):\n        logger.error(f"500 error: {str(e)}")\n        return render_template(\'errors/500.html\'), 500\n    \n    return app\n\nif __name__ == \'__main__\':\n    logger.info("Starting application")\n    create_directories()\n    app = create_app(os.environ.get(\'FLASK_ENV\', \'default\'))\n    app.run(debug=True)\n'
    }
    
    for file_path, content in new_files.items():
        path = os.path.join(base_dir, file_path)
        # Ensure directory exists
        dir_path = os.path.dirname(path)
        os.makedirs(dir_path, exist_ok=True)
        
        # Create file
        with open(path, 'w') as f:
            f.write(content)
        print(f"Created new file: {path}")

def main():
    # Get current directory
    current_dir = os.getcwd()
    
    # Target directory for refactored project
    refactored_dir = os.path.join(current_dir, 'refactored_project')
    
    # Create refactored directory structure
    print(f"Creating refactored project structure in: {refactored_dir}")
    create_directory_structure(refactored_dir)
    
    # Create __init__.py files
    create_init_files(refactored_dir)
    
    # Migrate existing files
    migrate_existing_files(refactored_dir, current_dir)
    
    # Create new files
    create_new_files(refactored_dir)
    
    print("\nRefactoring completed!")
    print(f"The refactored project structure has been created in: {refactored_dir}")
    print("\nNext steps:")
    print("1. Review the migrated files and complete the implementation of placeholders")
    print("2. Update imports and references in the migrated files")
    print("3. Set up a virtual environment and install dependencies")
    print("4. Test the refactored application")

if __name__ == "__main__":
    main()
