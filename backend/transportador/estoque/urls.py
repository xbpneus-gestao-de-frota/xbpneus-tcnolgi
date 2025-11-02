"""
URLs expandidas para o módulo de Estoque
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaProdutoViewSet, ProdutoViewSet, SaldoEstoqueViewSet,
    MovimentacaoEstoqueViewSet, PrevisaoDemandaViewSet, CurvaABCViewSet
)

router = DefaultRouter()
router.register(r'categorias', CategoriaProdutoViewSet, basename='categoriaproduto')
router.register(r'produtos', ProdutoViewSet, basename='produto')
router.register(r'saldos', SaldoEstoqueViewSet, basename='saldoestoque')
router.register(r'movimentacoes', MovimentacaoEstoqueViewSet, basename='movimentacaoestoque')
router.register(r'previsoes-demanda', PrevisaoDemandaViewSet, basename='previsaodemanda')
router.register(r'curva-abc', CurvaABCViewSet, basename='curvaabc')

urlpatterns = [
    path('', include(router.urls)),
]
