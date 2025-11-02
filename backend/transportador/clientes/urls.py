from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, ContatoClienteViewSet

router = DefaultRouter()
router.register(r"clientes", ClienteViewSet, basename="cliente")
router.register(r"contatos", ContatoClienteViewSet, basename="contato")

urlpatterns = router.urls
