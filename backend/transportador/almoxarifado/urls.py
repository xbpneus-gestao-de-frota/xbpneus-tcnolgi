"""
URLs para o módulo de Almoxarifado
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AlmoxarifadoViewSet, LocalEstoqueViewSet, MovimentacaoAlmoxarifadoViewSet,
    InventarioAlmoxarifadoViewSet, ItemInventarioViewSet,
    RequisicaoMaterialViewSet, ItemRequisicaoViewSet
)

router = DefaultRouter()
router.register(r'almoxarifados', AlmoxarifadoViewSet, basename='almoxarifado')
router.register(r'locais-estoque', LocalEstoqueViewSet, basename='localestoque')
router.register(r'movimentacoes', MovimentacaoAlmoxarifadoViewSet, basename='movimentacao')
router.register(r'inventarios', InventarioAlmoxarifadoViewSet, basename='inventario')
router.register(r'itens-inventario', ItemInventarioViewSet, basename='iteminventario')
router.register(r'requisicoes', RequisicaoMaterialViewSet, basename='requisicao')
router.register(r'itens-requisicao', ItemRequisicaoViewSet, basename='itemrequisicao')

urlpatterns = [
    path('', include(router.urls)),
]
