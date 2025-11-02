import pytest

@pytest.mark.django_db
def test_frota_veiculos_list(client_auth):
    resp = client_auth.get("/api/transportador/frota/veiculos/")
    assert resp.status_code == 200

@pytest.mark.django_db
def test_pneus_list(client_auth):
    resp = client_auth.get("/api/transportador/pneus/pneus/")
    assert resp.status_code == 200

@pytest.mark.django_db
def test_estoque_mov_list(client_auth):
    resp = client_auth.get("/api/transportador/estoque/movimentacoes/")
    assert resp.status_code == 200

@pytest.mark.django_db
def test_manut_os_list(client_auth):
    resp = client_auth.get("/api/transportador/manutencao/os/")
    assert resp.status_code == 200
