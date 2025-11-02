from django.contrib import admin
from .models import CanalNotificacao, Notificacao, TemplateNotificacao, PreferenciaNotificacao

@admin.register(CanalNotificacao)
class CanalNotificacaoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'ativo']
    list_filter = ['tipo', 'ativo']
    search_fields = ['nome']

@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'canal', 'destinatario_usuario', 'status', 'prioridade', 'criado_em']
    list_filter = ['status', 'prioridade', 'categoria']
    search_fields = ['titulo', 'mensagem']
    date_hierarchy = 'criado_em'

@admin.register(TemplateNotificacao)
class TemplateNotificacaoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'ativo']
    list_filter = ['categoria', 'ativo']
    search_fields = ['nome', 'descricao']

@admin.register(PreferenciaNotificacao)
class PreferenciaNotificacaoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'email_habilitado', 'sms_habilitado', 'push_habilitado']
    list_filter = ['email_habilitado', 'sms_habilitado', 'push_habilitado']
    search_fields = ['usuario__username']
