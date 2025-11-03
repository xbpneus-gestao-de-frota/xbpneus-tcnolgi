from rest_framework.routers import DefaultRouter
from .views import FleetAnalysisViewSet, PositionViewSet, VehicleViewSet

router = DefaultRouter()
router.register(r"veiculos", VehicleViewSet, basename="veiculo")
router.register(r"posicoes", PositionViewSet, basename="posicao")
router.register(r"analise", FleetAnalysisViewSet, basename="frota-analise")
urlpatterns = router.urls
