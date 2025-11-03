from rest_framework.routers import DefaultRouter

from .views import (
    ApplicationViewSet,
    MedicaoPneuViewSet,
    MovimentacaoPneuViewSet,
    TireViewSet,
)


router = DefaultRouter()
router.register(r"pneus", TireViewSet, basename="tire")
router.register(r"aplicacoes", ApplicationViewSet, basename="application")
router.register(r"movimentacoes", MovimentacaoPneuViewSet, basename="movimentacaopneu")
router.register(r"medicoes", MedicaoPneuViewSet, basename="medicaopneu")

urlpatterns = router.urls
