"""
URLs para o módulo de Manutenção
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework.routers import DefaultRouter
from .views import (
    OrdemServicoViewSet, ItemOSViewSet, ChecklistManutencaoViewSet,
    PlanoManutencaoPreventivaViewSet, HistoricoManutencaoViewSet,
    WorkOrderViewSet, TesteViewSet
)

router = DefaultRouter()

# Endpoints novos (100% completos)
router.register(r"ordens-servico", OrdemServicoViewSet, basename="ordem-servico")
router.register(r"itens-os", ItemOSViewSet, basename="item-os")
router.register(r"checklists", ChecklistManutencaoViewSet, basename="checklist")
router.register(r"planos-preventiva", PlanoManutencaoPreventivaViewSet, basename="plano-preventiva")
router.register(r"historico", HistoricoManutencaoViewSet, basename="historico")

# Endpoints legados (compatibilidade)
router.register(r"os", WorkOrderViewSet, basename="os")
router.register(r"testes", TesteViewSet, basename="teste")

urlpatterns = router.urls
