# apps/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Initialize SQLAlchemy (without attaching to app yet)
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize the db with the app
    db.init_app(app)
    
    # Register blueprints
    from apps.controllers.auth_controller import auth_blurprint, verify_otp_blueprint
    from apps.controllers.matches_controller import fetch_matches_blueprint
    
    app.register_blueprint(auth_blurprint)
    app.register_blueprint(fetch_matches_blueprint)
    app.register_blueprint(verify_otp_blueprint)
    
    return app
