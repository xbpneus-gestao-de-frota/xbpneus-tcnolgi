"""
URLs para o módulo de Ferramentas
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FerramentaViewSet, EmprestimoFerramentaViewSet, ManutencaoFerramentaViewSet, CalibracaoFerramentaViewSet

router = DefaultRouter()
router.register(r'ferramentas', FerramentaViewSet, basename='ferramenta')
router.register(r'emprestimoferramentas', EmprestimoFerramentaViewSet, basename='emprestimoferramenta')
router.register(r'manutencaoferramentas', ManutencaoFerramentaViewSet, basename='manutencaoferramenta')
router.register(r'calibracaoferramentas', CalibracaoFerramentaViewSet, basename='calibracaoferramenta')

urlpatterns = [
    path('', include(router.urls)),
]
