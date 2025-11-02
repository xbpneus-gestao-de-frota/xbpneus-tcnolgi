from rest_framework.routers import DefaultRouter
from .views import FornecedorViewSet, ContatoFornecedorViewSet

router = DefaultRouter()
router.register(r"fornecedores", FornecedorViewSet, basename="fornecedor")
router.register(r"contatos", ContatoFornecedorViewSet, basename="contato")

urlpatterns = router.urls
