"""
Admin para o módulo de Manutenção
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.contrib import admin
from .models import (
    OrdemServico, ItemOS, ChecklistManutencao,
    PlanoManutencaoPreventiva, HistoricoManutencao,
    WorkOrder, Teste
)


class ItemOSInline(admin.TabularInline):
    """Inline para itens da OS"""
    model = ItemOS
    extra = 1
    fields = ['tipo', 'codigo', 'descricao', 'quantidade', 'unidade', 'valor_unitario', 'valor_total', 'aplicado']
    readonly_fields = ['valor_total']


class ChecklistInline(admin.StackedInline):
    """Inline para checklist"""
    model = ChecklistManutencao
    extra = 0
    max_num = 1


@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    """Admin para Ordem de Serviço"""
    
    list_display = ['numero', 'veiculo', 'tipo', 'status', 'prioridade', 'data_abertura', 'custo_total']
    list_filter = ['status', 'tipo', 'prioridade', 'data_abertura']
    search_fields = ['numero', 'veiculo__placa', 'descricao_problema']
    readonly_fields = ['custo_total', 'criado_em', 'atualizado_em']
    date_hierarchy = 'data_abertura'
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('empresa', 'veiculo', 'numero', 'tipo', 'status', 'prioridade')
        }),
        ('Datas', {
            'fields': ('data_agendamento', 'data_inicio', 'data_conclusao', 'data_cancelamento')
        }),
        ('Descrição', {
            'fields': ('descricao_problema', 'descricao_servico', 'observacoes')
        }),
        ('Quilometragem', {
            'fields': ('km_abertura', 'km_conclusao')
        }),
        ('Custos', {
            'fields': ('custo_pecas', 'custo_mao_obra', 'custo_total')
        }),
        ('Responsáveis', {
            'fields': ('aberta_por', 'mecanico')
        }),
        ('Auditoria', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [ItemOSInline, ChecklistInline]


@admin.register(ItemOS)
class ItemOSAdmin(admin.ModelAdmin):
    """Admin para Item da OS"""
    
    list_display = ['os', 'tipo', 'codigo', 'descricao', 'quantidade', 'valor_unitario', 'valor_total', 'aplicado']
    list_filter = ['tipo', 'aplicado']
    search_fields = ['codigo', 'descricao', 'os__numero']
    readonly_fields = ['valor_total']


@admin.register(ChecklistManutencao)
class ChecklistManutencaoAdmin(admin.ModelAdmin):
    """Admin para Checklist de Manutenção"""
    
    list_display = ['os', 'realizado_por', 'realizado_em', 'percentual_conclusao']
    list_filter = ['realizado_em']
    search_fields = ['os__numero']
    readonly_fields = ['percentual_conclusao', 'realizado_em']
    
    fieldsets = (
        ('Informações', {
            'fields': ('os', 'realizado_por', 'realizado_em', 'percentual_conclusao')
        }),
        ('Níveis e Fluidos', {
            'fields': ('nivel_oleo_motor', 'nivel_fluido_freio', 'nivel_agua_radiador')
        }),
        ('Pneus', {
            'fields': ('pressao_pneus', 'estado_pneus')
        }),
        ('Elétrica', {
            'fields': ('funcionamento_farois', 'funcionamento_setas', 'funcionamento_buzina')
        }),
        ('Mecânica', {
            'fields': ('funcionamento_freios', 'limpeza_filtro_ar', 'estado_correia', 'vazamentos')
        }),
        ('Testes', {
            'fields': ('torque_ok', 'pressao_ok', 'rodagem_ok')
        }),
        ('Observações', {
            'fields': ('observacoes',)
        }),
    )


@admin.register(PlanoManutencaoPreventiva)
class PlanoManutencaoPreventivaAdmin(admin.ModelAdmin):
    """Admin para Plano de Manutenção Preventiva"""
    
    list_display = ['nome', 'veiculo', 'periodicidade_km', 'periodicidade_dias', 'proxima_manutencao_data', 'ativo']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'descricao', 'veiculo__placa']
    readonly_fields = ['criado_em', 'atualizado_em']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('empresa', 'veiculo', 'nome', 'descricao', 'ativo')
        }),
        ('Periodicidade', {
            'fields': ('periodicidade_km', 'periodicidade_dias')
        }),
        ('Próxima Manutenção', {
            'fields': ('proxima_manutencao_km', 'proxima_manutencao_data')
        }),
        ('Auditoria', {
            'fields': ('criado_por', 'criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )


@admin.register(HistoricoManutencao)
class HistoricoManutencaoAdmin(admin.ModelAdmin):
    """Admin para Histórico de Manutenção"""
    
    list_display = ['veiculo', 'tipo', 'data', 'km', 'custo']
    list_filter = ['tipo', 'data']
    search_fields = ['veiculo__placa', 'descricao']
    readonly_fields = ['criado_em']
    date_hierarchy = 'data'


# Admins legados (compatibilidade)
@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    """Admin para Work Order (legado)"""
    list_display = [f.name for f in WorkOrder._meta.fields]


@admin.register(Teste)
class TesteAdmin(admin.ModelAdmin):
    """Admin para Teste (legado)"""
    list_display = [f.name for f in Teste._meta.fields]

