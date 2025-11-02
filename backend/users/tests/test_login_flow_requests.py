import requests
import pytest
import time

BASE_URL = "https://xbpneus-backend.onrender.com"

# Dados para os testes
TRANSPORTADOR_REGISTER_DATA = {
    "email": "transportador_test_new@example.com",
    "password": "Test@12345",
    "password2": "Test@12345",
    "tipo_usuario": "transportador",
    "nome_razao_social": "Transportador Teste Novo",
    "cnpj": "11223344556678",
    "telefone": "11911112223"
}

MOTORISTA_REGISTER_DATA = {
    "email": "motorista_test_new@example.com",
    "password": "Test@12345",
    "password2": "Test@12345",
    "tipo_usuario": "motorista",
    "nome_completo": "Motorista Teste Novo",
    "cpf": "12345678902",
    "cnh": "12345678903",
    "categoria_cnh": "B",
    "telefone": "11933334445"
}

ADMIN_LOGIN_DATA = {
    "email": "catanharacing@gmail.com",
    "password": "fer69@HOTMAIL"
}

@pytest.fixture(scope="module")
def admin_token():
    response = requests.post(f"{BASE_URL}/api/token/", json=ADMIN_LOGIN_DATA)
    if response.status_code == 200:
        return response.json()["access"]
    else:
        pytest.fail(f"Falha ao obter token de admin: {response.status_code} - {response.json()}")

def test_1_register_new_transportador():
    response = requests.post(f"{BASE_URL}/api/users/register_full/", json=TRANSPORTADOR_REGISTER_DATA)
    assert response.status_code == 201, f"Erro no cadastro do transportador: {response.json()}"
    assert "message" in response.json()
    assert "Cadastro realizado com sucesso! Aguarde aprovação do administrador." in response.json()["message"]

def test_2_register_new_motorista():
    response = requests.post(f"{BASE_URL}/api/users/register_full/", json=MOTORISTA_REGISTER_DATA)
    assert response.status_code == 201, f"Erro no cadastro do motorista: {response.json()}"
    assert "message" in response.json()
    assert "Cadastro realizado com sucesso! Aguarde aprovação do administrador." in response.json()["message"]

def test_3_admin_approve_transportador(admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = requests.post(f"{BASE_URL}/api/approve-user-by-email/", json={
        "email": TRANSPORTADOR_REGISTER_DATA["email"]
    }, headers=headers)
    assert response.status_code == 200, f"Falha na aprovação do transportador: {response.json()}"
    assert "message" in response.json()
    assert "aprovado com sucesso!" in response.json()["message"]

def test_4_admin_approve_motorista(admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = requests.post(f"{BASE_URL}/api/approve-user-by-email/", json={
        "email": MOTORISTA_REGISTER_DATA["email"]
    }, headers=headers)
    assert response.status_code == 200, f"Falha na aprovação do motorista: {response.json()}"
    assert "message" in response.json()
    assert "aprovado com sucesso!" in response.json()["message"]

def test_5_login_transportador_aprovado():
    login_data = {
        "email": TRANSPORTADOR_REGISTER_DATA["email"],
        "password": TRANSPORTADOR_REGISTER_DATA["password"]
    }
    response = requests.post(f"{BASE_URL}/api/token/", json=login_data)
    assert response.status_code == 200, f"Falha no login do transportador: {response.json()}"
    assert "access" in response.json()

def test_6_login_motorista_aprovado():
    login_data = {
        "email": MOTORISTA_REGISTER_DATA["email"],
        "password": MOTORISTA_REGISTER_DATA["password"]
    }
    response = requests.post(f"{BASE_URL}/api/token/", json=login_data)
    assert response.status_code == 200, f"Falha no login do motorista: {response.json()}"
    assert "access" in response.json()

def test_7_login_existing_transportador():
    login_data = {
        "email": "transportador.teste2@xbpneus.com",
        "password": "Teste@2025"
    }
    response = requests.post(f"{BASE_URL}/api/token/", json=login_data)
    assert response.status_code == 200, f"Falha no login do transportador existente: {response.json()}"
    assert "access" in response.json()

