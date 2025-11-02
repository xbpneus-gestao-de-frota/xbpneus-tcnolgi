"""
Admin para o módulo de Ferramentas
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.contrib import admin
from .models import Ferramenta, EmprestimoFerramenta, ManutencaoFerramenta, CalibracaoFerramenta


@admin.register(Ferramenta)
class FerramentaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'empresa', 'ativo', 'criado_em']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em']


@admin.register(EmprestimoFerramenta)
class EmprestimoFerramentaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'empresa', 'ativo', 'criado_em']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em']


@admin.register(ManutencaoFerramenta)
class ManutencaoFerramentaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'empresa', 'ativo', 'criado_em']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em']


@admin.register(CalibracaoFerramenta)
class CalibracaoFerramentaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'empresa', 'ativo', 'criado_em']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em']


