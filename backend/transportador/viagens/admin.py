from django.contrib import admin
from .models import Viagem, Carga, Parada


@admin.register(Viagem)
class ViagemAdmin(admin.ModelAdmin):
    list_display = ['numero_viagem', 'veiculo', 'origem', 'destino', 'status', 'data_saida_prevista']
    list_filter = ['status', 'data_saida_prevista']
    search_fields = ['numero_viagem', 'origem', 'destino', 'motorista_nome']
    readonly_fields = ['criado_em', 'atualizado_em']


@admin.register(Carga)
class CargaAdmin(admin.ModelAdmin):
    list_display = ['viagem', 'descricao', 'peso', 'cliente_nome']
    list_filter = ['viagem']
    search_fields = ['descricao', 'cliente_nome']


@admin.register(Parada)
class ParadaAdmin(admin.ModelAdmin):
    list_display = ['viagem', 'tipo', 'local', 'data_hora_entrada', 'duracao_minutos']
    list_filter = ['tipo', 'data_hora_entrada']
    search_fields = ['local', 'cidade']
