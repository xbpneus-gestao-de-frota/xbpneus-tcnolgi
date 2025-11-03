from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone

from .models import UsuarioTransportador


@admin.register(UsuarioTransportador)
class UsuarioTransportadorAdmin(UserAdmin):
    model = UsuarioTransportador
    list_display = (
        "email",
        "nome_razao_social",
        "cnpj",
        "aprovado",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    list_filter = ("aprovado", "is_active", "is_staff", "is_superuser")
    search_fields = ("email", "nome_razao_social", "cnpj")
    ordering = ("email",)
    filter_horizontal = ("groups", "user_permissions")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Dados", {"fields": ("nome_razao_social", "cnpj", "telefone")}),
        (
            "Status",
            {
                "fields": (
                    "aprovado",
                    "aprovado_em",
                    "aprovado_por",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        ("Permissões", {"fields": ("groups", "user_permissions")}),
        ("Datas", {"fields": ("last_login", "criado_em", "atualizado_em")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "nome_razao_social",
                    "cnpj",
                    "telefone",
                    "password1",
                    "password2",
                    "aprovado",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    readonly_fields = ("criado_em", "atualizado_em", "aprovado_em", "aprovado_por", "last_login")
    actions = ["aprovar_usuarios", "rejeitar_usuarios"]

    def aprovar_usuarios(self, request, queryset):
        """Aprovar usuários selecionados."""

        count = 0
        for user in queryset:
            if not user.aprovado:
                user.aprovado = True
                user.is_active = True
                user.aprovado_em = timezone.now()
                user.aprovado_por = (
                    request.user.email if getattr(request.user, "email", None) else str(request.user)
                )
                user.save()
                count += 1

        self.message_user(request, f"{count} usuário(s) aprovado(s) com sucesso!")

    aprovar_usuarios.short_description = "Aprovar usuários selecionados"

    def rejeitar_usuarios(self, request, queryset):
        """Rejeitar usuários selecionados."""

        count = queryset.update(aprovado=False, is_active=False)
        self.message_user(request, f"{count} usuário(s) rejeitado(s)!")

    rejeitar_usuarios.short_description = "Rejeitar usuários selecionados"

