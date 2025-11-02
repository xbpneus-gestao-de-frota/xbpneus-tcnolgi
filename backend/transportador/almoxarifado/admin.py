"""
Admin para o módulo de Almoxarifado
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.contrib import admin
from .models import (
    Almoxarifado, LocalEstoque, MovimentacaoAlmoxarifado,
    InventarioAlmoxarifado, ItemInventario, RequisicaoMaterial, ItemRequisicao
)


@admin.register(Almoxarifado)
class AlmoxarifadoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nome', 'tipo', 'cidade', 'ativo']
    list_filter = ['tipo', 'ativo', 'estado']
    search_fields = ['codigo', 'nome', 'cidade']


@admin.register(LocalEstoque)
class LocalEstoqueAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'almoxarifado', 'descricao', 'corredor', 'prateleira', 'ativo']
    list_filter = ['almoxarifado', 'ativo']
    search_fields = ['codigo', 'descricao']


@admin.register(MovimentacaoAlmoxarifado)
class MovimentacaoAlmoxarifadoAdmin(admin.ModelAdmin):
    list_display = ['numero', 'tipo', 'almoxarifado', 'data_movimentacao', 'descricao_produto', 'quantidade']
    list_filter = ['tipo', 'data_movimentacao']
    search_fields = ['numero', 'codigo_produto', 'descricao_produto']


@admin.register(InventarioAlmoxarifado)
class InventarioAlmoxarifadoAdmin(admin.ModelAdmin):
    list_display = ['numero', 'almoxarifado', 'data_inventario', 'status']
    list_filter = ['status', 'data_inventario']
    search_fields = ['numero']


@admin.register(ItemInventario)
class ItemInventarioAdmin(admin.ModelAdmin):
    list_display = ['inventario', 'codigo_produto', 'descricao_produto', 'quantidade_sistema', 'quantidade_contada', 'diferenca']
    list_filter = ['inventario']
    search_fields = ['codigo_produto', 'descricao_produto']


@admin.register(RequisicaoMaterial)
class RequisicaoMaterialAdmin(admin.ModelAdmin):
    list_display = ['numero', 'almoxarifado', 'solicitante', 'data_requisicao', 'status']
    list_filter = ['status', 'data_requisicao']
    search_fields = ['numero', 'solicitante__username']


@admin.register(ItemRequisicao)
class ItemRequisicaoAdmin(admin.ModelAdmin):
    list_display = ['requisicao', 'codigo_produto', 'descricao_produto', 'quantidade_solicitada', 'quantidade_atendida']
    list_filter = ['requisicao']
    search_fields = ['codigo_produto', 'descricao_produto']
