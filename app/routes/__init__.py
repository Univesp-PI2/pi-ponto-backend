from .auth import bp as auth_bp
from .funcionarios import bp as funcionarios_bp
from .registros import bp as registros_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(funcionarios_bp)
    app.register_blueprint(registros_bp)