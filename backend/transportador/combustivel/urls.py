from rest_framework.routers import DefaultRouter
from .views import PostoCombustivelViewSet, AbastecimentoViewSet, ConsumoMensalViewSet

router = DefaultRouter()
router.register(r"postos", PostoCombustivelViewSet, basename="posto")
router.register(r"abastecimentos", AbastecimentoViewSet, basename="abastecimento")
router.register(r"consumo-mensal", ConsumoMensalViewSet, basename="consumo-mensal")

urlpatterns = router.urls
