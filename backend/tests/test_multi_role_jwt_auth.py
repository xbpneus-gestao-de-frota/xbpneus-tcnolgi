import pytest
from rest_framework.test import APIClient
from django.conf import settings

from backend.motorista.models import UsuarioMotorista
from backend.borracharia.models import UsuarioBorracharia
from backend.revenda.models import UsuarioRevenda
from backend.recapagem.models import UsuarioRecapagem


@pytest.mark.django_db
@pytest.mark.parametrize(
    "model,user_data,profile_url,expected_role,expected_redirect",
    [
        (
            UsuarioMotorista,
            {
                "email": "motorista.jwt@example.com",
                "password": "SenhaSegura123",
                "nome_completo": "Motorista JWT",
                "cpf": "11122233344",
                "cnh": "CNH1234567",
                "categoria_cnh": "D",
                "telefone": "(11) 99999-9999",
                "aprovado": True,
                "is_active": True,
            },
            "/api/motorista/perfil/",
            "motorista",
            "/motorista/dashboard/",
        ),
        (
            UsuarioBorracharia,
            {
                "email": "borracharia.jwt@example.com",
                "password": "SenhaSegura123",
                "nome_razao_social": "Borracharia JWT",
                "cnpj": "12345678000190",
                "telefone": "(11) 98888-7777",
                "endereco": "Rua das Borrachas, 100",
                "aprovado": True,
                "is_active": True,
            },
            "/api/borracharia/perfil/",
            "borracharia",
            "/borracharia/dashboard/",
        ),
        (
            UsuarioRevenda,
            {
                "email": "revenda.jwt@example.com",
                "password": "SenhaSegura123",
                "nome_razao_social": "Revenda JWT",
                "cnpj": "98765432000190",
                "telefone": "(11) 97777-6666",
                "endereco": "Avenida das Revendas, 200",
                "aprovado": True,
                "is_active": True,
            },
            "/api/revenda/perfil/",
            "revenda",
            "/revenda/dashboard/",
        ),
        (
            UsuarioRecapagem,
            {
                "email": "recapagem.jwt@example.com",
                "password": "SenhaSegura123",
                "nome_razao_social": "Recapagem JWT",
                "cnpj": "11223344000190",
                "telefone": "(11) 96666-5555",
                "endereco": "Rodovia das Recapagens, 300",
                "aprovado": True,
                "is_active": True,
            },
            "/api/recapagem/perfil/",
            "recapagem",
            "/recapagem/dashboard/",
        ),
    ],
)
def test_multimodel_token_login_and_profile(model, user_data, profile_url, expected_role, expected_redirect):
    client = APIClient()
    payload = user_data.copy()
    password = payload.pop("password")
    email = payload["email"]

    model.objects.filter(email__iexact=email).delete()

    user = model.objects.create_user(password=password, **payload)

    # Garantir aprovação e ativação pós-criação
    if hasattr(user, "aprovado"):
        user.aprovado = True
    if hasattr(user, "is_active"):
        user.is_active = True
    user.save()

    login_response = client.post(
        "/api/token/",
        {"email": email, "password": password},
        format="json",
    )

    assert login_response.status_code == 200
    assert "access" in login_response.data
    assert "refresh" in login_response.data
    assert login_response.data["user_role"] == expected_role
    assert login_response.data["redirect"] == expected_redirect

    access_token = login_response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    profile_response = client.get(profile_url)
    assert profile_response.status_code == 200
    assert profile_response.data["email"].lower() == email.lower()


@pytest.mark.django_db
def test_refresh_token_for_motorista_user():
    client = APIClient()

    UsuarioMotorista.objects.filter(email__iexact="refresh.motorista@example.com").delete()

    user = UsuarioMotorista.objects.create_user(
        email="refresh.motorista@example.com",
        password="SenhaSegura123",
        nome_completo="Motorista Refresh",
        cpf="55566677788",
        cnh="CNH7654321",
        categoria_cnh="D",
        telefone="(11) 91234-5678",
        aprovado=True,
        is_active=True,
    )

    login_response = client.post(
        "/api/token/",
        {"email": user.email, "password": "SenhaSegura123"},
        format="json",
    )

    assert login_response.status_code == 200
    refresh_token = login_response.data["refresh"]

    refresh_response = client.post(
        "/api/token/refresh/",
        {"refresh": refresh_token},
        format="json",
    )

    assert refresh_response.status_code == 200
    assert "access" in refresh_response.data
    # Rotation and blacklisting are disabled for multi-model tokens to avoid
    # OutstandingToken foreign key issues, so the refresh token is not rotated.
    assert "refresh" not in refresh_response.data
