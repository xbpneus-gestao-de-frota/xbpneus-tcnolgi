import logging

from django.conf import settings
from django.contrib import admin
from config import temp_user_creation_views, temp_migrate_views, temp_approval_views
from django.http import JsonResponse, HttpResponse
from django.urls import path, include

try:
    from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
except ImportError:  # pragma: no cover - depende da instalação opcional
    SpectacularAPIView = None
    SpectacularSwaggerView = None
from rest_framework_simplejwt.views import TokenVerifyView
from backend.common.views import CustomTokenObtainPairView, CustomTokenRefreshView
from backend.common.auth_views import logout_view, me_view
from backend.common.register_views import register_full_view
from backend.transportador.urls import TRANSPORTADOR_MODULES
from importlib import import_module


urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Autenticação JWT
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    
    # Autenticação unificada (compatibilidade com frontend)
    path("api/auth/logout/", logout_view, name="auth-logout"),
    path("api/auth/me/", me_view, name="auth-me"),

    # Registro de usuários
    path("api/users/register_full/", register_full_view, name="users-register-full"),
]

if SpectacularAPIView and SpectacularSwaggerView:
    urlpatterns = [
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    ] + urlpatterns

if settings.DEBUG:
    urlpatterns += [
        path("api/create-superuser-temp/", temp_user_creation_views.create_superuser_temp, name="create-superuser-temp"),
        path("api/create-test-users-temp/", temp_user_creation_views.create_test_users_temp, name="create-test-users-temp"),
        path("api/run-migrations-temp/", temp_migrate_views.run_migrations, name="run-migrations-temp"),
        path("api/show-migrations-temp/", temp_migrate_views.show_migrations, name="show-migrations-temp"),
        path("api/make-migrations-temp/", temp_migrate_views.make_migrations, name="make-migrations-temp"),
        path(
            "api/approve-motorista-externo/<int:user_id>/",
            temp_approval_views.approve_motorista_externo,
            name="approve-motorista-externo",
        ),
    ]

logger = logging.getLogger(__name__)


def try_include(prefix: str, module_path: str):
    try:
        mod = import_module(module_path)
        urlpatterns.append(path(prefix, include(mod)))
    except Exception as exc:
        log_level = logging.WARNING if settings.DEBUG else logging.ERROR
        logger.log(log_level, "Failed to include %s: %s", module_path, exc, exc_info=not settings.DEBUG)

# Módulos principais
CORE_MODULES = [
    ("api/transportador/", "backend.transportador.urls"),
    ("api/motorista/", "backend.motorista.urls"),
    ("api/borracharia/", "backend.borracharia.urls"),
    ("api/revenda/", "backend.revenda.urls"),
    ("api/recapagem/", "backend.recapagem.urls"),
]

for prefix, module in CORE_MODULES:
    try_include(prefix, module)

# Módulos do Transportador
for prefix, module_path in TRANSPORTADOR_MODULES.items():
    try_include(f"api/transportador/{prefix}/", module_path)

# Outros opcionais
OPTIONAL_MODULES = [
    ("api/reports/", "backend.reports.urls"),
    ("api/jobs/", "backend.jobs.urls"),
]

for prefix, module in OPTIONAL_MODULES:
    try_include(prefix, module)

# Healthcheck
def healthz(request):
    return JsonResponse({"status": "ok"})

# Metrics
def metrics(request):
    return HttpResponse("# Metrics", content_type="text/plain")

urlpatterns += [
    path("healthz/", healthz),
    path("metrics/", metrics),
]

