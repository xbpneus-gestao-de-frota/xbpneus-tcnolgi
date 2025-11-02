from rest_framework.routers import DefaultRouter
from .views import (
    MotoristaInternoViewSet, VinculoMotoristaVeiculoViewSet,
    RegistroJornadaViewSet, MensagemMotoristaViewSet, AlertaMotoristaViewSet
)

router = DefaultRouter()
router.register(r"motoristas", MotoristaInternoViewSet, basename="motorista")
router.register(r"vinculos", VinculoMotoristaVeiculoViewSet, basename="vinculo")
router.register(r"jornadas", RegistroJornadaViewSet, basename="jornada")
router.register(r"mensagens", MensagemMotoristaViewSet, basename="mensagem")
router.register(r"alertas", AlertaMotoristaViewSet, basename="alerta")

urlpatterns = router.urls
