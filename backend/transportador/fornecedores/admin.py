from django.contrib import admin
from .models import Fornecedor, ContatoFornecedor


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ['nome_razao_social', 'cpf_cnpj', 'categoria', 'cidade', 'avaliacao', 'status']
    list_filter = ['categoria', 'status', 'estado', 'avaliacao']
    search_fields = ['nome_razao_social', 'nome_fantasia', 'cpf_cnpj']
    readonly_fields = ['criado_em', 'atualizado_em']


@admin.register(ContatoFornecedor)
class ContatoFornecedorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'fornecedor', 'cargo', 'telefone', 'principal']
    list_filter = ['principal']
    search_fields = ['nome', 'fornecedor__nome_razao_social']
