
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from backend.recapagem.models import UsuarioRecapagem

# O modelo de usuário principal para recapagens é UsuarioRecapagem

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_register_recapagem_success(api_client):
    initial_user_count = UsuarioRecapagem.objects.count()

    data = {
        "tipo_usuario": "recapagem",
        "email": "nova.recapagem@teste.com",
        "password": "Senha@123",
        "nome_razao_social": "Nova Recapagem Teste",
        "cnpj": "66554433000188",
        "telefone": "(99) 99999-9999"
    }
    response = api_client.post("/api/users/register_full/", data, format="json")

    assert response.status_code == 201
    assert "Cadastro realizado com sucesso! Aguarde aprovação do administrador." in response.data["message"]
    assert UsuarioRecapagem.objects.count() == initial_user_count + 1

    new_recapagem = UsuarioRecapagem.objects.get(email="nova.recapagem@teste.com")
    assert not new_recapagem.is_active  # Deve estar inativo até aprovação
    assert not new_recapagem.aprovado # Deve estar não aprovado até aprovação
    assert new_recapagem.nome_razao_social == "Nova Recapagem Teste"
    assert new_recapagem.cnpj == "66554433000188"

@pytest.mark.django_db
def test_register_recapagem_email_exists(api_client):
    UsuarioRecapagem.objects.create_user(
        email="existente.recapagem@teste.com",
        password="Senha@123",
        nome_razao_social="Recapagem Existente",
        cnpj="99887766000111",
        telefone="(88) 88888-8888",
        is_active=True,
        aprovado=True
    )

    data = {
        "tipo_usuario": "recapagem",
        "email": "existente.recapagem@teste.com",
        "password": "OutraSenha@456",
        "nome_razao_social": "Outra Recapagem",
        "cnpj": "11122233000144",
        "telefone": "(77) 77777-7777"
    }
    response = api_client.post("/api/users/register_full/", data, format="json")

    assert response.status_code == 400
    assert "Email já cadastrado" in response.data["error"]

@pytest.mark.django_db
def test_register_recapagem_missing_fields(api_client):
    data = {
        "tipo_usuario": "recapagem",
        "email": "incompleta.recapagem@teste.com",
        "password": "Senha@123",
        "nome_razao_social": "Recapagem Incompleta",
        # Faltando cnpj, telefone
    }
    response = api_client.post("/api/users/register_full/", data, format="json")

    assert response.status_code == 400
    assert "Campos obrigatórios faltando" in response.data["error"]
    assert "cnpj" in response.data["campos_faltando"]
    assert "telefone" in response.data["campos_faltando"]

@pytest.mark.django_db
def test_register_recapagem_cnpj_exists(api_client):
    UsuarioRecapagem.objects.create_user(
        email="recapagem.cnpj@teste.com",
        password="Senha@123",
        nome_razao_social="Recapagem CNPJ Existente",
        cnpj="66554433000188", # CNPJ que já vai ser usado no teste
        telefone="(88) 88888-8888",
        is_active=True,
        aprovado=True
    )

    data = {
        "tipo_usuario": "recapagem",
        "email": "nova.recapagem2@teste.com",
        "password": "Senha@123",
        "nome_razao_social": "Nova Recapagem Teste 2",
        "cnpj": "66554433000188", # CNPJ duplicado
        "telefone": "(99) 99999-9999"
    }
    response = api_client.post("/api/users/register_full/", data, format="json")

    assert response.status_code == 400
    assert "CNPJ já cadastrado" in response.data["error"]

