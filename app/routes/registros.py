from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..models import Ponto, User
from sqlalchemy import and_
from .. import db

bp = Blueprint('registros', __name__, url_prefix='/registro')

@bp.route('/', methods=['OPTIONS'])
@jwt_required()
def registro_options():
    response = jsonify({'message': 'Options request successful'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    return response, 200

@bp.route('/salvar', methods=['POST'])
@jwt_required()
def salvar_registro():

    data = request.json

    user = data.get('funcionario')
    dia = data.get('dia')
    campo_tempo = data.get('campo_tempo')
    valor_tempo = data.get('valor_tempo')

    if not all([user, dia, campo_tempo, valor_tempo]):
        return jsonify({'error': 'Por favor, forneça todos os campos'}), 400

    if campo_tempo not in ['entrada', 'intervalo', 'retorno', 'saida']:
        return jsonify({'error': 'Campo campo_tempo inválido. Deve ser entrada, intervalo, retorno ou saida'}), 400

    try:
        ponto = Ponto.query.filter_by(user_id=user, data=dia).first()
        if not ponto:
            ponto = Ponto(user_id=user, data=dia)
            db.session.add(ponto)
        
        setattr(ponto, campo_tempo, valor_tempo)
        db.session.commit()
        return jsonify({'message': 'Tempo salvo com sucesso'}), 200

    except Exception as error:
        db.session.rollback()
        return jsonify({'error': f'Erro ao salvar tempo: {error}'}), 500

@bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_registros_by_funcionario(user_id):
    try:

        query = db.session.query(Ponto).filter(Ponto.user_id == user_id)
        registros = query.all()

        registros_json = []

        for registro in registros:
            registros_json.append({
                'id': registro.id,
                'funcionario': registro.user_id,
                'dia': registro.data.strftime('%Y-%m-%d') if registro.data else None,
                'entrada': registro.entrada.strftime('%H:%M:%S') if registro.entrada else None,
                'intervalo': registro.intervalo.strftime('%H:%M:%S') if registro.intervalo else None,
                'retorno': registro.retorno.strftime('%H:%M:%S') if registro.retorno else None,
                'saida': registro.saida.strftime('%H:%M:%S') if registro.saida else None
            })
        
        return jsonify(registros_json), 200

    except Exception as error:
        return jsonify({'error': f'Erro ao obter registros: {error}'}), 500

@bp.route('/', methods=['GET'])
@jwt_required()
def registro_by_funcionario_and_periodo():
    periodo = request.args.get('periodo')
    funcionario = request.args.get('funcionario')


    if not periodo:
        return jsonify({'error': 'Por favor, forneça todos os campos'}), 400

    try:
        query = db.session.query(Ponto, User).join(User, Ponto.user_id == User.id)


        if funcionario:
            funcionario_param = f"%{funcionario}%"
            query = query.filter(
                (User.nome.ilike(funcionario_param) | User.sobrenome.ilike(funcionario_param))
            ).filter(
                and_(Ponto.data.between(periodo.split(',')[1], periodo.split(',')[0]))
            )
        else:
            query = query.filter(
                Ponto.data.between(periodo.split(',')[1], periodo.split(',')[0])
            )
            print(query)

        registros = query.all()
        print(registros)

        registros_json = []

        for ponto, user in registros:
            registros_json.append({
                'dia': ponto.data.strftime('%d/%m/%Y') if ponto.data else None,
                'funcionario': f"{user.nome} {user.sobrenome}",
                'entrada': ponto.entrada.strftime('%H:%M:%S') if ponto.entrada else None,
                'intervalo': ponto.intervalo.strftime('%H:%M:%S') if ponto.intervalo else None,
                'retorno': ponto.retorno.strftime('%H:%M:%S') if ponto.retorno else None,
                'saida': ponto.saida.strftime('%H:%M:%S') if ponto.saida else None
            })

        return jsonify(registros_json), 200

    except Exception as error:
        return jsonify({'error': f'Erro ao obter registros: {error}'}), 500
