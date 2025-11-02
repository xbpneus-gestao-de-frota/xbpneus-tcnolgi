from django.contrib import admin
from django.contrib import admin
from .models import AnaliseIA, Gamificacao, Garantia


@admin.register(AnaliseIA)
class AnaliseIAAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'tipo_analise', 'data_analise', 'precisao', 'status']
    list_filter = ['tipo_analise', 'status', 'data_analise']
    search_fields = ['usuario__username']
    date_hierarchy = 'data_analise'


@admin.register(Gamificacao)
class GamificacaoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'pontos', 'nivel']
    list_filter = ['nivel']
    search_fields = ['usuario__username']


@admin.register(Garantia)
class GarantiaAdmin(admin.ModelAdmin):
    list_display = ['protocolo', 'usuario', 'status', 'data_abertura']
    list_filter = ['status', 'data_abertura']
    search_fields = ['protocolo', 'usuario__username']
    date_hierarchy = 'data_abertura'

