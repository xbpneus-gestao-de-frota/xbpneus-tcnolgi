from django.contrib import admin
from .models import Contrato, Aditivo


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ['numero_contrato', 'titulo', 'tipo', 'data_inicio', 'data_fim', 'valor_total', 'status']
    list_filter = ['tipo', 'status', 'data_inicio']
    search_fields = ['numero_contrato', 'titulo']
    readonly_fields = ['criado_em', 'atualizado_em']


@admin.register(Aditivo)
class AditivoAdmin(admin.ModelAdmin):
    list_display = ['numero_aditivo', 'contrato', 'data_aditivo', 'alteracao_valor']
    list_filter = ['data_aditivo']
    search_fields = ['numero_aditivo', 'contrato__numero_contrato']
