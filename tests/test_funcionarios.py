def test_cadastrar_funcionario_post(client):
    data = {
        'nome': 'Marcos',
        'sobrenome': 'Rodrigues',
        'email': 'marcos@examplo.com',
        'password': 'password123',
        'cargo': 'Desenvolvedor',
        'role': 2  # ID do role de usuário (user)
    }
    response = client.post('/funcionarios/cadastrar', json=data)
    assert response.status_code == 201
    assert response.json['nome'] == 'Marcos'
    assert response.json['email'] == 'marcos@examplo.com'

def test_get_funcionarios(client, auth_headers):
    response = client.get('/funcionarios', headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_cadastrar_funcionario_put(client):
    # Primeiro, cria um usuário
    data = {
        'nome': 'Marcela',
        'sobrenome': 'Rodrigues',
        'email': 'marcela@examplo.com',
        'cargo': 'Gerente',
        'role': 1,  # ID do role de adminidtrador (admin)
        'password': 'password123'
    }
    response = client.post('/funcionarios/cadastrar', json=data)
    assert response.status_code == 201
    user_id = response.json['id']

    # NDepois, atualiza o usuário
    update_data = {
        'id': user_id,
        'nome': 'Marcela',
        'sobrenome': 'Rodrigues da Silva', 
        'email': 'marcela.silvad@examplo.com',
        'cargo': 'Gerente',
        'role': 1,  # ID do role de adminidtrador (admin)
        'password': 'newpassword123'
    }
    response = client.put('/funcionarios/cadastrar', json=update_data)
    assert response.status_code == 200
    assert response.json['sobrenome'] == 'Rodrigues da Silva'
    assert response.json['email'] == 'marcela.silvad@examplo.com'

def test_get_funcionarios_by_name(client, auth_headers):
    response = client.get('/funcionarios', headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json, list)