from flask import Flask
from pathlib import Path
from flask.cli import load_dotenv
import os

# Define project directory and environment file location.
PROJECT_DIR: Path = Path(__file__).resolve().parent.parent
ENV_FILE: Path = PROJECT_DIR / ".env"

# Load environment variables
load_dotenv(ENV_FILE)

PORTFOLIO_DIR: str | None = os.getenv('PORTFOLIO_DIR')
THUMBNAIL_DIR = ".thumbnails"

IMAGE_FORMATS: list[str] = [
    ".jpg",
    ".jpeg",
    ]

from .routes import main_bp, dev_bp, social_bp

def portfolio():
    app = Flask(__name__)
    app.register_blueprint(main_bp)
    app.register_blueprint(dev_bp)
    app.register_blueprint(social_bp)

    return app