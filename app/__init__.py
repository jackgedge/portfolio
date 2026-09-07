from flask import Flask
from .routes import main_bp, dev_bp, social_bp

def portfolio():
    app = Flask(__name__)
    app.register_blueprint(main_bp)
    app.register_blueprint(dev_bp)
    app.register_blueprint(social_bp)

    return app