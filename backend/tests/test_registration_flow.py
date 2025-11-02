
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

# O modelo de usuário principal é UsuarioTransportador, conforme AUTH_USER_MODEL
User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_register_transportador_success(api_client):
    initial_user_count = User.objects.count()

    data = {
        "tipo_usuario": "transportador", # Este campo pode ser ignorado se o registro for direto para UsuarioTransportador
        "email": "novo.transportador@teste.com",
        "password": "Senha@123",
        "nome_razao_social": "Novo Transportador Teste",
        "cnpj": "11223344000155",
        "telefone": "(99) 99999-9999"
    }
    # Assumindo que o endpoint /api/register/ é o register_full_view que lida com diferentes tipos
    response = api_client.post("/api/users/register_full/", data, format="json")

    assert response.status_code == 201
    assert "Cadastro realizado com sucesso! Aguarde aprovação do administrador." in response.data["message"]
    assert User.objects.count() == initial_user_count + 1

    new_user = User.objects.get(email="novo.transportador@teste.com")
    assert not new_user.is_active  # Deve estar inativo até aprovação
    assert not new_user.aprovado # Deve estar não aprovado até aprovação
    assert new_user.nome_razao_social == "Novo Transportador Teste"
    assert new_user.cnpj == "11223344000155"

@pytest.mark.django_db
def test_register_transportador_email_exists(api_client):
    User.objects.create_user(
        email="existente.transportador@teste.com",
        password="Senha@123",
        nome_razao_social="Transportador Existente",
        cnpj="99887766000111",
        telefone="(88) 88888-8888",
        is_active=True,
        aprovado=True
    )

    data = {
        "tipo_usuario": "transportador",
        "email": "existente.transportador@teste.com",
        "password": "OutraSenha@456",
        "nome_razao_social": "Outro Transportador",
        "cnpj": "11122233000144",
        "telefone": "(77) 77777-7777"
    }
    response = api_client.post("/api/users/register_full/", data, format="json")

    assert response.status_code == 400
    assert "Email já cadastrado" in response.data["error"]

@pytest.mark.django_db
def test_register_transportador_missing_fields(api_client):
    data = {
        "tipo_usuario": "transportador",
        "email": "incompleto.transportador@teste.com",
        "password": "Senha@123",
        # Faltando nome_razao_social, cnpj, telefone
    }
    response = api_client.post("/api/users/register_full/", data, format="json")

    assert response.status_code == 400
    assert "Campos obrigatórios faltando" in response.data["error"]
    assert "nome_razao_social" in response.data["campos_faltando"]
    assert "cnpj" in response.data["campos_faltando"]
    assert "telefone" in response.data["campos_faltando"]

@pytest.mark.django_db
def test_register_transportador_cnpj_exists(api_client):
    User.objects.create_user(
        email="transportador.cnpj@teste.com",
        password="Senha@123",
        nome_razao_social="Transportador CNPJ Existente",
        cnpj="11223344000155", # CNPJ que já vai ser usado no teste
        telefone="(88) 88888-8888",
        is_active=True,
        aprovado=True
    )

    data = {
        "tipo_usuario": "transportador",
        "email": "novo.transportador2@teste.com",
        "password": "Senha@123",
        "nome_razao_social": "Novo Transportador Teste 2",
        "cnpj": "11223344000155", # CNPJ duplicado
        "telefone": "(99) 99999-9999"
    }
    response = api_client.post("/api/users/register_full/", data, format="json")

    assert response.status_code == 400
    assert "CNPJ já cadastrado" in response.data["error"]

