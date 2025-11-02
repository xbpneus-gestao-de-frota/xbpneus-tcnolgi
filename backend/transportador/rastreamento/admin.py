from django.contrib import admin
from .models import Posicao, CercaEletronica, ViolacaoCerca, HistoricoRastreamento

@admin.register(Posicao)
class PosicaoAdmin(admin.ModelAdmin):
    list_display = ['veiculo', 'data_hora', 'latitude', 'longitude', 'velocidade']
    list_filter = ['veiculo', 'data_hora']
    readonly_fields = ['criado_em']

@admin.register(CercaEletronica)
class CercaEletronicaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'ativa', 'alertar_entrada', 'alertar_saida']
    list_filter = ['tipo', 'ativa']
    search_fields = ['nome']

@admin.register(ViolacaoCerca)
class ViolacaoCercaAdmin(admin.ModelAdmin):
    list_display = ['veiculo', 'cerca', 'tipo', 'data_hora', 'status']
    list_filter = ['tipo', 'status', 'data_hora']

@admin.register(HistoricoRastreamento)
class HistoricoRastreamentoAdmin(admin.ModelAdmin):
    list_display = ['veiculo', 'data', 'km_percorrido', 'velocidade_maxima', 'numero_paradas']
    list_filter = ['data']
