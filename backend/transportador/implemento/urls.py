from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImplementoViewSet

router = DefaultRouter()
router.register(r'implementos', ImplementoViewSet, basename='transportador-implementos')

urlpatterns = [
    path('', include(router.urls)),
]

