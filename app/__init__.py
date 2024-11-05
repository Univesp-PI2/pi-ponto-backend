from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

        print(f"SQLALCHEMY_DATABASE_URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print(f"SECRET_KEY: {app.config['SECRET_KEY']}")
    
    db.init_app(app)
    JWTManager(app)
    CORS(app)

    
    with app.app_context():
        from .routes import register_blueprints
        register_blueprints(app)
        
        db.create_all()
    
    return app

