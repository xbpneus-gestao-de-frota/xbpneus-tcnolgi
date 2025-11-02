from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registro_recapagem, name='recapagem-register'),
    path('login/', views.login_recapagem, name='recapagem-login'),
    path('perfil/', views.perfil_recapagem, name='recapagem-perfil'),
]
