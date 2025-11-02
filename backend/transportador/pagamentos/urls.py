from rest_framework.routers import DefaultRouter
from .views import ContaPagarViewSet, ContaReceberViewSet, PagamentoViewSet

router = DefaultRouter()
router.register(r"contas-pagar", ContaPagarViewSet, basename="conta-pagar")
router.register(r"contas-receber", ContaReceberViewSet, basename="conta-receber")
router.register(r"pagamentos", PagamentoViewSet, basename="pagamento")

urlpatterns = router.urls
