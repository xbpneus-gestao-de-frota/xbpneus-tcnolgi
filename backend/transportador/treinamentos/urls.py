"""
URLs para o módulo de Treinamentos
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CursoTreinamentoViewSet, TreinamentoRealizadoViewSet, CertificadoTreinamentoViewSet, InstrutorTreinamentoViewSet

router = DefaultRouter()
router.register(r'cursotreinamentos', CursoTreinamentoViewSet, basename='cursotreinamento')
router.register(r'treinamentorealizados', TreinamentoRealizadoViewSet, basename='treinamentorealizado')
router.register(r'certificadotreinamentos', CertificadoTreinamentoViewSet, basename='certificadotreinamento')
router.register(r'instrutortreinamentos', InstrutorTreinamentoViewSet, basename='instrutortreinamento')

urlpatterns = [
    path('', include(router.urls)),
]
