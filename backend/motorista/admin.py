from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils import timezone
from .models import UsuarioMotorista


@admin.register(UsuarioMotorista)
class UsuarioMotoristaAdmin(BaseUserAdmin):
    list_display = ['email', 'nome_completo', 'cpf', 'cnh', 'aprovado', 'is_active', 'criado_em']
    list_filter = ['aprovado', 'is_active', 'categoria_cnh', 'criado_em']
    search_fields = ['email', 'nome_completo', 'cpf', 'cnh']
    ordering = ['-criado_em']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('nome_completo', 'cpf', 'cnh', 'categoria_cnh', 'telefone')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Aprovação', {'fields': ('aprovado', 'aprovado_em', 'aprovado_por')}),
        ('Datas', {'fields': ('criado_em', 'atualizado_em')}),
    )
    
    readonly_fields = ['criado_em', 'atualizado_em']
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome_completo', 'cpf', 'cnh', 'categoria_cnh', 'telefone', 'password1', 'password2'),
        }),
    )
    
    actions = ['aprovar_usuarios', 'rejeitar_usuarios']
    
    def aprovar_usuarios(self, request, queryset):
        """Aprovar usuários selecionados"""
        count = 0
        for user in queryset:
            if not user.aprovado:
                user.aprovado = True
                user.is_active = True
                user.aprovado_em = timezone.now()
                user.aprovado_por = request.user.email if hasattr(request.user, 'email') else str(request.user)
                user.save()
                count += 1
        
        self.message_user(request, f'{count} usuário(s) aprovado(s) com sucesso!')
    aprovar_usuarios.short_description = 'Aprovar usuários selecionados'
    
    def rejeitar_usuarios(self, request, queryset):
        """Rejeitar usuários selecionados"""
        count = queryset.update(aprovado=False, is_active=False)
        self.message_user(request, f'{count} usuário(s) rejeitado(s)!')
    rejeitar_usuarios.short_description = 'Rejeitar usuários selecionados'
