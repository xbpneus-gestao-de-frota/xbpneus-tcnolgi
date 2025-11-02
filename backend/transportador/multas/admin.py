from django.contrib import admin
from .models import Multa, RecursoMulta, PontuacaoCNH


@admin.register(Multa)
class MultaAdmin(admin.ModelAdmin):
    list_display = ['numero_auto', 'veiculo', 'data_infracao', 'gravidade', 'valor', 'status']
    list_filter = ['gravidade', 'status', 'data_infracao']
    search_fields = ['numero_auto', 'veiculo__placa', 'motorista_nome']
    readonly_fields = ['criado_em', 'atualizado_em']


@admin.register(RecursoMulta)
class RecursoMultaAdmin(admin.ModelAdmin):
    list_display = ['protocolo', 'multa', 'data_recurso', 'status']
    list_filter = ['status', 'data_recurso']
    search_fields = ['protocolo', 'multa__numero_auto']


@admin.register(PontuacaoCNH)
class PontuacaoCNHAdmin(admin.ModelAdmin):
    list_display = ['motorista_nome', 'motorista_cnh', 'pontos_atuais', 'pontos_limite', 'suspenso']
    list_filter = ['suspenso']
    search_fields = ['motorista_nome', 'motorista_cnh']
