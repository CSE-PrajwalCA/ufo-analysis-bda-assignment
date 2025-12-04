"""
UFO Dashboard - Configuration
Centralized configuration for the application
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================
# MongoDB Configuration
# ============================================================

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
DB_NAME = os.getenv('DB_NAME', 'ufo_database')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'sightings')

# ============================================================
# Flask Configuration
# ============================================================

FLASK_ENV = os.getenv('FLASK_ENV', 'development')
FLASK_DEBUG = os.getenv('FLASK_DEBUG', True)
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# ============================================================
# Server Configuration
# ============================================================

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))

# ============================================================
# Application Settings
# ============================================================

MAX_RECORDS_PER_QUERY = 10000
MAX_RECORDS_FOR_PDF_EXPORT = 100
BATCH_INSERT_SIZE = 1000

# ============================================================
# Display Settings
# ============================================================

CHARTS_PER_ROW = 2
DEFAULT_CHART_HEIGHT = 400

# ============================================================
# CSV Export Settings
# ============================================================

CSV_FIELD_ORDER = [
    'datetime',
    'city',
    'state',
    'country',
    'shape',
    'duration (seconds)',
    'duration (hours/min)',
    'comments',
    'date posted',
    'latitude',
    'longitude'
]

# ============================================================
# Validation Settings
# ============================================================

MIN_YEAR = 1900
MAX_YEAR = 2100
MIN_DURATION = 0
MAX_DURATION = 999999
