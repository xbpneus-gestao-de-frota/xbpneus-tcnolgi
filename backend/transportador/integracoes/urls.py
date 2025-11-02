"""
URLs para o módulo de Integracoes
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IntegracaoExternaViewSet, LogIntegracaoViewSet, WebhookConfigViewSet, APICredentialViewSet

router = DefaultRouter()
router.register(r'integracaoexternas', IntegracaoExternaViewSet, basename='integracaoexterna')
router.register(r'logintegracaos', LogIntegracaoViewSet, basename='logintegracao')
router.register(r'webhookconfigs', WebhookConfigViewSet, basename='webhookconfig')
router.register(r'apicredentials', APICredentialViewSet, basename='apicredential')

urlpatterns = [
    path('', include(router.urls)),
]
