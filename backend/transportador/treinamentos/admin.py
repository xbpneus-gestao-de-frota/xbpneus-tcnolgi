"""
Admin para o módulo de Treinamentos
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.contrib import admin
from .models import CursoTreinamento, TreinamentoRealizado, CertificadoTreinamento, InstrutorTreinamento


@admin.register(CursoTreinamento)
class CursoTreinamentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'empresa', 'ativo', 'criado_em', 'criado_por']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em', 'criado_por']


@admin.register(TreinamentoRealizado)
class TreinamentoRealizadoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'empresa', 'ativo', 'criado_em', 'criado_por']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em', 'criado_por']


@admin.register(CertificadoTreinamento)
class CertificadoTreinamentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'empresa', 'ativo', 'criado_em', 'criado_por']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em', 'criado_por']


@admin.register(InstrutorTreinamento)
class InstrutorTreinamentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'empresa', 'ativo', 'criado_em', 'criado_por']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em', 'criado_por']


