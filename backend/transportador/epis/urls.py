"""
URLs para o módulo de Epis
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TipoEPIViewSet, EPIViewSet, EntregaEPIViewSet, FichaEPIViewSet

router = DefaultRouter()
router.register(r'tipoepis', TipoEPIViewSet, basename='tipoepi')
router.register(r'epis', EPIViewSet, basename='epi')
router.register(r'entregaepis', EntregaEPIViewSet, basename='entregaepi')
router.register(r'fichaepis', FichaEPIViewSet, basename='fichaepi')

urlpatterns = [
    path('', include(router.urls)),
]
