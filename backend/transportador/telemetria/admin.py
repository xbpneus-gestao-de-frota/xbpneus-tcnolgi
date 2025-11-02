from django.contrib import admin
from .models import Dispositivo, Leitura, Alerta

@admin.register(Dispositivo)
class DispositivoAdmin(admin.ModelAdmin):
    list_display = ['numero_serie', 'tipo', 'veiculo', 'fabricante', 'status']
    list_filter = ['tipo', 'status', 'fabricante']
    search_fields = ['numero_serie', 'veiculo__placa']

@admin.register(Leitura)
class LeituraAdmin(admin.ModelAdmin):
    list_display = ['dispositivo', 'data_hora', 'velocidade', 'temperatura', 'hodometro']
    list_filter = ['dispositivo', 'data_hora']
    readonly_fields = ['criado_em']

@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ['dispositivo', 'tipo', 'severidade', 'data_hora', 'status']
    list_filter = ['tipo', 'severidade', 'status']
    search_fields = ['mensagem']
