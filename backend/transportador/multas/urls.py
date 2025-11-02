from rest_framework.routers import DefaultRouter
from .views import MultaViewSet, RecursoMultaViewSet, PontuacaoCNHViewSet

router = DefaultRouter()
router.register(r"multas", MultaViewSet, basename="multa")
router.register(r"recursos", RecursoMultaViewSet, basename="recurso")
router.register(r"pontuacao-cnh", PontuacaoCNHViewSet, basename="pontuacao")

urlpatterns = router.urls
