from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .motorista_externo_views import MotoristaExternoProfileViewSet, MotoristaExternoAlocacaoViewSet, motorista_externo_me, motorista_externo_dashboard, MotoristaExternoActionViewSet

router = DefaultRouter()
router.register(r'perfil-externo', MotoristaExternoProfileViewSet, basename='motorista-externo-perfil')
router.register(r'alocacoes-externo', MotoristaExternoAlocacaoViewSet, basename='motorista-externo-alocacoes')
router.register(r'acoes-externo', MotoristaExternoActionViewSet, basename='motorista-externo-acoes')

urlpatterns = [
    path('me-externo/', motorista_externo_me, name='motorista-externo-me'),
    path('dashboard/', motorista_externo_dashboard, name='motorista-externo-dashboard'),
    path('', include(router.urls)),
]

