"""
URLs para o módulo de Alertas
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TipoAlertaViewSet, AlertaViewSet, ConfiguracaoAlertaViewSet, HistoricoAlertaViewSet

router = DefaultRouter()
router.register(r'tipoalertas', TipoAlertaViewSet, basename='tipoalerta')
router.register(r'alertas', AlertaViewSet, basename='alerta')
router.register(r'configuracaoalertas', ConfiguracaoAlertaViewSet, basename='configuracaoalerta')
router.register(r'historicoalertas', HistoricoAlertaViewSet, basename='historicoalerta')

urlpatterns = [
    path('', include(router.urls)),
]
