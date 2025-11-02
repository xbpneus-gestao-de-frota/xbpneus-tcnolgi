"""
URLs para o módulo de Configuracoes
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ConfiguracaoSistemaViewSet,
    ParametroEmpresaViewSet,
    PerfilUsuarioViewSet,
    PermissaoCustomizadaViewSet,
    CatalogoModeloVeiculoViewSet,
    MapaPosicaoPneuViewSet,
    OperacaoConfiguracaoViewSet,
    MedidaPorPosicaoViewSet,
    PressaoRecomendadaViewSet,
    CatalogoPneuXBRIViewSet
)

router = DefaultRouter()
router.register(r'configuracaosistemas', ConfiguracaoSistemaViewSet, basename='configuracaosistema')
router.register(r'parametroempresas', ParametroEmpresaViewSet, basename='parametroempresa')
router.register(r'perfilusuarios', PerfilUsuarioViewSet, basename='perfilusuario')
router.register(r'permissaocustomizadas', PermissaoCustomizadaViewSet, basename='permissaocustomizada')

# Rotas para tabelas auxiliares (somente leitura)
router.register(r'catalogo-modelos-veiculos', CatalogoModeloVeiculoViewSet, basename='catalogo-modelo-veiculo')
router.register(r'mapa-posicoes-pneus', MapaPosicaoPneuViewSet, basename='mapa-posicao-pneu')
router.register(r'operacoes-configuracoes', OperacaoConfiguracaoViewSet, basename='operacao-configuracao')
router.register(r'medidas-por-posicao', MedidaPorPosicaoViewSet, basename='medida-por-posicao')
router.register(r'pressoes-recomendadas', PressaoRecomendadaViewSet, basename='pressao-recomendada')
router.register(r'catalogo-pneus-xbri', CatalogoPneuXBRIViewSet, basename='catalogo-pneu-xbri')

urlpatterns = [
    path('', include(router.urls)),
]
