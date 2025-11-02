
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from backend.borracharia.models import UsuarioBorracharia

# O modelo de usuário principal para borracharias é UsuarioBorracharia

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_register_borracharia_success(api_client):
    initial_user_count = UsuarioBorracharia.objects.count()

    data = {
        "tipo_usuario": "borracharia",
        "email": "nova.borracharia@teste.com",
        "password": "Senha@123",
        "nome_razao_social": "Nova Borracharia Teste",
        "cnpj": "11223344000155",
        "telefone": "(99) 99999-9999"
    }
    response = api_client.post("/api/users/register_full/", data, format="json")

    assert response.status_code == 201
    assert "Cadastro realizado com sucesso! Aguarde aprovação do administrador." in response.data["message"]
    assert UsuarioBorracharia.objects.count() == initial_user_count + 1

    new_borracharia = UsuarioBorracharia.objects.get(email="nova.borracharia@teste.com")
    assert not new_borracharia.is_active  # Deve estar inativo até aprovação
    assert not new_borracharia.aprovado # Deve estar não aprovado até aprovação
    assert new_borracharia.nome_razao_social == "Nova Borracharia Teste"
    assert new_borracharia.cnpj == "11223344000155"

@pytest.mark.django_db
def test_register_borracharia_email_exists(api_client):
    UsuarioBorracharia.objects.create_user(
        email="existente.borracharia@teste.com",
        password="Senha@123",
        nome_razao_social="Borracharia Existente",
        cnpj="99887766000111",
        telefone="(88) 88888-8888",
        is_active=True,
        aprovado=True
    )

    data = {
        "tipo_usuario": "borracharia",
        "email": "existente.borracharia@teste.com",
        "password": "OutraSenha@456",
        "nome_razao_social": "Outra Borracharia",
        "cnpj": "11122233000144",
        "telefone": "(77) 77777-7777"
    }
    response = api_client.post("/api/users/register_full/", data, format="json")

    assert response.status_code == 400
    assert "Email já cadastrado" in response.data["error"]

@pytest.mark.django_db
def test_register_borracharia_missing_fields(api_client):
    data = {
        "tipo_usuario": "borracharia",
        "email": "incompleta.borracharia@teste.com",
        "password": "Senha@123",
        "nome_razao_social": "Borracharia Incompleta",
        # Faltando cnpj, telefone
    }
    response = api_client.post("/api/users/register_full/", data, format="json")

    assert response.status_code == 400
    assert "Campos obrigatórios faltando" in response.data["error"]
    assert "cnpj" in response.data["campos_faltando"]
    assert "telefone" in response.data["campos_faltando"]

@pytest.mark.django_db
def test_register_borracharia_cnpj_exists(api_client):
    UsuarioBorracharia.objects.create_user(
        email="borracharia.cnpj@teste.com",
        password="Senha@123",
        nome_razao_social="Borracharia CNPJ Existente",
        cnpj="11223344000155", # CNPJ que já vai ser usado no teste
        telefone="(88) 88888-8888",
        is_active=True,
        aprovado=True
    )

    data = {
        "tipo_usuario": "borracharia",
        "email": "nova.borracharia2@teste.com",
        "password": "Senha@123",
        "nome_razao_social": "Nova Borracharia Teste 2",
        "cnpj": "11223344000155", # CNPJ duplicado
        "telefone": "(99) 99999-9999"
    }
    response = api_client.post("/api/users/register_full/", data, format="json")

    assert response.status_code == 400
    assert "CNPJ já cadastrado" in response.data["error"]

