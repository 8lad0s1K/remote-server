from pathlib import Path
from dotenv import load_dotenv
import os

# Коренева папка сервера
BASE_DIR = Path(__file__).resolve().parent

# Завантаження .env
load_dotenv(BASE_DIR / ".env")

# База даних
DATABASE_PATH = BASE_DIR / "database" / "licenses.db"

# SQLAlchemy
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# API
API_NAME = "REMOTE SERVER"
API_VERSION = "1.0.0"

# Heartbeat
HEARTBEAT_SECONDS = 30

# Логи
LOGS_DIR = BASE_DIR / "logs"

# Security
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "REMOTE_SECRET_KEY_2026"
)