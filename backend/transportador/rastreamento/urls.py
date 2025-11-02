from rest_framework.routers import DefaultRouter
from .views import PosicaoViewSet, CercaEletronicaViewSet, ViolacaoCercaViewSet, HistoricoRastreamentoViewSet

router = DefaultRouter()
router.register(r"posicoes", PosicaoViewSet, basename="posicao")
router.register(r"cercas", CercaEletronicaViewSet, basename="cerca")
router.register(r"violacoes", ViolacaoCercaViewSet, basename="violacao")
router.register(r"historico", HistoricoRastreamentoViewSet, basename="historico")

urlpatterns = router.urls
