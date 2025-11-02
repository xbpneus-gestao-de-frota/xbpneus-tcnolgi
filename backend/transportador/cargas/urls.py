"""
URLs para o módulo de Cargas
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TipoCargaViewSet, CargaViewSet, ItemCargaViewSet, ManifestoCargaViewSet, RastreamentoCargaViewSet

router = DefaultRouter()
router.register(r'tipocargas', TipoCargaViewSet, basename='tipocarga')
router.register(r'cargas', CargaViewSet, basename='carga')
router.register(r'itemcargas', ItemCargaViewSet, basename='itemcarga')
router.register(r'manifestocargas', ManifestoCargaViewSet, basename='manifestocarga')
router.register(r'rastreamentocargas', RastreamentoCargaViewSet, basename='rastreamentocarga')

urlpatterns = [
    path('', include(router.urls)),
]
