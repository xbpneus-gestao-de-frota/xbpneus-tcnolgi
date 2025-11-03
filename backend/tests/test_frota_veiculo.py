
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from backend.transportador.frota.models import Vehicle
from backend.transportador.empresas.models import Empresa, Filial
from backend.transportador.configuracoes.models import CatalogoModeloVeiculo, OperacaoConfiguracao
from django.contrib.auth import get_user_model

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    def _create_user(email, password, is_staff=False, is_active=True):
        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(
        existing_user = user_model.objects.filter(email=email).first()
        if existing_user:
            updated_fields = []
            if existing_user.is_staff != is_staff:
                existing_user.is_staff = is_staff
                updated_fields.append("is_staff")
            if existing_user.is_active != is_active:
                existing_user.is_active = is_active
                updated_fields.append("is_active")
            if password and not existing_user.check_password(password):
                existing_user.set_password(password)
                updated_fields.append("password")
            if updated_fields:
                existing_user.save(update_fields=updated_fields)
            return existing_user

        return user_model.objects.create_user(
            email=email,
            defaults={
                "is_staff": is_staff,
                "is_active": is_active,
            },
        )

        if created:
            user.set_password(password)
        else:
            if password:
                user.set_password(password)
            user.is_staff = is_staff
            user.is_active = is_active

        user.save()
        return user
    return _create_user

@pytest.fixture
def auth_client(api_client, create_user):
    user = create_user("test@example.com", "password123")
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def setup_vehicle_dependencies():
    empresa, _ = Empresa.objects.get_or_create(nome="Empresa Teste", cnpj="12.345.678/0001-90", tipo="TRANSPORTADOR")
    filial, _ = Filial.objects.get_or_create(nome="Filial Teste", codigo="001", empresa=empresa)
    modelo_veiculo, _ = CatalogoModeloVeiculo.objects.get_or_create(
        marca="Mercedes-Benz", familia_modelo="Actros", variante="2651",
        categoria="CAMINHAO_TRATOR", ano_inicio=2015, ano_fim=2025, configuracoes="6x4"
    )
    config_operacional, _ = OperacaoConfiguracao.objects.get_or_create(
        op_code="RODOVIARIO_PESADO", config_ids_recomendados="6x4|4x2",
        implementos_recomendados="Carreta Graneleira", eixos_tipicos="6x4", pbtc_faixa_aprox_t="45-74"
    )
    return empresa, filial, modelo_veiculo, config_operacional

@pytest.mark.django_db
def test_vehicle_creation(auth_client, setup_vehicle_dependencies):
    empresa, filial, modelo_veiculo, config_operacional = setup_vehicle_dependencies
    url = reverse("veiculo-list") # Assumindo que o basename é 'veiculo'
    data = {
        "empresa": empresa.id,
        "filial": filial.id,
        "placa": "ABC1234",
        "modelo_veiculo": modelo_veiculo.id,
        "ano_fabricacao": 2020,
        "ano_modelo": 2021,
        "tipo": "CAMINHAO",
        "status": "ATIVO",
        "km": 100000,
        "km_ultima_manutencao": 90000,
        "km_proxima_manutencao": 120000,
        "chassi": "12345678901234567",
        "renavam": "12345678901",
        "capacidade_carga": 30,
        "configuracao_operacional": config_operacional.id,
        "data_aquisicao": "2020-01-01",
        "data_venda": None,
        "observacoes": "Veículo de teste"
    }
    response = auth_client.post(url, data, format="json")
    assert response.status_code == 201, response.data
    assert Vehicle.objects.count() == 1
    vehicle = Vehicle.objects.first()
    assert vehicle.placa == "ABC1234"

@pytest.mark.django_db
def test_vehicle_maintenance_fields(auth_client, setup_vehicle_dependencies):
    empresa, filial, modelo_veiculo, config_operacional = setup_vehicle_dependencies
    vehicle = Vehicle.objects.create(
        empresa=empresa, filial=filial, placa="XYZ5678",
        modelo_veiculo=modelo_veiculo, ano_fabricacao=2018, ano_modelo=2019,
        tipo="CAMINHAO", status="ATIVO", km=150000, km_ultima_manutencao=140000,
        km_proxima_manutencao=160000, chassi="98765432109876543", renavam="98765432109",
        capacidade_carga=25, configuracao_operacional=config_operacional,
        data_aquisicao="2018-05-10"
    )
    url = reverse("veiculo-detail", kwargs={"pk": vehicle.id})
    response = auth_client.get(url)
    assert response.status_code == 200, response.data
    assert response.data["precisa_manutencao"] == False
    assert response.data["km_ate_manutencao"] == 10000

    # Test when maintenance is needed
    vehicle.km = 160001
    vehicle.save()
    response = auth_client.get(url)
    assert response.status_code == 200, response.data
    assert response.data["precisa_manutencao"] == True
    assert response.data["km_ate_manutencao"] == -1


@pytest.mark.django_db
def test_fleet_analysis_endpoint(auth_client, setup_vehicle_dependencies):
    Vehicle.objects.all().delete()
    empresa, filial, modelo_veiculo, config_operacional = setup_vehicle_dependencies

    Vehicle.objects.create(
        empresa=empresa,
        filial=filial,
        placa="AAA1B23",
        modelo_veiculo=modelo_veiculo,
        ano_fabricacao=2019,
        ano_modelo=2020,
        tipo="CAMINHAO",
        status="ATIVO",
        km=120000,
        km_ultima_manutencao=110000,
        km_proxima_manutencao=125000,
        configuracao_operacional=config_operacional,
    )

    Vehicle.objects.create(
        empresa=empresa,
        filial=filial,
        placa="BBB2C34",
        modelo_veiculo=modelo_veiculo,
        ano_fabricacao=2017,
        ano_modelo=2018,
        tipo="CARRETA",
        status="MANUTENCAO",
        km=180000,
        km_ultima_manutencao=170000,
        km_proxima_manutencao=175000,
        configuracao_operacional=config_operacional,
    )

    Vehicle.objects.create(
        empresa=empresa,
        filial=filial,
        placa="CCC3D45",
        modelo_veiculo=modelo_veiculo,
        ano_fabricacao=2016,
        ano_modelo=2017,
        tipo="CAMINHAO",
        status="ATIVO",
        km=90000,
        km_ultima_manutencao=85000,
        km_proxima_manutencao=None,
        configuracao_operacional=config_operacional,
    )

    Vehicle.objects.create(
        empresa=empresa,
        filial=filial,
        placa="DDD4E56",
        modelo_veiculo=modelo_veiculo,
        ano_fabricacao=2021,
        ano_modelo=2022,
        tipo="CAMINHAO",
        status="ATIVO",
        km=174800,
        km_ultima_manutencao=170000,
        km_proxima_manutencao=175000,
        configuracao_operacional=config_operacional,
    )

    url = reverse("frota-analise-list")
    response = auth_client.get(url)

    assert response.status_code == 200, response.data
    data = response.data

    assert data["total_veiculos"] == 4
    assert data["por_status"].get("ATIVO") == 3
    assert data["por_status"].get("MANUTENCAO") == 1
    assert data["por_tipo"].get("CAMINHAO") == 3
    assert data["por_tipo"].get("CARRETA") == 1
    assert data["manutencao"]["precisam_manutencao"] == 1
    assert data["manutencao"]["sem_agendamento"] == 1

    proximas = data["manutencao"]["proximas_manutencoes"]
    assert isinstance(proximas, list)
    assert any(item["placa"] == "DDD4E56" for item in proximas)

