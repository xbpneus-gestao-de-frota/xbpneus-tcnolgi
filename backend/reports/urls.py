
from django.urls import path
from .views import MedicoesPorPosicao, CustosPorOS, GiroEstoque, CustosPorPosicao

urlpatterns = [
    path("manutencao/custos_por_posicao/", CustosPorPosicao.as_view()),
    path("pneus/medicoes_por_posicao/", MedicoesPorPosicao.as_view()),
    path("manutencao/custos_por_os/", CustosPorOS.as_view()),
    path("estoque/giro/", GiroEstoque.as_view()),
]
