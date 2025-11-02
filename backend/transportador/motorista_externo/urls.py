from rest_framework.routers import DefaultRouter
from .views import MotoristaExternoViewSet, AlocacaoMotoristaViewSet

router = DefaultRouter()
router.register(r'motoristas-externos', MotoristaExternoViewSet)
router.register(r'alocacoes-motorista', AlocacaoMotoristaViewSet)

urlpatterns = router.urls

