import json
import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()
BASE_DIR = Path(__file__).resolve().parents[3]

# Директория для сгенерированного сайта
DIST_DIR = BASE_DIR / "dist"

TEMPLATES_DIR = BASE_DIR / "apps" / "templates"

# PandaScore
PANDASCORE_API_URL: str = os.getenv("PANDASCORE_API_URL")
PANDASCORE_API_TOKEN: str = os.getenv("PANDASCORE_API_TOKEN", "")

if not PANDASCORE_API_TOKEN:
    raise RuntimeError("PANDASCORE_API_TOKEN is not set in environment")

# Базовый URL сайта (домен или IP)
SITE_BASE_URL: str = os.getenv("SITE_BASE_URL", "").rstrip("/")

if not SITE_BASE_URL:
    raise RuntimeError("SITE_BASE_URL is not set in environment")


TIMEZONE: str = os.getenv("SITE_TIMEZONE", "UTC")

# Формат дат для API
DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

DISCIPLINES_FILE = BASE_DIR / "apps" / "site_generator" / "config" / "disciplines.json"

with open(DISCIPLINES_FILE, "r", encoding="utf-8") as f:
    DISCIPLINES = json.load(f)

MEDIA_STATIC = BASE_DIR / "media" / "static"

PLACEHOLDER_LOGO = "/static/team_placeholder_logo.webp"