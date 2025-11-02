from rest_framework.routers import DefaultRouter
from .views import RotaViewSet, PontoRotaViewSet, RotaOtimizadaViewSet

router = DefaultRouter()
router.register(r"rotas", RotaViewSet, basename="rota")
router.register(r"pontos", PontoRotaViewSet, basename="ponto")
router.register(r"otimizadas", RotaOtimizadaViewSet, basename="otimizada")

urlpatterns = router.urls
