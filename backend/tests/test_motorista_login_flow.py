from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from backend.motorista.models import UsuarioMotorista


class MotoristaLoginFlowTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_motorista_login_returns_tokens_and_redirect(self):
        user = UsuarioMotorista.objects.create_user(
            email="motorista.ativo@example.com",
            password="SenhaSegura123",
            nome_completo="Motorista Ativo",
            cpf="12345678901",
            cnh="99887766554",
            categoria_cnh="D",
            telefone="(11) 99999-9999",
            aprovado=True,
            is_active=True,
            aprovado_em=timezone.now(),
            aprovado_por="admin@example.com",
        )

        response = self.client.post(
            "/api/motorista/login/",
            {"email": "motorista.ativo@example.com", "password": "SenhaSegura123"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("tokens", response.data)
        self.assertIn("redirect", response.data)

        tokens = response.data["tokens"]
        self.assertIn("access", tokens)
        self.assertIn("refresh", tokens)

        access_token = AccessToken(tokens["access"])
        self.assertEqual(access_token["user_id"], user.id)
        self.assertEqual(access_token["user_role"], "motorista")
        self.assertEqual(response.data["redirect"], "/motorista/dashboard/")

    def test_motorista_login_requires_approval(self):
        UsuarioMotorista.objects.create_user(
            email="motorista.pendente@example.com",
            password="SenhaSegura123",
            nome_completo="Motorista Pendente",
            cpf="55566677788",
            cnh="11223344556",
            categoria_cnh="C",
            telefone="(11) 98888-7777",
            aprovado=False,
            is_active=False,
        )

        response = self.client.post(
            "/api/motorista/login/",
            {"email": "motorista.pendente@example.com", "password": "SenhaSegura123"},
            format="json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertIn("Seu cadastro ainda não foi aprovado", response.data["error"])
