
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def approved_transportador_user(db):
    user_model = get_user_model()
    user, created = user_model.objects.get_or_create(
        email="aprovado.transportador@teste.com",
        defaults={
            "password": "Senha@123",
            "is_active": True,  # Usuário ativo
            "aprovado": True,    # Usuário aprovado
            "nome_razao_social": "Transportador Aprovado",
            "cnpj": "11111111000111",
            "telefone": "(11) 11111-1111"
        }
    )
    if created:
        user.set_password("Senha@123")
        user.save()
    return user

@pytest.fixture
def unapproved_transportador_user(db):
    user_model = get_user_model()
    user, created = user_model.objects.get_or_create(
        email="naoaprovado.transportador@teste.com",
        defaults={
            "password": "Senha@123",
            "is_active": False, # Usuário inativo
            "aprovado": False,   # Usuário não aprovado
            "nome_razao_social": "Transportador Não Aprovado",
            "cnpj": "22222222000122",
            "telefone": "(22) 22222-2222"
        }
    )
    if created:
        user.set_password("Senha@123")
        user.save()
    return user

@pytest.mark.django_db
def test_login_transportador_success(api_client, approved_transportador_user):
    data = {
        "email": "aprovado.transportador@teste.com",
        "password": "Senha@123"
    }
    response = api_client.post("/api/token/", data, format="json")

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data

@pytest.mark.django_db
def test_login_transportador_unapproved(api_client, unapproved_transportador_user):
    data = {
        "email": "naoaprovado.transportador@teste.com",
        "password": "Senha@123"
    }
    response = api_client.post("/api/token/", data, format="json")

    assert response.status_code == 403
    assert "detail" in response.data
    assert "Usuário não aprovado" in response.data["detail"]

@pytest.mark.django_db
def test_login_transportador_wrong_password(api_client, approved_transportador_user):
    data = {
        "email": "aprovado.transportador@teste.com",
        "password": "SenhaErrada@123"
    }
    response = api_client.post("/api/token/", data, format="json")

    assert response.status_code == 401
    assert "detail" in response.data
    assert "No active account found with the given credentials" in response.data["detail"]

@pytest.mark.django_db
def test_login_transportador_non_existent_user(api_client):
    data = {
        "email": "naoexiste@teste.com",
        "password": "SenhaQualquer@123"
    }
    response = api_client.post("/api/token/", data, format="json")

    assert response.status_code == 401
    assert "detail" in response.data
    assert "No active account found with the given credentials" in response.data["detail"]

@pytest.mark.django_db
def test_login_transportador_missing_fields(api_client):
    data = {
        "email": "aprovado.transportador@teste.com",
        # Faltando password
    }
    response = api_client.post("/api/token/", data, format="json")
    print(response.data) # Adicionado para depuração
    assert response.status_code == 400
    assert "password" in response.data
    assert "Este campo é obrigatório." in response.data["password"][0]

