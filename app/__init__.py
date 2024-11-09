from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .config import Config

db = SQLAlchemy()

def create_app(config=None):
    app = Flask(__name__)
    
    if config is None:
        app.config.from_object(Config)
    else:
        app.config.update(config)

    db.init_app(app)
    JWTManager(app)
    CORS(app)

    
    with app.app_context():
        from .routes import register_blueprints
        register_blueprints(app)
        
        db.create_all()
    
    return app

