from rest_framework.routers import DefaultRouter
from .views import VehicleViewSet, PositionViewSet

router = DefaultRouter()
router.register(r"veiculos", VehicleViewSet, basename="veiculo")
router.register(r"posicoes", PositionViewSet, basename="posicao")
urlpatterns = router.urls
