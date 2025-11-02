"""
URLs para o módulo de Compliance
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NormaComplianceViewSet, AuditoriaComplianceViewSet, NaoConformidadeViewSet, PlanoAcaoComplianceViewSet

router = DefaultRouter()
router.register(r'normacompliances', NormaComplianceViewSet, basename='normacompliance')
router.register(r'auditoriacompliances', AuditoriaComplianceViewSet, basename='auditoriacompliance')
router.register(r'naoconformidades', NaoConformidadeViewSet, basename='naoconformidade')
router.register(r'planoacaocompliances', PlanoAcaoComplianceViewSet, basename='planoacaocompliance')

urlpatterns = [
    path('', include(router.urls)),
]
