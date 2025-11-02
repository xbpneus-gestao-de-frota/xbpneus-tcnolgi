from rest_framework.routers import DefaultRouter
from .views import DispositivoViewSet, LeituraViewSet, AlertaViewSet

router = DefaultRouter()
router.register(r"dispositivos", DispositivoViewSet, basename="dispositivo")
router.register(r"leituras", LeituraViewSet, basename="leitura")
router.register(r"alertas", AlertaViewSet, basename="alerta")

urlpatterns = router.urls
