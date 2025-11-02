"""
Admin para o módulo de Pecas
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.contrib import admin
from .models import CategoriaPeca, Peca, EstoquePeca, MovimentacaoPeca, FornecedorPeca


@admin.register(CategoriaPeca)
class CategoriaPecaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'empresa', 'ativo', 'criado_em', 'criado_por']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em', 'criado_por']


@admin.register(Peca)
class PecaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'empresa', 'ativo', 'criado_em', 'criado_por']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em', 'criado_por']


@admin.register(EstoquePeca)
class EstoquePecaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'empresa', 'ativo', 'criado_em', 'criado_por']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em', 'criado_por']


@admin.register(MovimentacaoPeca)
class MovimentacaoPecaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'empresa', 'ativo', 'criado_em', 'criado_por']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em', 'criado_por']


@admin.register(FornecedorPeca)
class FornecedorPecaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'empresa', 'ativo', 'criado_em', 'criado_por']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em', 'criado_por']


