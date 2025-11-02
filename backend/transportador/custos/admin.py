from django.contrib import admin
from .models import CategoriaCusto, Custo, CustoPorKm


@admin.register(CategoriaCusto)
class CategoriaCustoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'ativo']
    list_filter = ['tipo', 'ativo']
    search_fields = ['nome']


@admin.register(Custo)
class CustoAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'categoria', 'veiculo', 'valor', 'data_custo', 'status']
    list_filter = ['categoria', 'status', 'data_custo']
    search_fields = ['descricao', 'fornecedor']
    readonly_fields = ['criado_em', 'atualizado_em']


@admin.register(CustoPorKm)
class CustoPorKmAdmin(admin.ModelAdmin):
    list_display = ['veiculo', 'mes_referencia', 'km_rodado', 'custo_total', 'custo_por_km']
    list_filter = ['mes_referencia']
    search_fields = ['veiculo__placa']
    readonly_fields = ['criado_em']
