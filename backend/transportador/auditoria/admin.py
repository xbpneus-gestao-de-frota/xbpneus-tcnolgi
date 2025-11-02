"""
Admin para o módulo de Auditoria
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.contrib import admin
from .models import (
    LogAuditoria,
    LogAcesso,
    LogAlteracao,
    SessaoUsuario,
    ConfiguracaoAuditoria
)


@admin.register(LogAuditoria)
class LogAuditoriaAdmin(admin.ModelAdmin):
    """Admin para Log de Auditoria"""
    
    list_display = [
        'criado_em', 'usuario', 'empresa', 'acao',
        'severidade', 'descricao', 'ip_address'
    ]
    list_filter = ['acao', 'severidade', 'criado_em', 'modulo']
    search_fields = ['descricao', 'usuario__username', 'ip_address', 'url']
    readonly_fields = [
        'usuario', 'empresa', 'acao', 'descricao', 'severidade',
        'content_type', 'object_id', 'ip_address', 'user_agent',
        'metodo_http', 'url', 'dados_anteriores', 'dados_novos',
        'modulo', 'funcao', 'mensagem_erro', 'stack_trace', 'criado_em'
    ]
    date_hierarchy = 'criado_em'
    
    def has_add_permission(self, request):
        """Não permite adicionar logs manualmente"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Não permite editar logs"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Permite deletar apenas para superusuários"""
        return request.user.is_superuser


@admin.register(LogAcesso)
class LogAcessoAdmin(admin.ModelAdmin):
    """Admin para Log de Acesso"""
    
    list_display = [
        'criado_em', 'usuario', 'tipo_acesso', 'sucesso',
        'ip_address', 'dispositivo'
    ]
    list_filter = ['tipo_acesso', 'sucesso', 'criado_em']
    search_fields = ['usuario__username', 'ip_address']
    readonly_fields = [
        'usuario', 'tipo_acesso', 'ip_address', 'user_agent',
        'dispositivo', 'navegador', 'sistema_operacional',
        'pais', 'cidade', 'sucesso', 'motivo_falha', 'criado_em'
    ]
    date_hierarchy = 'criado_em'
    
    def has_add_permission(self, request):
        """Não permite adicionar logs manualmente"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Não permite editar logs"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Permite deletar apenas para superusuários"""
        return request.user.is_superuser


@admin.register(LogAlteracao)
class LogAlteracaoAdmin(admin.ModelAdmin):
    """Admin para Log de Alteração"""
    
    list_display = [
        'criado_em', 'usuario', 'tipo_alteracao',
        'object_repr', 'campo'
    ]
    list_filter = ['tipo_alteracao', 'content_type', 'criado_em']
    search_fields = ['object_repr', 'campo', 'usuario__username']
    readonly_fields = [
        'usuario', 'empresa', 'content_type', 'object_id',
        'object_repr', 'tipo_alteracao', 'campo',
        'valor_anterior', 'valor_novo', 'criado_em'
    ]
    date_hierarchy = 'criado_em'
    
    def has_add_permission(self, request):
        """Não permite adicionar logs manualmente"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Não permite editar logs"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Permite deletar apenas para superusuários"""
        return request.user.is_superuser


@admin.register(SessaoUsuario)
class SessaoUsuarioAdmin(admin.ModelAdmin):
    """Admin para Sessão de Usuário"""
    
    list_display = [
        'usuario', 'ativa', 'iniciada_em',
        'ultima_atividade', 'ip_address', 'dispositivo'
    ]
    list_filter = ['ativa', 'iniciada_em']
    search_fields = ['usuario__username', 'ip_address', 'session_key']
    readonly_fields = [
        'usuario', 'session_key', 'ip_address', 'user_agent',
        'dispositivo', 'iniciada_em', 'ultima_atividade'
    ]
    date_hierarchy = 'iniciada_em'
    
    actions = ['encerrar_sessoes']
    
    def encerrar_sessoes(self, request, queryset):
        """Encerra sessões selecionadas"""
        from django.utils import timezone
        count = queryset.filter(ativa=True).update(
            ativa=False,
            encerrada_em=timezone.now(),
            motivo_encerramento='ADMIN'
        )
        self.message_user(request, f'{count} sessões encerradas com sucesso.')
    encerrar_sessoes.short_description = 'Encerrar sessões selecionadas'


@admin.register(ConfiguracaoAuditoria)
class ConfiguracaoAuditoriaAdmin(admin.ModelAdmin):
    """Admin para Configuração de Auditoria"""
    
    list_display = [
        'empresa', 'registrar_alteracoes', 'registrar_exclusoes',
        'dias_retencao_logs', 'notificar_acessos_suspeitos'
    ]
    list_filter = [
        'registrar_visualizacoes', 'registrar_exportacoes',
        'registrar_alteracoes', 'registrar_exclusoes'
    ]
    search_fields = ['empresa__razao_social']
    
    fieldsets = (
        ('Empresa', {
            'fields': ('empresa',)
        }),
        ('Configurações de Registro', {
            'fields': (
                'registrar_visualizacoes', 'registrar_exportacoes',
                'registrar_alteracoes', 'registrar_exclusoes'
            )
        }),
        ('Retenção de Dados', {
            'fields': ('dias_retencao_logs', 'dias_retencao_logs_acesso')
        }),
        ('Notificações', {
            'fields': (
                'notificar_acessos_suspeitos', 'notificar_alteracoes_criticas',
                'email_notificacao'
            )
        }),
        ('Módulos', {
            'fields': ('modulos_auditados',)
        }),
    )
