from rest_framework.routers import DefaultRouter
from .views import DashboardViewSet, WidgetViewSet, KPIViewSet

router = DefaultRouter()
router.register(r"dashboards", DashboardViewSet, basename="dashboard")
router.register(r"widgets", WidgetViewSet, basename="widget")
router.register(r"kpis", KPIViewSet, basename="kpi")

urlpatterns = router.urls
