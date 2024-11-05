from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..models import User
from .. import db

bp = Blueprint('funcionarios', __name__, url_prefix='/funcionarios')

@bp.route('', methods=['GET'])
@jwt_required()
def get_funcionarios():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@bp.route('/cadastrar', methods=['POST', 'PUT'])
def cadastrar_funcionario():
    data = request.json
    password = data.get('password')
    if not password:
        return jsonify({"error": "Password must be provided"}), 400

    if request.method == 'POST':
        user = User(
            nome=data.get('nome'),
            sobrenome=data.get('sobrenome'),
            email=data.get('email'),
            cargo=data.get('cargo'),
            role_id=data.get('role')
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201

    elif request.method == 'PUT':
        user_id = data.get('id')
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        user.nome = data.get('nome', user.nome)
        user.sobrenome = data.get('sobrenome', user.sobrenome)
        user.email = data.get('email', user.email)
        user.cargo = data.get('cargo', user.cargo)
        user.role_id = data.get('role', user.role_id)
        user.set_password(password)
        db.session.commit()
        return jsonify(user.to_dict()), 200

@bp.route('/', methods=['GET'])
@jwt_required()
def get_funcionarios_by_name():
    nome = request.args.get('nome')
    if not nome:
        return jsonify({"error": "Nome must be provided"}), 400

    nome_param = f"%{nome}%"

    users = User.query.filter(User.nome.ilike(nome_param) | User.sobrenome.ilike(nome_param)).all()

    return jsonify([user.to_dict() for user in users]), 200