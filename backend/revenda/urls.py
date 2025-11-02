from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registro_revenda, name='revenda-register'),
    path('login/', views.login_revenda, name='revenda-login'),
    path('perfil/', views.perfil_revenda, name='revenda-perfil'),
]
