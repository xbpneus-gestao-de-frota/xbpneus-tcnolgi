from django.contrib import admin
from .models import Rota, PontoRota, RotaOtimizada

@admin.register(Rota)
class RotaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'origem', 'destino', 'veiculo', 'distancia_km', 'status']
    list_filter = ['status', 'data_inicio_prevista']
    search_fields = ['nome', 'origem', 'destino']

@admin.register(PontoRota)
class PontoRotaAdmin(admin.ModelAdmin):
    list_display = ['rota', 'ordem', 'tipo', 'nome', 'cidade']
    list_filter = ['tipo']
    search_fields = ['nome', 'cidade']

@admin.register(RotaOtimizada)
class RotaOtimizadaAdmin(admin.ModelAdmin):
    list_display = ['rota_original', 'algoritmo', 'distancia_km', 'economia_distancia_km', 'criado_em']
    list_filter = ['algoritmo']
