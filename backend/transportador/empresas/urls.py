from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmpresaViewSet, FilialViewSet, register_transportador

router = DefaultRouter()
router.register(r'empresas', EmpresaViewSet, basename='empresa')
router.register(r'filiais', FilialViewSet, basename='filial')

urlpatterns = [
    path('transportador/register/', register_transportador, name='transportador-register'),
    path('', include(router.urls)),
]

