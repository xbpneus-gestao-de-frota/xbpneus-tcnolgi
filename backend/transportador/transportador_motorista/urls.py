from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MotoristaTransportadorViewSet

router = DefaultRouter()
router.register(r'motoristas', MotoristaTransportadorViewSet, basename='transportador-motoristas')

urlpatterns = [
    path('', include(router.urls)),
]

