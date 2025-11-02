from django.contrib import admin
from config import temp_user_creation_views, temp_migrate_views, temp_approval_views
from django.http import JsonResponse, HttpResponse
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenVerifyView
from backend.common.views import CustomTokenObtainPairView, CustomTokenRefreshView
from backend.common.auth_views import logout_view, me_view
from backend.common.register_views import register_full_view
from backend.transportador.urls import TRANSPORTADOR_MODULES
from importlib import import_module

urlpatterns = [
    path("api/create-superuser-temp/", temp_user_creation_views.create_superuser_temp, name="create-superuser-temp"),
    path("api/create-test-users-temp/", temp_user_creation_views.create_test_users_temp, name="create-test-users-temp"),
    path("api/run-migrations-temp/", temp_migrate_views.run_migrations, name="run-migrations-temp"),
    path("api/show-migrations-temp/", temp_migrate_views.show_migrations, name="show-migrations-temp"),
    path("api/make-migrations-temp/", temp_migrate_views.make_migrations, name="make-migrations-temp"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
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
    path("api/approve-motorista-externo/<int:user_id>/", temp_approval_views.approve_motorista_externo, name="approve-motorista-externo"),

    path('api/borracharia/', include('borracharia.urls')),
    path('api/jobs/', include('jobs.urls')),
    path('api/motorista/', include('motorista.urls')),
    path('api/recapagem/', include('recapagem.urls')),
    path('api/reports/', include('reports.urls')),
    path('api/revenda/', include('revenda.urls')),
    path('api/alertas/', include('alertas.urls')),
    path('api/almoxarifado/', include('almoxarifado.urls')),
    path('api/cargas/', include('cargas.urls')),
    path('api/clientes/', include('clientes.urls')),
    path('api/combustivel/', include('combustivel.urls')),
    path('api/compliance/', include('compliance.urls')),
    path('api/configuracoes/', include('configuracoes.urls')),
    path('api/contratos/', include('contratos.urls')),
    path('api/custos/', include('custos.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/dashboards/', include('dashboards.urls')),
    path('api/documentos/', include('documentos.urls')),
    path('api/empresas/', include('empresas.urls')),
    path('api/entregas/', include('entregas.urls')),
    path('api/epis/', include('epis.urls')),
    path('api/estoque/', include('estoque.urls')),
    path('api/faturamento/', include('faturamento.urls')),
    path('api/ferramentas/', include('ferramentas.urls')),
    path('api/fornecedores/', include('fornecedores.urls')),
    path('api/frota/', include('frota.urls')),
    path('api/ia_pneus/', include('ia_pneus.urls')),
    path('api/integracoes/', include('integracoes.urls')),
    path('api/loja/', include('loja.urls')),
    path('api/manutencao/', include('manutencao.urls')),
    path('api/motorista_externo/', include('motorista_externo.urls')),
    path('api/motorista_interno/', include('motorista_interno.urls')),
    path('api/multas/', include('multas.urls')),
    path('api/notificacoes/', include('notificacoes.urls')),
    path('api/pagamentos/', include('pagamentos.urls')),
    path('api/pecas/', include('pecas.urls')),
    path('api/pneus/', include('pneus.urls')),
    path('api/rastreamento/', include('rastreamento.urls')),
    path('api/relatorios/', include('relatorios.urls')),
    path('api/rotas/', include('rotas.urls')),
    path('api/seguros/', include('seguros.urls')),
    path('api/telemetria/', include('telemetria.urls')),
    path('api/transportador_financeiro/', include('transportador_financeiro.urls')),
    path('api/transportador_motorista/', include('transportador_motorista.urls')),
    path('api/transportador_relatorios/', include('transportador_relatorios.urls')),
    path('api/transportador_tr/', include('transportador_tr.urls')),
    path('api/treinamentos/', include('treinamentos.urls')),
    path('api/viagens/', include('viagens.urls')),
    path('api/admindocs/', include('admindocs.urls')),
    path('api/auth/', include('auth.urls')),
    path('api/flatpages/', include('flatpages.urls')),
    path('api/staticfiles/', include('staticfiles.urls')),
    path('api/django_rq/', include('django_rq.urls')),
    path('api/rest_framework/', include('rest_framework.urls')),
]

def try_include(prefix: str, module_path: str):
    try:
        mod = import_module(module_path)
        urlpatterns.append(path(prefix, include(mod)))
    except Exception as e:
        import logging
        logging.warning(f"Failed to include {module_path}: {e}")

# Módulos principais
try_include("api/transportador/", "backend.transportador.urls")
try_include("api/motorista/", "backend.motorista.urls") # Rotas de login/cadastro removidas. Apenas perfil e rotas externas permanecem.
try_include("api/borracharia/", "backend.borracharia.urls")
try_include("api/revenda/", "backend.revenda.urls")
try_include("api/recapagem/", "backend.recapagem.urls")

# Módulos do Transportador
for prefix, module_path in TRANSPORTADOR_MODULES.items():
    try_include(f"api/transportador/{prefix}/", module_path)

# Outros
try_include("api/reports/", "backend.reports.urls")
try_include("api/jobs/", "backend.jobs.urls")

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

