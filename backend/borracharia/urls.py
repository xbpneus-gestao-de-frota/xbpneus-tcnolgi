from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registro_borracharia, name='borracharia-register'),
    path('login/', views.login_borracharia, name='borracharia-login'),
    path('perfil/', views.perfil_borracharia, name='borracharia-perfil'),
]
