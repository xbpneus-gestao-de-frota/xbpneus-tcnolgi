"""
Admin para o módulo de Relatorios
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.contrib import admin
from .models import RelatorioTemplate, RelatorioAgendado, RelatorioGerado, DashboardPersonalizado


@admin.register(RelatorioTemplate)
class RelatorioTemplateAdmin(admin.ModelAdmin):
    list_display = ['nome', 'empresa', 'ativo', 'criado_em', 'criado_por']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em', 'criado_por']


@admin.register(RelatorioAgendado)
class RelatorioAgendadoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'empresa', 'ativo', 'criado_em', 'criado_por']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em', 'criado_por']


@admin.register(RelatorioGerado)
class RelatorioGeradoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'empresa', 'ativo', 'criado_em', 'criado_por']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em', 'criado_por']


@admin.register(DashboardPersonalizado)
class DashboardPersonalizadoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'empresa', 'ativo', 'criado_em', 'criado_por']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em', 'criado_por']


