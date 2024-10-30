from flask import Blueprint, request, jsonify
from ..models import User
from .. import db

bp = Blueprint('funcionarios', __name__, url_prefix='/funcionarios')

@bp.route('/', methods=['GET'])
def get_funcionarios():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@bp.route('/cadastrar', methods=['POST'])
def cadastrar_funcionario():
    data = request.json
    user = User(
        nome=data.get('nome'),
        sobrenome=data.get('sobrenome'),
        email=data.get('email'),
        cargo=data.get('cargo'),
        role_id=data.get('role')
    )
    user.set_password(data.get('password'))
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Usuário salvo com sucesso'}), 200
