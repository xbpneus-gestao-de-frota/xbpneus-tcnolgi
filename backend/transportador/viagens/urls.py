from rest_framework.routers import DefaultRouter
from .views import ViagemViewSet, CargaViewSet, ParadaViewSet

router = DefaultRouter()
router.register(r"viagens", ViagemViewSet, basename="viagem")
router.register(r"cargas", CargaViewSet, basename="carga")
router.register(r"paradas", ParadaViewSet, basename="parada")

urlpatterns = router.urls
