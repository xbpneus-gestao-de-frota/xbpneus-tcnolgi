from django.urls import path, include
from . import views
from . import motorista_externo_urls

urlpatterns = [


    path('perfil/', views.perfil_motorista, name='motorista-perfil'),
    path('externo/', include(motorista_externo_urls)),
]