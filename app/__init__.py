from flask import Flask
from .routes import main_bp

def portfolio():
    app = Flask(__name__)
    app.register_blueprint(main_bp)

    return app