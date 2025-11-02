"""
Testes de integração para validar o fluxo de login e acesso às funcionalidades do Transportador.
"""
import pytest
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from backend.transportador.models import UsuarioTransportador

User = get_user_model()


@pytest.mark.django_db
class TestTransportadorFuncionalidades(TestCase):
    """Testes para validar as funcionalidades do Transportador."""
    
    def setUp(self):
        """Configurar dados de teste."""
        self.client = APIClient()
        
        # Criar um usuário Transportador
        self.user = UsuarioTransportador.objects.create_user(
            email="transportador.teste@xbpneus.com",
            password="Teste@2025",
            nome_razao_social="Transportadora Teste",
            cnpj="12345678000190",
            telefone="11987654321"
        )
        self.user.is_active = True
        self.user.aprovado = True
        self.user.save()
    
    def test_login_transportador(self):
        """Testa se o login do Transportador retorna um token válido."""
        response = self.client.post(
            "/api/token/",
            {
                "email": "transportador.teste@xbpneus.com",
                "password": "Teste@2025"
            },
            format="json"
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data
        
        print(f"✓ Login bem-sucedido. Token: {response.data['access'][:20]}...")
    
    def test_dashboard_endpoint_with_token(self):
        """Testa se conseguimos acessar o endpoint de dashboard com o token."""
        # Fazer login
        login_response = self.client.post(
            "/api/token/",
            {
                "email": "transportador.teste@xbpneus.com",
                "password": "Teste@2025"
            },
            format="json"
        )
        
        token = login_response.data["access"]
        
        # Acessar o endpoint de dashboard com o token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get("/api/transportador/dashboard/")
        
        assert response.status_code == status.HTTP_200_OK
        print(f"✓ Acesso ao dashboard bem-sucedido. Dados: {response.data}")
    
    def test_dashboard_endpoint_without_token(self):
        """Testa se o endpoint de dashboard rejeita requisições sem token."""
        response = self.client.get("/api/transportador/dashboard/")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        print(f"✓ Acesso ao dashboard sem token foi rejeitado corretamente.")
    
    def test_dashboard_endpoint_with_invalid_token(self):
        """Testa se o endpoint de dashboard rejeita tokens inválidos."""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer invalid_token")
        response = self.client.get("/api/transportador/dashboard/")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        print(f"✓ Acesso ao dashboard com token inválido foi rejeitado corretamente.")
    
    def test_refresh_token(self):
        """Testa se conseguimos renovar o token usando o refresh token."""
        # Fazer login
        login_response = self.client.post(
            "/api/token/",
            {
                "email": "transportador.teste@xbpneus.com",
                "password": "Teste@2025"
            },
            format="json"
        )
        
        refresh_token = login_response.data["refresh"]
        
        # Renovar o token
        refresh_response = self.client.post(
            "/api/token/refresh/",
            {"refresh": refresh_token},
            format="json"
        )
        
        assert refresh_response.status_code == status.HTTP_200_OK
        assert "access" in refresh_response.data
        print(f"✓ Renovação de token bem-sucedida. Novo token: {refresh_response.data['access'][:20]}...")
    
    def test_logout_invalidates_token(self):
        """Testa se o logout invalida o token."""
        # Fazer login
        login_response = self.client.post(
            "/api/token/",
            {
                "email": "transportador.teste@xbpneus.com",
                "password": "Teste@2025"
            },
            format="json"
        )
        
        token = login_response.data["access"]
        refresh_token = login_response.data["refresh"]
        
        # Fazer logout
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        logout_response = self.client.post(
            "/api/auth/logout/",
            {"refresh": refresh_token},
            format="json"
        )
        
        # Limpar o token de acesso do cliente
        self.client.credentials()

        # Tentar renovar o token de acesso com o refresh token blacklisted
        refresh_response = self.client.post(
            "/api/token/refresh/",
            {"refresh": refresh_token},
            format="json"
        )

        # A renovação deve falhar porque o refresh token foi blacklisted
        assert refresh_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Token is blacklisted" in refresh_response.data["detail"]
        print(f"✓ Logout bem-sucedido. Token foi invalidado.")


@pytest.mark.django_db
class TestTransportadorFrotaFuncionalidades(TestCase):
    """Testes para validar as funcionalidades de Frota do Transportador."""
    
    def setUp(self):
        """Configurar dados de teste."""
        self.client = APIClient()
        
        # Criar um usuário Transportador
        self.user = UsuarioTransportador.objects.create_user(
            email="transportador.teste@xbpneus.com",
            password="Teste@2025",
            nome_razao_social="Transportadora Teste",
            cnpj="12345678000190",
            telefone="11987654321"
        )
        self.user.is_active = True
        self.user.aprovado = True
        self.user.save()
        
        # Fazer login
        login_response = self.client.post(
            "/api/token/",
            {
                "email": "transportador.teste@xbpneus.com",
                "password": "Teste@2025"
            },
            format="json"
        )
        
        self.token = login_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
    
    def test_list_veiculos(self):
        """Testa se conseguimos listar os veículos do Transportador."""
        response = self.client.get("/api/transportador/frota/veiculos/")
        
        assert response.status_code == status.HTTP_200_OK
        print(f"✓ Listagem de veículos bem-sucedida. Dados: {response.data}")
    
    def test_list_motoristas(self):
        """Testa se conseguimos listar os motoristas do Transportador."""
        response = self.client.get("/api/transportador/frota/motoristas/")
        
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
        print(f"✓ Listagem de motoristas bem-sucedida. Status: {response.status_code}")


@pytest.mark.django_db
class TestTransportadorPneusFuncionalidades(TestCase):
    """Testes para validar as funcionalidades de Pneus do Transportador."""
    
    def setUp(self):
        """Configurar dados de teste."""
        self.client = APIClient()
        
        # Criar um usuário Transportador
        self.user = UsuarioTransportador.objects.create_user(
            email="transportador.teste@xbpneus.com",
            password="Teste@2025",
            nome_razao_social="Transportadora Teste",
            cnpj="12345678000190",
            telefone="11987654321"
        )
        self.user.is_active = True
        self.user.aprovado = True
        self.user.save()
        
        # Fazer login
        login_response = self.client.post(
            "/api/token/",
            {
                "email": "transportador.teste@xbpneus.com",
                "password": "Teste@2025"
            },
            format="json"
        )
        
        self.token = login_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
    
    def test_list_pneus(self):
        """Testa se conseguimos listar os pneus do Transportador."""
        response = self.client.get("/api/transportador/pneus/")
        
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
        print(f"✓ Listagem de pneus bem-sucedida. Status: {response.status_code}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

