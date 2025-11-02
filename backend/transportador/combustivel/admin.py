from django.contrib import admin
from .models import PostoCombustivel, Abastecimento, ConsumoMensal


@admin.register(PostoCombustivel)
class PostoCombustivelAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cidade', 'estado', 'ativo']
    list_filter = ['ativo', 'estado']
    search_fields = ['nome', 'cnpj', 'cidade']


@admin.register(Abastecimento)
class AbastecimentoAdmin(admin.ModelAdmin):
    list_display = ['veiculo', 'data_abastecimento', 'litros', 'valor_total', 'consumo_medio']
    list_filter = ['tipo_combustivel', 'forma_pagamento', 'data_abastecimento']
    search_fields = ['veiculo__placa', 'posto__nome']
    readonly_fields = ['criado_em', 'valor_total', 'consumo_medio']


@admin.register(ConsumoMensal)
class ConsumoMensalAdmin(admin.ModelAdmin):
    list_display = ['veiculo', 'mes_referencia', 'total_litros', 'consumo_medio', 'custo_por_km']
    list_filter = ['mes_referencia']
    search_fields = ['veiculo__placa']
