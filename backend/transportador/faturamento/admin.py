from django.contrib import admin
from .models import Fatura, ItemFatura, NotaFiscal

@admin.register(Fatura)
class FaturaAdmin(admin.ModelAdmin):
    list_display = ['numero_fatura', 'cliente', 'data_emissao', 'data_vencimento', 'valor_liquido', 'status']
    list_filter = ['status', 'data_emissao']
    search_fields = ['numero_fatura', 'cliente__nome_razao_social']
    readonly_fields = ['criado_em', 'atualizado_em']

@admin.register(ItemFatura)
class ItemFaturaAdmin(admin.ModelAdmin):
    list_display = ['fatura', 'descricao', 'quantidade', 'valor_unitario', 'valor_total']
    list_filter = ['fatura']
    search_fields = ['descricao']

@admin.register(NotaFiscal)
class NotaFiscalAdmin(admin.ModelAdmin):
    list_display = ['numero', 'serie', 'tipo', 'fatura', 'data_emissao', 'valor_total', 'status']
    list_filter = ['tipo', 'status', 'data_emissao']
    search_fields = ['numero', 'serie', 'chave_acesso']
    readonly_fields = ['criado_em', 'atualizado_em']
