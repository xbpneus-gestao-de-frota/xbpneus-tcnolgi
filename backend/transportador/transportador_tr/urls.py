from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TRViewSet

router = DefaultRouter()
router.register(r'tr', TRViewSet, basename='transportador-tr')

urlpatterns = [
    path('', include(router.urls)),
]

