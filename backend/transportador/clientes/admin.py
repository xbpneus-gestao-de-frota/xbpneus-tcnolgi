from django.contrib import admin
from .models import Cliente, ContatoCliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome_razao_social', 'cpf_cnpj', 'tipo', 'cidade', 'status']
    list_filter = ['tipo', 'status', 'estado']
    search_fields = ['nome_razao_social', 'nome_fantasia', 'cpf_cnpj']
    readonly_fields = ['criado_em', 'atualizado_em']


@admin.register(ContatoCliente)
class ContatoClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cliente', 'cargo', 'telefone', 'principal']
    list_filter = ['principal']
    search_fields = ['nome', 'cliente__nome_razao_social']
