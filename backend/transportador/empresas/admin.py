from django.contrib import admin
from .models import Empresa, Filial, Transportador


class FilialInline(admin.TabularInline):
    """Inline para exibir filiais dentro da página de Empresa"""
    model = Filial
    extra = 0
    fields = ('codigo', 'nome', 'cidade', 'estado', 'matriz', 'ativa')
    readonly_fields = ('criado_em',)


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'cnpj', 'cidade', 'estado', 'ativa', 'total_filiais')
    list_filter = ('tipo', 'ativa', 'estado')
    search_fields = ('nome', 'cnpj', 'razao_social', 'nome_fantasia', 'email')
    readonly_fields = ('criado_em', 'atualizado_em')
    inlines = [FilialInline]

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'tipo', 'cnpj', 'razao_social', 'nome_fantasia')
        }),
        ('Inscrições', {
            'fields': ('inscricao_estadual', 'inscricao_municipal'),
            'classes': ('collapse',)
        }),
        ('Endereço', {
            'fields': ('cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado'),
            'classes': ('collapse',)
        }),
        ('Contato', {
            'fields': ('telefone', 'celular', 'email', 'site'),
            'classes': ('collapse',)
        }),
        ('Configurações', {
            'fields': ('ativa',)
        }),
        ('Metadados', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )

    def total_filiais(self, obj):
        """Retorna o total de filiais da empresa"""
        return obj.filiais.count()
    total_filiais.short_description = 'Total de Filiais'


@admin.register(Filial)
class FilialAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo', 'empresa', 'cidade', 'estado', 'matriz', 'ativa')
    list_filter = ('empresa', 'ativa', 'matriz', 'estado')
    search_fields = ('nome', 'codigo', 'cnpj', 'email', 'empresa__nome')
    readonly_fields = ('criado_em', 'atualizado_em')

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('empresa', 'codigo', 'nome', 'cnpj')
        }),
        ('Inscrições', {
            'fields': ('inscricao_estadual', 'inscricao_municipal'),
            'classes': ('collapse',)
        }),
        ('Endereço', {
            'fields': ('cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado'),
            'classes': ('collapse',)
        }),
        ('Contato', {
            'fields': ('telefone', 'celular', 'email'),
            'classes': ('collapse',)
        }),
        ('Configurações', {
            'fields': ('matriz', 'ativa')
        }),
        ('Metadados', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Transportador)
class TransportadorAdmin(admin.ModelAdmin):
    list_display = (
        'razao', 'cnpj', 'email', 'telefone', 'status', 'criado_em'
    )
    list_filter = ('status', 'criado_em')
    search_fields = ('razao', 'cnpj', 'email')
    readonly_fields = ('criado_em',)

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('razao', 'cnpj', 'telefone', 'email')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Datas', {
            'fields': ('criado_em',),
            'classes': ('collapse',)
        }),
    )

    actions = ['aprovar_cadastros', 'recusar_cadastros']

    def aprovar_cadastros(self, request, queryset):
        from backend.users.models import User
        count = 0
        for transportador in queryset.filter(status='PENDENTE'):
            # Criar usuário
            user = User.objects.create_user(
                username=transportador.email,
                email=transportador.email,
                password="senha_temporaria_123",  # Enviar email para redefinir
                is_active=True
            )
            user.role = 'transportador'
            user.save()
            transportador.status = 'APROVADO'
            transportador.save()
            count += 1
        self.message_user(request, f'{count} cadastro(s) aprovado(s) com sucesso!')
    aprovar_cadastros.short_description = 'Aprovar cadastros selecionados'

    def recusar_cadastros(self, request, queryset):
        count = queryset.filter(status='PENDENTE').update(status='RECUSADO')
        self.message_user(request, f'{count} cadastro(s) recusado(s)!')
    recusar_cadastros.short_description = 'Recusar cadastros selecionados'

