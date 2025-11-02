from rest_framework.routers import DefaultRouter
from .views import SeguradoraViewSet, ApoliceViewSet, SinistroViewSet

router = DefaultRouter()
router.register(r"seguradoras", SeguradoraViewSet, basename="seguradora")
router.register(r"apolices", ApoliceViewSet, basename="apolice")
router.register(r"sinistros", SinistroViewSet, basename="sinistro")

urlpatterns = router.urls
