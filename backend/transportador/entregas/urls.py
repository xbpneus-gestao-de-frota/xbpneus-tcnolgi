from rest_framework.routers import DefaultRouter
from .views import EntregaViewSet, PODViewSet, OcorrenciaViewSet, TentativaViewSet

router = DefaultRouter()
router.register(r"entregas", EntregaViewSet, basename="entrega")
router.register(r"pods", PODViewSet, basename="pod")
router.register(r"ocorrencias", OcorrenciaViewSet, basename="ocorrencia")
router.register(r"tentativas", TentativaViewSet, basename="tentativa")

urlpatterns = router.urls
