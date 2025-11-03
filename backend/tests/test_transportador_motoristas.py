from datetime import date, timedelta

import pytest
from rest_framework.test import APIClient

from backend.transportador.empresas.models import Empresa
from backend.transportador.models import UsuarioTransportador
from backend.transportador.motorista_externo.models import MotoristaExterno
from backend.transportador.motorista_interno.models import MotoristaInterno


@pytest.mark.django_db
def test_motorista_transportador_viewset_combines_sources():
    empresa = Empresa.objects.create(
        nome="Galáxia Log",
        tipo="transportador",
        cnpj="55566677000188",
    )

    user = UsuarioTransportador.objects.create_user(
        email="gestor.motoristas@empresa.com",
        password="SenhaForte!123",
        nome_razao_social="Gestor Motoristas",
        cnpj="55566677000188",
        telefone="11888887777",
        empresa=empresa,
        aprovado=True,
        is_active=True,
    )

    interno = MotoristaInterno.objects.create(
        empresa=empresa,
        nome_completo="Motorista Interno",
        cpf="123.456.789-10",
        cnh="CNH123",
        validade_cnh=date.today() + timedelta(days=365),
    )

    externo = MotoristaExterno.objects.create(
        empresa=empresa,
        nome_completo="Motorista Externo",
        cpf="987.654.321-00",
        cnh="CNH999",
        email="externo@empresa.com",
        telefone="11900000000",
    )

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/api/transportador/motorista/motoristas/")
    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] == 2
    tipos = {item["tipo"] for item in payload["results"]}
    assert tipos == {"interno", "externo"}
    ids = {item["id"] for item in payload["results"]}
    assert f"interno:{interno.id}" in ids
    assert f"externo:{externo.id}" in ids

    resumo = client.get("/api/transportador/motorista/motoristas/resumo/")
    assert resumo.status_code == 200
    assert resumo.json() == {"total": 2, "internos": 1, "externos": 1}

    interno_detail = client.get(f"/api/transportador/motorista/motoristas/interno:{interno.id}/")
    assert interno_detail.status_code == 200
    assert interno_detail.json()["nome"] == "Motorista Interno"

    externo_detail = client.get(f"/api/transportador/motorista/motoristas/externo:{externo.id}/")
    assert externo_detail.status_code == 200
    assert externo_detail.json()["nome"] == "Motorista Externo"


@pytest.mark.django_db
def test_motorista_transportador_filters_and_restricts_access():
    empresa_a = Empresa.objects.create(
        nome="Transportes Alfa",
        tipo="transportador",
        cnpj="11122233000155",
    )
    empresa_b = Empresa.objects.create(
        nome="Transportes Beta",
        tipo="transportador",
        cnpj="22233344000166",
    )

    user_a = UsuarioTransportador.objects.create_user(
        email="gestor.alfa@empresa.com",
        password="SenhaForte!123",
        nome_razao_social="Gestor Alfa",
        cnpj="11122233000155",
        telefone="11777776666",
        empresa=empresa_a,
        aprovado=True,
        is_active=True,
    )

    interno_a = MotoristaInterno.objects.create(
        empresa=empresa_a,
        nome_completo="Interno Alfa",
        cpf="111.111.111-11",
        cnh="CNHALFA",
        validade_cnh=date.today() + timedelta(days=400),
    )
    externo_a = MotoristaExterno.objects.create(
        empresa=empresa_a,
        nome_completo="Externo Alfa",
        cpf="222.222.222-22",
        cnh="CNH-EXT-A",
        email="externo.alfa@empresa.com",
    )

    interno_b = MotoristaInterno.objects.create(
        empresa=empresa_b,
        nome_completo="Interno Beta",
        cpf="333.333.333-33",
        cnh="CNHBETA",
        validade_cnh=date.today() + timedelta(days=400),
    )

    client = APIClient()
    client.force_authenticate(user=user_a)

    internos = client.get("/api/transportador/motorista/motoristas/?tipo=interno")
    assert internos.status_code == 200
    internos_payload = internos.json()
    assert internos_payload["count"] == 1
    assert internos_payload["results"][0]["id"] == f"interno:{interno_a.id}"

    externos = client.get("/api/transportador/motorista/motoristas/?tipo=externo")
    assert externos.status_code == 200
    externos_payload = externos.json()
    assert externos_payload["count"] == 1
    assert externos_payload["results"][0]["id"] == f"externo:{externo_a.id}"

    forbidden = client.get(f"/api/transportador/motorista/motoristas/interno:{interno_b.id}/")
    assert forbidden.status_code == 404

    user_sem_empresa = UsuarioTransportador.objects.create_user(
        email="sem.empresa.motorista@teste.com",
        password="SenhaForte!123",
        nome_razao_social="Sem Empresa",
        cnpj="77788899000111",
        telefone="11955556666",
        aprovado=True,
        is_active=True,
    )
    client.force_authenticate(user=user_sem_empresa)
    vazio = client.get("/api/transportador/motorista/motoristas/")
    assert vazio.status_code == 200
    assert vazio.json()["count"] == 0
