from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DespesaViewSet, LancamentoViewSet

router = DefaultRouter()
router.register(r'despesas', DespesaViewSet, basename='transportador-despesas')
router.register(r'lancamentos', LancamentoViewSet, basename='transportador-lancamentos')

urlpatterns = [
    path('', include(router.urls)),
]

