"""
URLs para o módulo de Auditoria
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LogAuditoriaViewSet,
    LogAcessoViewSet,
    LogAlteracaoViewSet,
    SessaoUsuarioViewSet,
    ConfiguracaoAuditoriaViewSet
)

router = DefaultRouter()
router.register(r'logs-auditoria', LogAuditoriaViewSet, basename='logauditoria')
router.register(r'logs-acesso', LogAcessoViewSet, basename='logacesso')
router.register(r'logs-alteracao', LogAlteracaoViewSet, basename='logalteracao')
router.register(r'sessoes', SessaoUsuarioViewSet, basename='sessaousuario')
router.register(r'configuracoes', ConfiguracaoAuditoriaViewSet, basename='configuracaoauditoria')

urlpatterns = [
    path('', include(router.urls)),
]
