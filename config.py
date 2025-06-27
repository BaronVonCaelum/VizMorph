"""
VizMorph Configuration
Contains configuration settings for the application
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
UPLOAD_FOLDER = BASE_DIR / 'uploads'
STATIC_FOLDER = BASE_DIR / 'static'
TEMPLATES_FOLDER = BASE_DIR / 'templates'

# Flask Configuration
class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'vizmorph-secret-key-change-in-production'
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size
    UPLOAD_FOLDER = str(UPLOAD_FOLDER)
    STATIC_FOLDER = str(STATIC_FOLDER)
    TEMPLATES_FOLDER = str(TEMPLATES_FOLDER)
    
    # API Configuration
    API_VERSION = 'v1'
    API_PREFIX = '/api'
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FILE = BASE_DIR / 'logs' / 'vizmorph.log'
    
    # Tableau Parser Configuration
    SUPPORTED_EXTENSIONS = ['.twb', '.twbx']
    CACHE_SIZE = 100  # Maximum number of workbooks to cache
    
    # Visualization Configuration
    DEFAULT_CHART_WIDTH = 800
    DEFAULT_CHART_HEIGHT = 400
    CONFIDENCE_THRESHOLD = 0.5  # Minimum confidence score for suggestions
    MAX_SUGGESTIONS = 10  # Maximum number of suggestions per workbook

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError('SECRET_KEY environment variable must be set in production')

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # 1MB for testing

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# Heuristic Rules Configuration
HEURISTIC_RULES = {
    'too_many_categories': {
        'enabled': True,
        'category_threshold': 10,
        'keywords': ['id', 'name', 'code', 'product']
    },
    'time_series_opportunity': {
        'enabled': True,
        'temporal_keywords': ['date', 'time', 'year', 'month', 'day', 'quarter']
    },
    'correlation_opportunity': {
        'enabled': True,
        'min_measures': 2
    },
    'distribution_analysis': {
        'enabled': True,
        'suggest_histogram': True,
        'suggest_boxplot': True
    },
    'part_to_whole': {
        'enabled': True,
        'max_categories': 8
    },
    'hierarchical_data': {
        'enabled': True,
        'hierarchical_keywords': ['category', 'subcategory', 'region', 'country', 'state', 'city']
    },
    'multiple_measures': {
        'enabled': True,
        'threshold': 3
    },
    'geographic_data': {
        'enabled': True,
        'geo_keywords': ['country', 'state', 'city', 'region', 'latitude', 'longitude', 'zip', 'postal']
    },
    'performance_comparison': {
        'enabled': True,
        'performance_keywords': ['sales', 'revenue', 'profit', 'performance', 'score', 'rating']
    }
}

# D3.js Template Configuration
D3_CONFIG = {
    'default_width': 800,
    'default_height': 400,
    'default_margin': {'top': 20, 'right': 30, 'bottom': 40, 'left': 40},
    'color_schemes': {
        'categorical': 'category10',
        'sequential': 'Blues',
        'diverging': 'RdYlBu'
    },
    'supported_formats': ['json', 'd3', 'vega-lite']
}

# Electron Configuration
ELECTRON_CONFIG = {
    'window': {
        'width': 1200,
        'height': 800,
        'min_width': 800,
        'min_height': 600
    },
    'api_base_url': 'http://localhost:5000',
    'auto_start_server': False
}

# Validation Rules
VALIDATION_RULES = {
    'file_upload': {
        'max_size': 50 * 1024 * 1024,  # 50MB
        'allowed_extensions': ['.twb', '.twbx'],
        'scan_for_malware': False
    },
    'suggestion_generation': {
        'max_suggestions': 10,
        'min_confidence': 0.3,
        'timeout_seconds': 30
    }
}

def get_config(config_name=None):
    """Get configuration based on environment or provided name"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    return config.get(config_name, config['default'])

def ensure_directories():
    """Ensure all required directories exist"""
    directories = [
        UPLOAD_FOLDER,
        STATIC_FOLDER,
        BASE_DIR / 'logs'
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

# Initialize directories when module is imported
ensure_directories()
