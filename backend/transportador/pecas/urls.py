"""
URLs para o módulo de Pecas
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaPecaViewSet, PecaViewSet, EstoquePecaViewSet, MovimentacaoPecaViewSet, FornecedorPecaViewSet

router = DefaultRouter()
router.register(r'categoriapecas', CategoriaPecaViewSet, basename='categoriapeca')
router.register(r'pecas', PecaViewSet, basename='peca')
router.register(r'estoquepecas', EstoquePecaViewSet, basename='estoquepeca')
router.register(r'movimentacaopecas', MovimentacaoPecaViewSet, basename='movimentacaopeca')
router.register(r'fornecedorpecas', FornecedorPecaViewSet, basename='fornecedorpeca')

urlpatterns = [
    path('', include(router.urls)),
]
