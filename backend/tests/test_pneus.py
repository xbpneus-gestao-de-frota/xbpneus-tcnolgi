
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from xbpneus.backend.transportador.pneus.models import Tire, Application, MovimentacaoPneu, MedicaoPneu
from xbpneus.backend.transportador.frota.models import Vehicle, Position
from xbpneus.backend.transportador.empresas.models import Empresa, Filial
from xbpneus.backend.transportador.configuracoes.models import CatalogoModeloVeiculo, OperacaoConfiguracao
from decimal import Decimal

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    def _create_user(email, password, is_staff=False, is_active=True):
        return User.objects.create_user(email=email, password=password, is_staff=is_staff, is_active=is_active)
    return _create_user

@pytest.fixture
def auth_client(api_client, create_user):
    user = create_user("test@example.com", "password123")
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def setup_tire_dependencies():
    empresa, _ = Empresa.objects.get_or_create(nome="Empresa Pneu", cnpj="11.222.333/0001-44", tipo="TRANSPORTADOR")
    filial, _ = Filial.objects.get_or_create(nome="Filial Pneu", codigo="002", empresa=empresa)
    modelo_veiculo, _ = CatalogoModeloVeiculo.objects.get_or_create(
        marca="Scania", familia_modelo="R450", variante="450",
        categoria="CAMINHAO_TRATOR", ano_inicio=2010, ano_fim=2020, configuracoes="4x2"
    )
    config_operacional, _ = OperacaoConfiguracao.objects.get_or_create(
        op_code="RODOVIARIO_LEVE", config_ids_recomendados="4x2",
        implementos_recomendados="Bau", eixos_tipicos="4x2", pbtc_faixa_aprox_t="10-20"
    )
    vehicle, _ = Vehicle.objects.get_or_create(
        empresa=empresa, filial=filial, placa="PNE0001", modelo_veiculo=modelo_veiculo,
        ano_fabricacao=2015, ano_modelo=2016, tipo="CAMINHAO", status="ATIVO", km=50000,
        km_ultima_manutencao=40000, km_proxima_manutencao=60000,
        chassi="CHASSPNEU0001", renavam="RENAVAMPNEU0001", capacidade_carga=10,
        configuracao_operacional=config_operacional, data_aquisicao="2015-01-01"
    )
    return empresa, filial, vehicle

@pytest.mark.django_db
def test_tire_creation(auth_client, setup_tire_dependencies):
    empresa, filial, vehicle = setup_tire_dependencies
    url = reverse("tire-list")
    data = {
        "empresa": empresa.id,
        "filial": filial.id,
        "codigo": "PNU001",
        "medida": "295/80R22.5",
        "marca": "Michelin",
        "modelo": "X Multiway 3D XZE",
        "dot": "1020",
        "profundidade_sulco_novo": Decimal("15.0"),
        "profundidade_sulco_minimo": Decimal("3.0"),
        "km_total": 0,
        "km_atual": 0,
        "status": "ESTOQUE",
        "posicao_atual": "",
        "data_compra": "2023-01-01",
        "valor_compra": Decimal("1500.00"),
        "observacoes": "Pneu novo para teste"
    }
    response = auth_client.post(url, data, format="json")
    assert response.status_code == 201, response.data
    assert Tire.objects.count() == 1
    tire = Tire.objects.first()
    assert tire.codigo == "PNU001"

@pytest.mark.django_db
def test_tire_maintenance_inspection_fields(auth_client, setup_tire_dependencies):
    empresa, filial, vehicle = setup_tire_dependencies
    tire = Tire.objects.create(
        empresa=empresa, filial=filial, codigo="PNU002",
        medida="295/80R22.5", marca="Pirelli", modelo="Formula Driver",
        dot="1221", profundidade_sulco_novo=Decimal("14.0"),
        profundidade_sulco_minimo=Decimal("3.0"), km_total=50000,
        km_atual=40000, status="MONTADO", data_compra="2022-06-01",
        valor_compra=Decimal("1200.00"), ultima_inspecao="2024-09-01",
        proxima_inspecao="2024-10-01"
    )
    url = reverse("tire-detail", kwargs={"pk": tire.id})
    response = auth_client.get(url)
    assert response.status_code == 200, response.data
    assert "vida_util_percentual" in response.data
    assert "precisa_inspecao" in response.data

    # Simulate a tire needing inspection
    tire.proxima_inspecao = "2024-01-01"
    tire.save()
    response = auth_client.get(url)
    assert response.status_code == 200, response.data
    assert response.data["precisa_inspecao"] == True

@pytest.mark.django_db
def test_application_creation(auth_client, setup_tire_dependencies):
    empresa, filial, vehicle = setup_tire_dependencies
    tire = Tire.objects.create(
        empresa=empresa, filial=filial, codigo="PNU003",
        medida="295/80R22.5", marca="Goodyear", modelo="KMax",
        dot="1522", profundidade_sulco_novo=Decimal("16.0"),
        profundidade_sulco_minimo=Decimal("4.0"), km_total=0,
        km_atual=0, status="ESTOQUE", data_compra="2023-03-01",
        valor_compra=Decimal("1600.00")
    )
    url = reverse("application-list")
    data = {
        "pneu": tire.id,
        "veiculo": vehicle.id,
        "km_montagem": 50000,
        "data_montagem": "2023-03-10",
        "posicao": "LD1",
        "observacoes": "Montagem inicial"
    }
    response = auth_client.post(url, data, format="json")
    assert response.status_code == 201, response.data
    assert Application.objects.count() == 1
    app = Application.objects.first()
    assert app.pneu == tire
    assert app.veiculo == vehicle

@pytest.mark.django_db
def test_movimentacao_pneu_creation(auth_client, setup_tire_dependencies):
    empresa, filial, vehicle = setup_tire_dependencies
    tire = Tire.objects.create(
        empresa=empresa, filial=filial, codigo="PNU004",
        medida="295/80R22.5", marca="Continental", modelo="Conti Hybrid",
        dot="1823", profundidade_sulco_novo=Decimal("14.5"),
        profundidade_sulco_minimo=Decimal("3.5"), km_total=10000,
        km_atual=10000, status="ESTOQUE", data_compra="2023-06-01",
        valor_compra=Decimal("1450.00")
    )
    url = reverse("movimentacaopneu-list")
    data = {
        "pneu": tire.id,
        "tipo": "MONTAGEM",
        "origem": "ESTOQUE",
        "destino": "VEICULO_PNE0001_LD1",
        "km_pneu": 10000,
        "observacoes": "Pneu montado no veículo PNE0001"
    }
    response = auth_client.post(url, data, format="json")
    assert response.status_code == 201, response.data
    assert MovimentacaoPneu.objects.count() == 1
    mov = MovimentacaoPneu.objects.first()
    assert mov.pneu == tire

@pytest.mark.django_db
def test_medicao_pneu_creation(auth_client, setup_tire_dependencies):
    empresa, filial, vehicle = setup_tire_dependencies
    tire = Tire.objects.create(
        empresa=empresa, filial=filial, codigo="PNU005",
        medida="295/80R22.5", marca="Bridgestone", modelo="Duravis",
        dot="2024", profundidade_sulco_novo=Decimal("13.0"),
        profundidade_sulco_minimo=Decimal("2.5"), km_total=20000,
        km_atual=15000, status="MONTADO", data_compra="2023-09-01",
        valor_compra=Decimal("1300.00")
    )
    url = reverse("medicaopneu-list")
    data = {
        "pneu": tire.id,
        "sulco": Decimal("10.0"),
        "pressao": Decimal("110.0"),
        "km_pneu": 15000,
        "observacoes": "Medição de rotina"
    }
    response = auth_client.post(url, data, format="json")
    assert response.status_code == 201, response.data
    assert MedicaoPneu.objects.count() == 1
    med = MedicaoPneu.objects.first()
    assert med.pneu == tire


