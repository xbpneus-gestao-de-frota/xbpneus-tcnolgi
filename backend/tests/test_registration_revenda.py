
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from backend.revenda.models import UsuarioRevenda

# O modelo de usuário principal para revendas é UsuarioRevenda

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_register_revenda_success(api_client):
    initial_user_count = UsuarioRevenda.objects.count()

    data = {
        "tipo_usuario": "revenda",
        "email": "nova.revenda@teste.com",
        "password": "Senha@123",
        "nome_razao_social": "Nova Revenda Teste",
        "cnpj": "55443322000199",
        "telefone": "(99) 99999-9999"
    }
    response = api_client.post("/api/users/register_full/", data, format="json")

    assert response.status_code == 201
    assert "Cadastro realizado com sucesso! Aguarde aprovação do administrador." in response.data["message"]
    assert UsuarioRevenda.objects.count() == initial_user_count + 1

    new_revenda = UsuarioRevenda.objects.get(email="nova.revenda@teste.com")
    assert not new_revenda.is_active  # Deve estar inativo até aprovação
    assert not new_revenda.aprovado # Deve estar não aprovado até aprovação
    assert new_revenda.nome_razao_social == "Nova Revenda Teste"
    assert new_revenda.cnpj == "55443322000199"

@pytest.mark.django_db
def test_register_revenda_email_exists(api_client):
    UsuarioRevenda.objects.create_user(
        email="existente.revenda@teste.com",
        password="Senha@123",
        nome_razao_social="Revenda Existente",
        cnpj="99887766000111",
        telefone="(88) 88888-8888",
        is_active=True,
        aprovado=True
    )

    data = {
        "tipo_usuario": "revenda",
        "email": "existente.revenda@teste.com",
        "password": "OutraSenha@456",
        "nome_razao_social": "Outra Revenda",
        "cnpj": "11122233000144",
        "telefone": "(77) 77777-7777"
    }
    response = api_client.post("/api/users/register_full/", data, format="json")

    assert response.status_code == 400
    assert "Email já cadastrado" in response.data["error"]

@pytest.mark.django_db
def test_register_revenda_missing_fields(api_client):
    data = {
        "tipo_usuario": "revenda",
        "email": "incompleta.revenda@teste.com",
        "password": "Senha@123",
        "nome_razao_social": "Revenda Incompleta",
        # Faltando cnpj, telefone
    }
    response = api_client.post("/api/users/register_full/", data, format="json")

    assert response.status_code == 400
    assert "Campos obrigatórios faltando" in response.data["error"]
    assert "cnpj" in response.data["campos_faltando"]
    assert "telefone" in response.data["campos_faltando"]

@pytest.mark.django_db
def test_register_revenda_cnpj_exists(api_client):
    UsuarioRevenda.objects.create_user(
        email="revenda.cnpj@teste.com",
        password="Senha@123",
        nome_razao_social="Revenda CNPJ Existente",
        cnpj="55443322000199", # CNPJ que já vai ser usado no teste
        telefone="(88) 88888-8888",
        is_active=True,
        aprovado=True
    )

    data = {
        "tipo_usuario": "revenda",
        "email": "nova.revenda2@teste.com",
        "password": "Senha@123",
        "nome_razao_social": "Nova Revenda Teste 2",
        "cnpj": "55443322000199", # CNPJ duplicado
        "telefone": "(99) 99999-9999"
    }
    response = api_client.post("/api/users/register_full/", data, format="json")

    assert response.status_code == 400
    assert "CNPJ já cadastrado" in response.data["error"]

