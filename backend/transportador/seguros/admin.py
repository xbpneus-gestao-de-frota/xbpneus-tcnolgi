from django.contrib import admin
from .models import Seguradora, Apolice, Sinistro


@admin.register(Seguradora)
class SeguradoraAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cnpj', 'telefone', 'ativo']
    list_filter = ['ativo']
    search_fields = ['nome', 'cnpj']


@admin.register(Apolice)
class ApoliceAdmin(admin.ModelAdmin):
    list_display = ['numero_apolice', 'tipo', 'seguradora', 'veiculo', 'data_inicio', 'data_fim', 'status']
    list_filter = ['tipo', 'status', 'data_inicio']
    search_fields = ['numero_apolice', 'veiculo__placa']
    readonly_fields = ['criado_em', 'atualizado_em']


@admin.register(Sinistro)
class SinistroAdmin(admin.ModelAdmin):
    list_display = ['numero_sinistro', 'tipo', 'apolice', 'data_ocorrencia', 'valor_estimado', 'status']
    list_filter = ['tipo', 'status', 'data_ocorrencia']
    search_fields = ['numero_sinistro', 'local_ocorrencia']
    readonly_fields = ['criado_em', 'atualizado_em']
