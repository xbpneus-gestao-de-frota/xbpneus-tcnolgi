"""
URLs para o módulo de Relatorios
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RelatorioTemplateViewSet, RelatorioAgendadoViewSet, RelatorioGeradoViewSet, DashboardPersonalizadoViewSet

router = DefaultRouter()
router.register(r'relatoriotemplates', RelatorioTemplateViewSet, basename='relatoriotemplate')
router.register(r'relatorioagendados', RelatorioAgendadoViewSet, basename='relatorioagendado')
router.register(r'relatoriogerados', RelatorioGeradoViewSet, basename='relatoriogerado')
router.register(r'dashboardpersonalizados', DashboardPersonalizadoViewSet, basename='dashboardpersonalizado')

urlpatterns = [
    path('', include(router.urls)),
]
