import os

import django
import pytest
from django.test import TransactionTestCase
from django.test.runner import DiscoverRunner
from django.test.utils import teardown_test_environment


# Garante que o Django está configurado para os testes
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()
except RuntimeError:
    # O Django já pode ter sido inicializado por outro processo de testes
    pass

from rest_framework.test import APIClient  # noqa: E402
from django.contrib.auth import get_user_model  # noqa: E402

from backend.common.jwt_utils import create_tokens_for_user  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def django_test_environment(request):
    runner = DiscoverRunner(verbosity=0, interactive=False, keepdb=True)
    old_config = runner.setup_databases()
    test_env_initialized = False
    try:
        runner.setup_test_environment()
        test_env_initialized = True
    except RuntimeError:
        try:
            teardown_test_environment()
        except Exception:
            pass
        runner.setup_test_environment()
        test_env_initialized = True

    def teardown():
        if test_env_initialized:
            try:
                runner.teardown_test_environment()
            except AttributeError:
                pass
        runner.teardown_databases(old_config)

    request.addfinalizer(teardown)
    return runner


@pytest.fixture
def db(django_test_environment):
    test_case = TransactionTestCase(methodName='__init__')
    test_case._pre_setup()
    try:
        yield
    finally:
        test_case._post_teardown()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(
        email="tester@xbpneus.com",
        password="pass123",
        nome_razao_social="Tester User",
        cnpj="12345678000100",
        telefone="(11) 99999-9999",
        is_active=True,
        aprovado=True,
    )


@pytest.fixture
def client_auth(user):
    client = APIClient()
    tokens = create_tokens_for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
    return client
