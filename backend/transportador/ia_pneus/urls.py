from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnaliseIAViewSet, GamificacaoViewSet, GarantiaViewSet

router = DefaultRouter()
router.register(r'analises', AnaliseIAViewSet, basename='analise')
router.register(r'gamificacao', GamificacaoViewSet, basename='gamificacao')
router.register(r'garantias', GarantiaViewSet, basename='garantia')

urlpatterns = [
    path('', include(router.urls)),
]

