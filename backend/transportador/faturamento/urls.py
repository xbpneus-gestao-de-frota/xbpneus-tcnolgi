from rest_framework.routers import DefaultRouter
from .views import FaturaViewSet, ItemFaturaViewSet, NotaFiscalViewSet

router = DefaultRouter()
router.register(r"faturas", FaturaViewSet, basename="fatura")
router.register(r"itens", ItemFaturaViewSet, basename="item")
router.register(r"notas-fiscais", NotaFiscalViewSet, basename="nota-fiscal")

urlpatterns = router.urls
