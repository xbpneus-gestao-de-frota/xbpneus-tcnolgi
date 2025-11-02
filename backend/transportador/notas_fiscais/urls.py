"""
URLs para o módulo de Notas Fiscais
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NotaFiscalViewSet,
    ItemNotaFiscalViewSet,
    ImpostoNotaFiscalViewSet,
    AnexoNotaFiscalViewSet
)

router = DefaultRouter()
router.register(r'notas-fiscais', NotaFiscalViewSet, basename='notafiscal')
router.register(r'itens', ItemNotaFiscalViewSet, basename='itemnotafiscal')
router.register(r'impostos', ImpostoNotaFiscalViewSet, basename='impostonotafiscal')
router.register(r'anexos', AnexoNotaFiscalViewSet, basename='anexonotafiscal')

urlpatterns = [
    path('', include(router.urls)),
]
