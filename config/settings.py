import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Database
DATABASE_PATH = os.path.join(BASE_DIR, "database", "contracts.db")

# Data files
BASE_DADOS_PATH = os.path.join(BASE_DIR, "BASE_DADOS.xlsx")

# Application settings
APP_NAME = "Gerador de Contratos KML"
APP_VERSION = "2.0"

# UI Configuration
THEME_COLOR = "#2196F3"
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600

# Logging
LOG_FILE = os.path.join(BASE_DIR, "app.log")
LOG_LEVEL = "INFO"

# Cache settings
CACHE_ENABLED = True
CACHE_TIMEOUT = 3600  # 1 hour
