"""Rotas principais do módulo Transportador."""
from collections import OrderedDict
import logging

from django.urls import include, path

from . import views
from .dashboard_views import dashboard_view, dashboard_stats_view, profile_view, me_view
from .dashboard.views import MetricsView

logger = logging.getLogger(__name__)

TRANSPORTADOR_MODULES = OrderedDict([
    ("motorista-externo", "backend.transportador.motorista_externo.urls"),
    ("motorista-interno", "backend.transportador.motorista_interno.urls"),
    ("frota", "backend.transportador.frota.urls"),
    ("pneus", "backend.transportador.pneus.urls"),
    ("manutencao", "backend.transportador.manutencao.urls"),
    ("estoque", "backend.transportador.estoque.urls"),
    ("loja", "backend.transportador.loja.urls"),
    ("custos", "backend.transportador.custos.urls"),
    ("combustivel", "backend.transportador.combustivel.urls"),
    ("multas", "backend.transportador.multas.urls"),
    ("documentos", "backend.transportador.documentos.urls"),
    ("viagens", "backend.transportador.viagens.urls"),
    ("clientes", "backend.transportador.clientes.urls"),
    ("fornecedores", "backend.transportador.fornecedores.urls"),
    ("seguros", "backend.transportador.seguros.urls"),
    ("contratos", "backend.transportador.contratos.urls"),
    ("faturamento", "backend.transportador.faturamento.urls"),
    ("pagamentos", "backend.transportador.pagamentos.urls"),
    ("telemetria", "backend.transportador.telemetria.urls"),
    ("rastreamento", "backend.transportador.rastreamento.urls"),
    ("rotas", "backend.transportador.rotas.urls"),
    ("entregas", "backend.transportador.entregas.urls"),
    ("dashboards", "backend.transportador.dashboards.urls"),
    ("notificacoes", "backend.transportador.notificacoes.urls"),
    ("almoxarifado", "backend.transportador.almoxarifado.urls"),
    ("relatorios", "backend.transportador.relatorios.urls"),
    ("cargas", "backend.transportador.cargas.urls"),
    ("pecas", "backend.transportador.pecas.urls"),
    ("ferramentas", "backend.transportador.ferramentas.urls"),
    ("epis", "backend.transportador.epis.urls"),
    ("treinamentos", "backend.transportador.treinamentos.urls"),
    ("compliance", "backend.transportador.compliance.urls"),
    ("alertas", "backend.transportador.alertas.urls"),
    ("integracoes", "backend.transportador.integracoes.urls"),
    ("configuracoes", "backend.transportador.configuracoes.urls"),
    ("empresas", "backend.transportador.empresas.urls"),
    ("financeiro", "backend.transportador.transportador_financeiro.urls"),
    ("motorista", "backend.transportador.transportador_motorista.urls"),
    ("relatorios_transportador", "backend.transportador.transportador_relatorios.urls"),
    ("tr", "backend.transportador.transportador_tr.urls"),
    ("implemento", "backend.transportador.implemento.urls"),
    ("analise_pneus", "backend.transportador.analise_pneus.urls"),
    ("garantias", "backend.transportador.garantias.urls"),
    ("auditoria", "backend.transportador.auditoria.urls"),
    ("notas_fiscais", "backend.transportador.notas_fiscais.urls"),
    ("ia", "backend.transportador.ia_pneus.urls"),
])

urlpatterns = [
    path("register/", views.registro_transportador, name="transportador-register"),
    path("login/", views.login_transportador, name="transportador-login"),
    path("logout/", views.logout_transportador, name="transportador-logout"),
    path("perfil/", views.perfil_transportador, name="transportador-perfil"),
    path("dashboard/", dashboard_view, name="transportador-dashboard"),
    path("dashboard/metrics/", MetricsView.as_view(), name="transportador-dashboard-metrics"),
    path("dashboard/stats/", dashboard_stats_view, name="transportador-dashboard-stats"),
    path("profile/", profile_view, name="transportador-profile"),
    path("me/", me_view, name="transportador-me"),
]


def include_optional(prefix: str, module_path: str) -> None:
    """Adiciona includes opcionais, registrando logs quando o módulo não existe."""
    try:
        urlpatterns.append(path(f"{prefix}/", include(module_path)))
    except Exception as exc:  # pragma: no cover - log defensivo
        logger.warning("Falha ao incluir %s: %s", module_path, exc)


for route_prefix, module_path in TRANSPORTADOR_MODULES.items():
    include_optional(route_prefix, module_path)


__all__ = ["TRANSPORTADOR_MODULES", "urlpatterns"]
