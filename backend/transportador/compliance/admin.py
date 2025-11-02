"""
Admin para o módulo de Compliance
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.contrib import admin
from .models import NormaCompliance, AuditoriaCompliance, NaoConformidade, PlanoAcaoCompliance


@admin.register(NormaCompliance)
class NormaComplianceAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo', 'criado_em']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em']


@admin.register(AuditoriaCompliance)
class AuditoriaComplianceAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo', 'criado_em']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em']


@admin.register(NaoConformidade)
class NaoConformidadeAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo', 'criado_em']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em']


@admin.register(PlanoAcaoCompliance)
class PlanoAcaoComplianceAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo', 'criado_em']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em']


