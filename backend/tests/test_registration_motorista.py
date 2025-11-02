
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from backend.motorista.models import UsuarioMotorista

# O modelo de usuário principal para motoristas é UsuarioMotorista

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_register_motorista_success(api_client):
    initial_user_count = UsuarioMotorista.objects.count()

    data = {
        "tipo_usuario": "motorista",
        "email": "novo.motorista@teste.com",
        "password": "Senha@123",
        "nome_completo": "Novo Motorista Teste",
        "cpf": "11122233344",
        "cnh": "12345678901",
        "categoria_cnh": "B",
        "telefone": "(99) 99999-9999"
    }
    response = api_client.post("/api/users/register_full/", data, format="json")

    assert response.status_code == 201
    assert "Cadastro realizado com sucesso! Aguarde aprovação do administrador." in response.data["message"]
    assert UsuarioMotorista.objects.count() == initial_user_count + 1

    new_motorista = UsuarioMotorista.objects.get(email="novo.motorista@teste.com")
    assert not new_motorista.is_active  # Deve estar inativo até aprovação
    assert not new_motorista.aprovado # Deve estar não aprovado até aprovação
    assert new_motorista.nome_completo == "Novo Motorista Teste"
    assert new_motorista.cpf == "11122233344"
    assert new_motorista.cnh == "12345678901"

@pytest.mark.django_db
def test_register_motorista_email_exists(api_client):
    UsuarioMotorista.objects.create_user(
        email="existente.motorista@teste.com",
        password="Senha@123",
        nome_completo="Motorista Existente",
        cpf="99988877766",
        cnh="98765432109",
        categoria_cnh="A",
        telefone="(88) 88888-8888",
        is_active=True,
        aprovado=True
    )

    data = {
        "tipo_usuario": "motorista",
        "email": "existente.motorista@teste.com",
        "password": "OutraSenha@456",
        "nome_completo": "Outro Motorista",
        "cpf": "12345678900",
        "cnh": "10987654321",
        "categoria_cnh": "C",
        "telefone": "(77) 77777-7777"
    }
    response = api_client.post("/api/users/register_full/", data, format="json")

    assert response.status_code == 400
    assert "Email já cadastrado" in response.data["error"]

@pytest.mark.django_db
def test_register_motorista_missing_fields(api_client):
    data = {
        "tipo_usuario": "motorista",
        "email": "incompleto.motorista@teste.com",
        "password": "Senha@123",
        "nome_completo": "Motorista Incompleto",
        # Faltando cpf, cnh, categoria_cnh, telefone
    }
    response = api_client.post("/api/users/register_full/", data, format="json")

    assert response.status_code == 400
    assert "Campos obrigatórios faltando" in response.data["error"]
    assert "cpf" in response.data["campos_faltando"]
    assert "cnh" in response.data["campos_faltando"]
    assert "categoria_cnh" in response.data["campos_faltando"]
    assert "telefone" in response.data["campos_faltando"]

@pytest.mark.django_db
def test_register_motorista_cpf_exists(api_client):
    UsuarioMotorista.objects.create_user(
        email="motorista.cpf@teste.com",
        password="Senha@123",
        nome_completo="Motorista CPF Existente",
        cpf="11122233344", # CPF que já vai ser usado no teste
        cnh="98765432100",
        categoria_cnh="A",
        telefone="(88) 88888-8888",
        is_active=True,
        aprovado=True
    )

    data = {
        "tipo_usuario": "motorista",
        "email": "novo.motorista2@teste.com",
        "password": "Senha@123",
        "nome_completo": "Novo Motorista Teste 2",
        "cpf": "11122233344", # CPF duplicado
        "cnh": "12345678902",
        "categoria_cnh": "B",
        "telefone": "(99) 99999-9999"
    }
    response = api_client.post("/api/users/register_full/", data, format="json")

    assert response.status_code == 400
    assert "CPF já cadastrado" in response.data["error"]

@pytest.mark.django_db
def test_register_motorista_cnh_exists(api_client):
    UsuarioMotorista.objects.create_user(
        email="motorista.cnh@teste.com",
        password="Senha@123",
        nome_completo="Motorista CNH Existente",
        cpf="22233344455",
        cnh="12345678901", # CNH que já vai ser usado no teste
        categoria_cnh="B",
        telefone="(88) 88888-8888",
        is_active=True,
        aprovado=True
    )

    data = {
        "tipo_usuario": "motorista",
        "email": "novo.motorista3@teste.com",
        "password": "Senha@123",
        "nome_completo": "Novo Motorista Teste 3",
        "cpf": "33344455566",
        "cnh": "12345678901", # CNH duplicada
        "categoria_cnh": "C",
        "telefone": "(99) 99999-9999"
    }
    response = api_client.post("/api/users/register_full/", data, format="json")

    assert response.status_code == 400
    assert "CNH já cadastrada" in response.data["error"]

