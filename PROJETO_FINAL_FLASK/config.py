import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    """Base configuration class"""
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fatec-socioeconomico-2025')
    
    # Upload configuration
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    DATABASE_FOLDER = os.path.join(os.getcwd(), 'database')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size
    
    # Ensure directories exist
    @staticmethod
    def init_app(app):
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        os.makedirs(app.config['DATABASE_FOLDER'], exist_ok=True)

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    
    # In production, use a proper secret key
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}