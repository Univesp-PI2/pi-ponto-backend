from datetime import datetime

def test_registro_options(client, auth_headers):
    response = client.options('/registro/', headers=auth_headers)
    assert response.status_code == 200
    assert response.json['message'] == 'Options request successful'

def test_salvar_registro(client, auth_headers):
    # Teste com data válida
    valid_data = {
        'funcionario': 1,
        'dia': '2023-10-10',
        'campo_tempo': 'entrada',
        'valor_tempo': '08:00:00'
    }
    response = client.post('/registro/salvar', json=valid_data, headers=auth_headers)
    print("Response:", response.json)
    assert response.status_code == 200
    assert response.json['message'] == 'Tempo salvo com sucesso'

    # Teste com data inválida
    invalid_data = {
        'funcionario': 1,
        'dia': '2023-10-10',
        'campo_tempo': 'entrada'
    }
    response = client.post('/registro/salvar', json=invalid_data, headers=auth_headers)
    assert response.status_code == 400
    assert response.json['error'] == 'Por favor, forneça todos os campos'

    # Teste com campo_tempo inválido
    invalid_data = {
        'funcionario': 1,
        'dia': '2023-10-10',
        'campo_tempo': 'invalid',
        'valor_tempo': '08:00:00'
    }
    response = client.post('/registro/salvar', json=invalid_data, headers=auth_headers)
    assert response.status_code == 400
    assert response.json['error'] == 'Campo campo_tempo inválido. Deve ser entrada, intervalo, retorno ou saida'

def test_get_registros_by_funcionario(client, auth_headers):
    user_id = 1
    response = client.get(f'/registro/{user_id}', headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_registro_by_funcionario_and_periodo(client, auth_headers):
    # Teste válido com user_id e período
    response = client.get('/registro/?periodo=2023-10-01,2023-10-31', headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json, list)

    # Teste inválido sem período
    response = client.get('/registro/', headers=auth_headers)
    assert response.status_code == 400
    assert response.json['error'] == 'Por favor, forneça todos os campos'