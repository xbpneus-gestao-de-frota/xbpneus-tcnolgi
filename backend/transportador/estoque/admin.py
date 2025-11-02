"""
Admin expandido para o módulo de Estoque
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.contrib import admin
from .models import (
    CategoriaProduto, Produto, SaldoEstoque, StockMove,
    MovimentacaoEstoque, PrevisaoDemanda, CurvaABC
)


@admin.register(CategoriaProduto)
class CategoriaProdutoAdmin(admin.ModelAdmin):
    list_display = ["codigo", "nome", "empresa", "ativo"]
    list_filter = ["ativo", "empresa"]
    search_fields = ["codigo", "nome"]


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ["codigo", "descricao", "categoria", "unidade", "custo_medio", "ativo"]
    list_filter = ["ativo", "categoria"]
    search_fields = ["codigo", "descricao", "codigo_barras"]


@admin.register(SaldoEstoque)
class SaldoEstoqueAdmin(admin.ModelAdmin):
    list_display = ["produto", "quantidade", "valor_total", "data_ultima_movimentacao"]
    list_filter = ["ativo"]
    search_fields = ["produto__codigo", "produto__descricao"]


@admin.register(MovimentacaoEstoque)
class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    list_display = ["produto", "tipo", "quantidade", "valor_unitario", "data_movimentacao"]
    list_filter = ["tipo", "data_movimentacao"]
    search_fields = ["produto__codigo", "documento_referencia"]


@admin.register(PrevisaoDemanda)
class PrevisaoDemandaAdmin(admin.ModelAdmin):
    list_display = ["produto", "mes_referencia", "quantidade_prevista", "quantidade_real", "metodo_previsao"]
    list_filter = ["metodo_previsao", "mes_referencia"]
    search_fields = ["produto__codigo"]


@admin.register(CurvaABC)
class CurvaABCAdmin(admin.ModelAdmin):
    list_display = ["produto", "classificacao", "valor_total_vendas", "percentual_acumulado", "periodo_inicio", "periodo_fim"]
    list_filter = ["classificacao"]
    search_fields = ["produto__codigo"]

