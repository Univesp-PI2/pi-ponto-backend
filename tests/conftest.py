import pytest
import random
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError as SQLAlchemyOperationalError
from sqlalchemy.pool import StaticPool
from app import create_app, db
from app.models import User, Role


def pytest_addoption(parser):
    parser.addoption(
        "--dburl",  # Utilizar outra string de conexão
        action="store",
        default="sqlite:///:memory:",  # Pot padrão, utiliza o SQLite in-memory database
        help="URL do Banco de Dados para testes",
    )

@pytest.fixture
def client():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'super-secret',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })
    with app.app_context():
        db.create_all()
        if not Role.query.filter_by(role_name='admin').first():
            admin = Role(role_name='admin')
            db.session.add(admin)
        if not Role.query.filter_by(role_name='user').first():
            user_role = Role(role_name='user')
            db.session.add(user_role)
        db.session.commit()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="session")
def db_url(request):
    """Fixture fixture para retornar a URL de BD."""
    return request.config.getoption("--dburl")


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    db_url = session.config.getoption("--dburl")
    try:
        # Tenta criar uma engine e conecta com o bando de dados.
        engine = create_engine(
            db_url,
            poolclass=StaticPool,
        )
        connection = engine.connect()
        connection.close()  # Fecha a conexão após uma conecão bem sucedida
        print("Database URL:", db_url)
        print("Conectado com sucesso.....")
    except SQLAlchemyOperationalError as e:
        print(f"Falha ao conectar ao bando de dados {db_url}: {e}")
        pytest.exit(
            "Encerrando testes porque a conexão com o banco de dados não pôde ser estabelecida."
        )


@pytest.fixture(scope="session")
def app(db_url):
    """Fixture de 'app' para testes de toda a sessão."""
    test_config = {
        "SQLALCHEMY_DATABASE_URI": db_url,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }
    app = create_app(test_config)

    with app.app_context():
        db.create_all()
        yield app

        # Encerra a sessão do banco de dados e exclui todas as tabelas após a sessão
        db.session.remove()
        db.drop_all()


@pytest.fixture
def test_client(app):
    """Client de testes para app."""
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    with client.application.app_context():
        # Inserindo um usuário diretamente no banco de dados
        # Apesar de não ser a melhor prática, é útil para testes
        user = User(
            nome='Jonathan',
            sobrenome='Lucas',
            email='johnathan.doe@example.com',
            cargo='Tester',
            role_id=1  # ID do role de adminidtrador (admin)
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

        # Now login the user to get the auth token
        # Logando o usuário para obter o token de autenticação
        login_data = {
            'email': 'johnathan.doe@example.com',
            'password': 'password123'
        }
        response = client.post('/login', json=login_data)

        access_token = response.json.get('accessToken')

        return {'Authorization': f'Bearer {access_token}'}