from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaProdutoViewSet, ProdutoViewSet, PedidoViewSet,
    ItemPedidoViewSet, MovimentacaoEstoqueLojaViewSet
)

router = DefaultRouter()
router.register(r"categorias", CategoriaProdutoViewSet, basename="categoria")
router.register(r"produtos", ProdutoViewSet, basename="produto")
router.register(r"pedidos", PedidoViewSet, basename="pedido")
router.register(r"itens-pedido", ItemPedidoViewSet, basename="item-pedido")
router.register(r"movimentacoes", MovimentacaoEstoqueLojaViewSet, basename="movimentacao")

urlpatterns = router.urls
