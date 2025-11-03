import pytest
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from backend.transportador.ia_pneus.models import AnaliseIA


@pytest.fixture
def authenticated_client(db):
    user_model = get_user_model()
    user = user_model.objects.create_user(
        email="ia-tester@example.com",
        password="test-pass-123",
        nome_razao_social="Tester",
        is_staff=True,
    )

    client = APIClient()
    client.force_authenticate(user)
    return client, user


@pytest.mark.django_db
def test_analisar_imagem_cria_registro(tmp_path, authenticated_client):
    client, user = authenticated_client
    arquivo = SimpleUploadedFile(
        "pneu_banda.jpg",
        b"fake-image-bytes",
        content_type="image/jpeg",
    )

    with override_settings(MEDIA_ROOT=tmp_path):
        response = client.post(
            reverse("analise-analisar"),
            {
                "tipo_analise": "imagem",
                "arquivo": arquivo,
                "descricao": "Fotos da banda de rodagem",
            },
            format="multipart",
        )

    assert response.status_code == 201, response.data

    analise = AnaliseIA.objects.get(pk=response.data["id"])
    analise.refresh_from_db()

    assert analise.usuario == user
    assert analise.status == "concluida"
    assert analise.resultado.get("total_imagens") == 1
    assert analise.precisao > 0


@pytest.mark.django_db
def test_dashboard_agrega_metricas_por_usuario(tmp_path, authenticated_client):
    client, user = authenticated_client

    with override_settings(MEDIA_ROOT=tmp_path):
        upload = SimpleUploadedFile(
            "pneu_banda.jpg",
            b"fake-image-bytes",
            content_type="image/jpeg",
        )
        response = client.post(
            reverse("analise-analisar"),
            {
                "tipo_analise": "imagem",
                "arquivo": upload,
                "descricao": "Fotos da banda de rodagem",
            },
            format="multipart",
        )

    assert response.status_code == 201, response.data

    analise_concluida = AnaliseIA.objects.get(pk=response.data["id"])
    analise_concluida.precisao = 0.85
    analise_concluida.tempo_processamento = 1.0
    analise_concluida.save(update_fields=["precisao", "tempo_processamento"])

    erro_file = ContentFile(b"dados", name="erro.jpg")
    AnaliseIA.objects.create(
        usuario=user,
        tipo_analise="imagem",
        arquivo=erro_file,
        resultado={"erro": "falha"},
        precisao=0.5,
        tempo_processamento=2.0,
        status="erro",
    )

    with override_settings(MEDIA_ROOT=tmp_path):
        dashboard = client.get(reverse("analise-dashboard"))

    assert dashboard.status_code == 200, dashboard.data
    payload = dashboard.data

    assert payload["total_analises"] == 2
    assert payload["fila"]["concluidas"] == 1
    assert payload["fila"]["erros"] == 1
    assert pytest.approx(payload["precisao_media"], rel=1e-3) == 0.675
    assert pytest.approx(payload["tempo_medio"], rel=1e-3) == 1.5
