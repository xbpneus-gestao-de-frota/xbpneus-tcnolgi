
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from xbpneus.backend.transportador.manutencao.models import OrdemServico, ItemOrdemServico
from xbpneus.backend.transportador.frota.models import Vehicle
from xbpneus.backend.transportador.empresas.models import Empresa, Filial
from xbpneus.backend.transportador.configuracoes.models import CatalogoModeloVeiculo, OperacaoConfiguracao

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
    user = create_user("test_manutencao@example.com", "password123")
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def setup_manutencao_dependencies():
    empresa, _ = Empresa.objects.get_or_create(nome="Empresa Manutencao", cnpj="11.111.111/0001-11", tipo="TRANSPORTADOR")
    filial, _ = Filial.objects.get_or_create(nome="Filial Manutencao", codigo="004", empresa=empresa)
    modelo_veiculo, _ = CatalogoModeloVeiculo.objects.get_or_create(
        marca="Volvo", familia_modelo="FH", variante="540",
        categoria="CAMINHAO_TRATOR", ano_inicio=2018, ano_fim=2028, configuracoes="6x2"
    )
    config_operacional, _ = OperacaoConfiguracao.objects.get_or_create(
        op_code="RODOVIARIO_PESADO", config_ids_recomendados="6x2",
        implementos_recomendados="Carreta Baú", eixos_tipicos="6x2", pbtc_faixa_aprox_t="40-60"
    )
    vehicle, _ = Vehicle.objects.get_or_create(
        empresa=empresa, filial=filial, placa="MAN0001", modelo_veiculo=modelo_veiculo,
        ano_fabricacao=2020, ano_modelo=2021, tipo="CAMINHAO", status="ATIVO", km=100000,
        km_ultima_manutencao=90000, km_proxima_manutencao=120000,
        chassi="CHASSIMANUTENCAO001", renavam="RENAVAMMANUTENCAO001", capacidade_carga=40,
        configuracao_operacional=config_operacional, data_aquisicao="2020-01-01"
    )
    return empresa, filial, vehicle

@pytest.mark.django_db
def test_ordem_servico_creation(auth_client, setup_manutencao_dependencies):
    empresa, filial, vehicle = setup_manutencao_dependencies
    url = reverse("ordemservico-list")
    data = {
        "empresa": empresa.id,
        "filial": filial.id,
        "veiculo": vehicle.id,
        "tipo_manutencao": "PREVENTIVA",
        "status": "ABERTA",
        "data_abertura": "2025-10-20",
        "observacoes": "Manutenção preventiva de rotina"
    }
    response = auth_client.post(url, data, format="json")
    assert response.status_code == 201, response.data
    assert OrdemServico.objects.count() == 1
    os = OrdemServico.objects.first()
    assert os.veiculo == vehicle

@pytest.mark.django_db
def test_item_ordem_servico_creation(auth_client, setup_manutencao_dependencies):
    empresa, filial, vehicle = setup_manutencao_dependencies
    os = OrdemServico.objects.create(
        empresa=empresa, filial=filial, veiculo=vehicle,
        tipo_manutencao="CORRETIVA", status="ABERTA",
        data_abertura="2025-10-19", observacoes="Troca de pastilhas"
    )
    url = reverse("itemordemservico-list")
    data = {
        "ordem_servico": os.id,
        "descricao": "Troca de óleo",
        "quantidade": 1,
        "valor_unitario": "150.00",
        "observacoes": "Óleo sintético 15W40"
    }
    response = auth_client.post(url, data, format="json")
    assert response.status_code == 201, response.data
    assert ItemOrdemServico.objects.count() == 1
    item = ItemOrdemServico.objects.first()
    assert item.ordem_servico == os


