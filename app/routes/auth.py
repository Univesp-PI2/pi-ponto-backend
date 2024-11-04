from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from ..models import User, Role
from .. import db

bp = Blueprint('auth', __name__, url_prefix='/login')

@bp.route('', methods=['POST'])
def login():
    data = request.json
    print(data)
    if not data or not 'email' in data or not 'password' in data:
        return jsonify({"msg": "Missing email or password"}), 400
    
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        print(user.check_password(password))
        role = Role.query.get(user.role_id).role_name
        access_token = create_access_token(identity={'id': user.id, 'role': role})
        print(access_token)
        return jsonify({'message': 'Usuário logado com sucesso', 'success': True, 'accessToken': access_token, 'role': role, 'id': user.id, 'nome': user.nome }), 200
    return jsonify({'message': 'Usuário e/ou senha inválidos'}), 401
