from rest_framework.routers import DefaultRouter
from .views import ContratoViewSet, AditivoViewSet

router = DefaultRouter()
router.register(r"contratos", ContratoViewSet, basename="contrato")
router.register(r"aditivos", AditivoViewSet, basename="aditivo")

urlpatterns = router.urls
