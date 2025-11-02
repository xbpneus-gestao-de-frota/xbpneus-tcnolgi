from rest_framework.routers import DefaultRouter
from .views import CanalNotificacaoViewSet, NotificacaoViewSet, TemplateNotificacaoViewSet, PreferenciaNotificacaoViewSet

router = DefaultRouter()
router.register(r"canais", CanalNotificacaoViewSet, basename="canal")
router.register(r"notificacoes", NotificacaoViewSet, basename="notificacao")
router.register(r"templates", TemplateNotificacaoViewSet, basename="template")
router.register(r"preferencias", PreferenciaNotificacaoViewSet, basename="preferencia")

urlpatterns = router.urls
