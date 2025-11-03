from datetime import timedelta
from decimal import Decimal

import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from backend.transportador.empresas.models import Empresa
from backend.transportador.estoque.models import MovimentacaoEstoque, Produto
from backend.transportador.frota.models import Position, Vehicle
from backend.transportador.manutencao.models import OrdemServico, StatusOS, TipoManutencao
from backend.transportador.models import UsuarioTransportador
from backend.transportador.pneus.models import Application, Tire


@pytest.mark.django_db
def test_dashboard_metrics_and_stats_align_with_company_data():
    empresa = Empresa.objects.create(
        nome="Transporte Interestelar",
        tipo="transportador",
        cnpj="12345678000100",
    )

    user = UsuarioTransportador.objects.create_user(
        email="gestor@empresa.com",
        password="SenhaForte!123",
        nome_razao_social="Gestor",
        cnpj="12345678000100",
        telefone="11999999999",
        empresa=empresa,
        aprovado=True,
        is_active=True,
    )

    client = APIClient()
    client.force_authenticate(user=user)

    veiculo = Vehicle.objects.create(
        empresa=empresa,
        placa="ABC1D23",
        status="ATIVO",
        km=1500,
        km_proxima_manutencao=1800,
    )

    Position.objects.create(empresa=empresa, veiculo=veiculo, pneu_atual_codigo="PN-1")
    Position.objects.create(empresa=empresa, veiculo=veiculo)

    pneu = Tire.objects.create(
        empresa=empresa,
        codigo="PN123",
        medida="295/80R22.5",
        status="MONTADO",
    )

    Application.objects.create(
        empresa=empresa,
        pneu=pneu,
        veiculo=veiculo,
        medida="295/80R22.5",
    )

    produto = Produto.objects.create(
        empresa=empresa,
        codigo="PRD1",
        descricao="Pneu de teste",
        unidade="UN",
    )

    MovimentacaoEstoque.objects.create(
        produto=produto,
        tipo="ENTRADA",
        data_movimentacao=timezone.now(),
        quantidade=Decimal("2"),
        valor_unitario=Decimal("1000"),
    )
    MovimentacaoEstoque.objects.create(
        produto=produto,
        tipo="SAIDA",
        data_movimentacao=timezone.now(),
        quantidade=Decimal("1"),
        valor_unitario=Decimal("1000"),
    )

    OrdemServico.objects.create(
        empresa=empresa,
        veiculo=veiculo,
        numero="OS001",
        tipo=TipoManutencao.PREVENTIVA,
        status=StatusOS.ABERTA,
        descricao_problema="Verificar freios",
    )
    OrdemServico.objects.create(
        empresa=empresa,
        veiculo=veiculo,
        numero="OS002",
        tipo=TipoManutencao.CORRETIVA,
        status=StatusOS.EM_ANDAMENTO,
        descricao_problema="Troca de óleo",
    )
    OrdemServico.objects.create(
        empresa=empresa,
        veiculo=veiculo,
        numero="OS003",
        tipo=TipoManutencao.CORRETIVA,
        status=StatusOS.CONCLUIDA,
        descricao_problema="Troca de filtro",
        data_conclusao=timezone.now() - timedelta(days=2),
    )

    dashboard_response = client.get("/api/transportador/dashboard/")
    metrics_response = client.get("/api/transportador/dashboard/metrics/")
    stats_response = client.get("/api/transportador/dashboard/stats/")

    assert dashboard_response.status_code == 200
    dashboard_data = dashboard_response.json()
    assert dashboard_data["frota"]["total_veiculos"] == 1
    assert dashboard_data["pneus"]["total_posicoes"] == 2
    assert dashboard_data["manutencao"]["os_abertas"] == 1
    assert dashboard_data["manutencao"]["os_em_andamento"] == 1
    assert dashboard_data["manutencao"]["total_pendentes"] == 2
    assert dashboard_data["mensagem"] is None

    assert metrics_response.status_code == 200
    metrics_data = metrics_response.json()
    assert metrics_data["vehicles"] == 1
    assert metrics_data["positions"] == 2
    assert metrics_data["tires"] == 1
    assert metrics_data["applications"] == 1

    assert stats_response.status_code == 200
    stats_data = stats_response.json()
    assert stats_data["veiculos_totais"] == 1
    assert stats_data["os_concluidas_30d"] == 1
    assert stats_data["pneus_em_uso"] == 1


@pytest.mark.django_db
def test_dashboard_handles_user_without_company():
    user = UsuarioTransportador.objects.create_user(
        email="sem.empresa@teste.com",
        password="SenhaForte!123",
        nome_razao_social="Sem Empresa",
        cnpj="99887766000100",
        telefone="11911112222",
        aprovado=True,
        is_active=True,
    )

    client = APIClient()
    client.force_authenticate(user=user)

    dashboard_response = client.get("/api/transportador/dashboard/")
    metrics_response = client.get("/api/transportador/dashboard/metrics/")
    stats_response = client.get("/api/transportador/dashboard/stats/")

    assert dashboard_response.status_code == 200
    dashboard_data = dashboard_response.json()
    assert dashboard_data["mensagem"] is not None
    assert dashboard_data["frota"]["total_veiculos"] == 0

    assert metrics_response.status_code == 200
    metrics_data = metrics_response.json()
    assert metrics_data == {
        "vehicles": 0,
        "positions": 0,
        "tires": 0,
        "applications": 0,
        "stock_moves": 0,
        "work_orders": 0,
        "tests": 0,
    }

    assert stats_response.status_code == 200
    stats_data = stats_response.json()
    assert stats_data["veiculos_totais"] == 0
    assert stats_data["pneus_em_uso"] == 0
