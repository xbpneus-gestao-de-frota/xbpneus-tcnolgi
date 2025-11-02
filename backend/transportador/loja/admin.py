from django.contrib import admin
from .models import CategoriaProduto, Produto, Pedido, ItemPedido, MovimentacaoEstoqueLoja


@admin.register(CategoriaProduto)
class CategoriaProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'ativo', 'criado_em']
    list_filter = ['tipo', 'ativo']
    search_fields = ['nome']


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nome', 'categoria', 'preco_venda', 'quantidade_estoque', 'status']
    list_filter = ['categoria', 'status', 'ativo']
    search_fields = ['codigo', 'nome', 'fabricante']
    readonly_fields = ['criado_em', 'atualizado_em']


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['numero_pedido', 'cliente_nome', 'tipo', 'status', 'valor_total', 'data_pedido']
    list_filter = ['status', 'tipo', 'data_pedido']
    search_fields = ['numero_pedido', 'cliente_nome', 'cliente_documento']
    readonly_fields = ['criado_em', 'atualizado_em']
    inlines = [ItemPedidoInline]


@admin.register(MovimentacaoEstoqueLoja)
class MovimentacaoEstoqueLojaAdmin(admin.ModelAdmin):
    list_display = ['produto', 'tipo', 'quantidade', 'data_movimentacao']
    list_filter = ['tipo', 'data_movimentacao']
    search_fields = ['produto__nome', 'produto__codigo']
    readonly_fields = ['data_movimentacao']
