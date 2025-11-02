from django.contrib import admin
from .models import ContaPagar, ContaReceber, Pagamento

@admin.register(ContaPagar)
class ContaPagarAdmin(admin.ModelAdmin):
    list_display = ['numero_documento', 'descricao', 'fornecedor', 'data_vencimento', 'valor_original', 'status']
    list_filter = ['tipo', 'status', 'data_vencimento']
    search_fields = ['numero_documento', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em']

@admin.register(ContaReceber)
class ContaReceberAdmin(admin.ModelAdmin):
    list_display = ['numero_documento', 'descricao', 'cliente', 'data_vencimento', 'valor_original', 'status']
    list_filter = ['status', 'data_vencimento']
    search_fields = ['numero_documento', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em']

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ['data_pagamento', 'valor', 'forma_pagamento']
    list_filter = ['forma_pagamento', 'data_pagamento']
