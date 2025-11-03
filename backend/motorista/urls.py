from django.urls import include, path

from . import motorista_externo_urls, views

urlpatterns = [
    path('login/', views.login_motorista, name='motorista-login'),
    path('perfil/', views.perfil_motorista, name='motorista-perfil'),
    path('externo/', include(motorista_externo_urls)),
]
