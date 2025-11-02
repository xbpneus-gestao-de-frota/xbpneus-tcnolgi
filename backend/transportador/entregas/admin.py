from django.contrib import admin
from .models import Entrega, POD, Ocorrencia, Tentativa

@admin.register(Entrega)
class EntregaAdmin(admin.ModelAdmin):
    list_display = ['numero_entrega', 'destinatario_nome', 'cidade', 'data_prevista', 'status']
    list_filter = ['status', 'data_prevista']
    search_fields = ['numero_entrega', 'destinatario_nome', 'numero_nota_fiscal']

@admin.register(POD)
class PODAdmin(admin.ModelAdmin):
    list_display = ['entrega', 'recebedor_nome', 'data_hora_recebimento']
    list_filter = ['data_hora_recebimento']
    search_fields = ['recebedor_nome']

@admin.register(Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    list_display = ['entrega', 'tipo', 'data_hora']
    list_filter = ['tipo', 'data_hora']
    search_fields = ['descricao']

@admin.register(Tentativa)
class TentativaAdmin(admin.ModelAdmin):
    list_display = ['entrega', 'numero_tentativa', 'data_hora', 'sucesso']
    list_filter = ['sucesso', 'data_hora']
