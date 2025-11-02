from rest_framework.routers import DefaultRouter
from .views import CategoriaCustoViewSet, CustoViewSet, CustoPorKmViewSet

router = DefaultRouter()
router.register(r"categorias", CategoriaCustoViewSet, basename="categoria")
router.register(r"custos", CustoViewSet, basename="custo")
router.register(r"custo-por-km", CustoPorKmViewSet, basename="custo-km")

urlpatterns = router.urls
