from rest_framework.routers import DefaultRouter
from .views import TireViewSet, ApplicationViewSet
router = DefaultRouter()
router.register(r"pneus", TireViewSet, basename="pneu")
router.register(r"aplicacoes", ApplicationViewSet, basename="aplicacao")
urlpatterns = router.urls
