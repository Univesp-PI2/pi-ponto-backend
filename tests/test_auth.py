def test_login_successo(client):
    # Dados de login válidos
    login_data = {
        'email': 'johnathan@exemplo.com',
        'password': 'password123'
    }
    response = client.post('/login', json=login_data)
    assert response.status_code == 200
    assert 'accessToken' in response.json
    assert response.json['message'] == 'Usuário logado com sucesso'

def test_login_password_invalido(client):
    # Dados de login com senha inválida
    login_data = {
        'email': 'johnathan@exemplo.com',
        'password': 'passworderrado'
    }
    response = client.post('/login', json=login_data)
    assert response.status_code == 401
    assert response.json['message'] == 'Usuário e/ou senha inválidos'

def test_login_email_invalido(client):
    # Dados de login com email inválido
    login_data = {
        'email': 'jonatas@exemplo.com',
        'password': 'password123'
    }
    response = client.post('/login', json=login_data)
    assert response.status_code == 401
    assert response.json['message'] == 'Usuário e/ou senha inválidos'

def test_login_campos_faltantes(client):
    # Dados de login faltando campos
    login_data = {
        'email': 'johnathan@exemplo.com'
    }
    response = client.post('/login', json=login_data)
    assert response.status_code == 400
    assert response.json['msg'] == 'Email ou senha não informados'

    login_data = {
        'password': 'password123'
    }
    response = client.post('/login', json=login_data)
    assert response.status_code == 400
    assert response.json['msg'] == 'Email ou senha não informados'