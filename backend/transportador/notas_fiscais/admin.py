"""
Admin para o módulo de Notas Fiscais
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.contrib import admin
from .models import NotaFiscal, ItemNotaFiscal, ImpostoNotaFiscal, AnexoNotaFiscal


class ItemNotaFiscalInline(admin.TabularInline):
    """Inline para itens da nota fiscal"""
    model = ItemNotaFiscal
    extra = 1
    fields = ['numero_item', 'codigo_produto', 'descricao', 'quantidade', 'valor_unitario', 'valor_total']
    readonly_fields = ['valor_total']


class ImpostoNotaFiscalInline(admin.TabularInline):
    """Inline para impostos da nota fiscal"""
    model = ImpostoNotaFiscal
    extra = 1
    fields = ['tipo_imposto', 'base_calculo', 'aliquota', 'valor_imposto']


class AnexoNotaFiscalInline(admin.TabularInline):
    """Inline para anexos da nota fiscal"""
    model = AnexoNotaFiscal
    extra = 0
    fields = ['titulo', 'arquivo', 'criado_em']
    readonly_fields = ['criado_em']


@admin.register(NotaFiscal)
class NotaFiscalAdmin(admin.ModelAdmin):
    """Admin para Nota Fiscal"""
    
    list_display = [
        'numero', 'serie', 'modelo', 'tipo', 'status',
        'destinatario_nome', 'valor_total', 'data_emissao'
    ]
    list_filter = ['tipo', 'status', 'modelo', 'data_emissao']
    search_fields = ['numero', 'serie', 'destinatario_nome', 'chave_acesso']
    readonly_fields = ['valor_total', 'criado_em', 'atualizado_em', 'criado_por']
    inlines = [ItemNotaFiscalInline, ImpostoNotaFiscalInline, AnexoNotaFiscalInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('empresa', 'numero', 'serie', 'modelo', 'tipo', 'status')
        }),
        ('Datas', {
            'fields': ('data_emissao', 'data_autorizacao', 'data_cancelamento')
        }),
        ('Emitente', {
            'fields': ('emitente_cnpj', 'emitente_nome', 'emitente_ie')
        }),
        ('Destinatário', {
            'fields': (
                'destinatario_cpf_cnpj', 'destinatario_nome',
                'destinatario_ie', 'destinatario_endereco'
            )
        }),
        ('Valores', {
            'fields': (
                'valor_produtos', 'valor_servicos', 'valor_desconto',
                'valor_frete', 'valor_seguro', 'valor_outras_despesas',
                'valor_total'
            )
        }),
        ('Impostos', {
            'fields': (
                'base_calculo_icms', 'valor_icms', 'valor_ipi',
                'valor_pis', 'valor_cofins'
            )
        }),
        ('SEFAZ', {
            'fields': (
                'chave_acesso', 'protocolo_autorizacao', 'motivo_cancelamento'
            )
        }),
        ('Observações', {
            'fields': ('observacoes', 'informacoes_complementares'),
            'classes': ('collapse',)
        }),
        ('Auditoria', {
            'fields': ('criado_em', 'atualizado_em', 'criado_por'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Salva o usuário que criou a nota"""
        if not change:
            obj.criado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(ItemNotaFiscal)
class ItemNotaFiscalAdmin(admin.ModelAdmin):
    """Admin para Item de Nota Fiscal"""
    
    list_display = [
        'nota_fiscal', 'numero_item', 'codigo_produto',
        'descricao', 'quantidade', 'valor_unitario', 'valor_total'
    ]
    list_filter = ['nota_fiscal__tipo']
    search_fields = ['codigo_produto', 'descricao', 'nota_fiscal__numero']
    readonly_fields = ['valor_total', 'valor_icms', 'valor_ipi']


@admin.register(ImpostoNotaFiscal)
class ImpostoNotaFiscalAdmin(admin.ModelAdmin):
    """Admin para Imposto de Nota Fiscal"""
    
    list_display = [
        'nota_fiscal', 'tipo_imposto', 'base_calculo',
        'aliquota', 'valor_imposto'
    ]
    list_filter = ['tipo_imposto']
    search_fields = ['nota_fiscal__numero', 'tipo_imposto']


@admin.register(AnexoNotaFiscal)
class AnexoNotaFiscalAdmin(admin.ModelAdmin):
    """Admin para Anexo de Nota Fiscal"""
    
    list_display = ['nota_fiscal', 'titulo', 'tipo_arquivo', 'tamanho_arquivo', 'criado_em']
    list_filter = ['tipo_arquivo', 'criado_em']
    search_fields = ['titulo', 'nota_fiscal__numero']
    readonly_fields = ['criado_em', 'criado_por', 'tamanho_arquivo']
