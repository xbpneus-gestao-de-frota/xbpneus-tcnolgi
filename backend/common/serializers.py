from datetime import datetime

from django.utils import timezone

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from backend.borracharia.models import UsuarioBorracharia
from backend.common.jwt_utils import (
    create_tokens_for_user,
    get_dashboard_redirect,
    get_user_from_token,
)
from backend.motorista.models import UsuarioMotorista
from backend.recapagem.models import UsuarioRecapagem
from backend.revenda.models import UsuarioRevenda
from backend.transportador.models import UsuarioTransportador


class CustomTokenObtainPairSerializer(serializers.Serializer):
    """Serializer de autenticação que suporta múltiplos tipos de usuários."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    default_error_messages = {
        "no_active_account": "No active account found with the given credentials",
    }

    USER_MODEL_MAP = (
        ("transportador", UsuarioTransportador),
        ("motorista", UsuarioMotorista),
        ("borracharia", UsuarioBorracharia),
        ("revenda", UsuarioRevenda),
        ("recapagem", UsuarioRecapagem),
    )

    def _find_user(self, email, password):
        password_candidates = []
        unapproved_match_found = False
        inactive_match_found = False
        email_match_found = False

        for _role, model in self.USER_MODEL_MAP:
            for candidate in model.objects.filter(email__iexact=email):
                email_match_found = True

                if not candidate.check_password(password):
                    continue

                password_candidates.append(candidate)

        if not password_candidates:
            return None, "not_found" if not email_match_found else "invalid_credentials"

        for candidate in sorted(password_candidates, key=self._candidate_sort_key, reverse=True):
            if hasattr(candidate, "aprovado") and not candidate.aprovado:
                unapproved_match_found = True
                continue

            if not getattr(candidate, "is_active", True):
                inactive_match_found = True
                continue

            return candidate, None

        if unapproved_match_found:
            return None, "unapproved"

        if inactive_match_found:
            return None, "inactive"

        return None, "invalid_credentials"

    def _candidate_sort_key(self, user):
        return (
            1 if getattr(user, "aprovado", True) else 0,
            1 if getattr(user, "is_active", True) else 0,
            self._datetime_score(getattr(user, "aprovado_em", None)),
            self._datetime_score(getattr(user, "atualizado_em", None)),
            self._datetime_score(getattr(user, "criado_em", None)),
            self._pk_score(user.pk),
        )

    @staticmethod
    def _datetime_score(value):
        if not isinstance(value, datetime):
            return float("-inf")

        if timezone.is_aware(value):
            value = timezone.make_naive(value, timezone.utc)

        try:
            return value.timestamp()
        except (OverflowError, OSError, ValueError):
            return float("-inf")

    @staticmethod
    def _pk_score(value):
        if isinstance(value, int):
            return value

        if hasattr(value, "int"):
            return value.int

        try:
            return int(value)
        except (TypeError, ValueError):
            return 0

    def _get_role(self, user):
        if getattr(user, "is_superuser", False) or getattr(user, "is_staff", False):
            return "admin"
        for role, model in self.USER_MODEL_MAP:
            if isinstance(user, model):
                return role
        return "transportador"

    def _get_user_display_name(self, user):
        if hasattr(user, "nome_completo"):
            return user.nome_completo
        if hasattr(user, "nome_razao_social"):
            return user.nome_razao_social
        return user.email

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user, status = self._find_user(email, password)

        if not user:
            if status == "unapproved":
                raise PermissionDenied("Usuário não aprovado pelo administrador.")

            raise AuthenticationFailed(
                self.default_error_messages["no_active_account"],
                code="no_active_account",
            )

        if hasattr(user, "aprovado") and not user.aprovado:
            raise PermissionDenied("Usuário não aprovado pelo administrador.")

        if not getattr(user, "is_active", True):
            raise AuthenticationFailed(
                self.default_error_messages["no_active_account"],
                code="no_active_account",
            )

        tokens = create_tokens_for_user(user)
        self.user = user
        role = self._get_role(user)

        user_id = user.pk
        if not isinstance(user_id, int):
            user_id = str(user_id)

        data = {
            "access": tokens["access"],
            "refresh": tokens["refresh"],
            "user_role": role,
            "redirect": get_dashboard_redirect(user),
            "user": {
                "id": user_id,
                "email": user.email,
                "nome": self._get_user_display_name(user),
                "aprovado": getattr(user, "aprovado", True),
                "is_active": getattr(user, "is_active", True),
                "tipo": role,
            },
        }

        self.user = user
        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """Refresh serializer that supports users stored in multiple models."""

    default_error_messages = {
        "no_active_account": "No active account found with the given credentials",
    }

    def validate(self, attrs):  # noqa: D401 - inherited docstring not needed
        try:
            refresh = self.token_class(attrs["refresh"])
            if hasattr(refresh, "check_blacklist"):
                refresh.check_blacklist()
        except TokenError as exc:
            message = str(exc)
            detail = "Token is blacklisted" if "blacklisted" in message.lower() else self.default_error_messages["no_active_account"]
            raise AuthenticationFailed(detail, code="token_not_valid") from exc

        user = get_user_from_token(refresh)
        if not user:
            try:
                from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

                jti = refresh.get("jti")
                if jti:
                    outstanding = OutstandingToken.objects.filter(jti=jti).first()
                    if outstanding and BlacklistedToken.objects.filter(token=outstanding).exists():
                        raise AuthenticationFailed("Token is blacklisted", code="token_not_valid")
            except Exception:
                pass

            raise AuthenticationFailed(
                self.default_error_messages["no_active_account"],
                code="no_active_account",
            )

        if hasattr(user, "aprovado") and not user.aprovado:
            raise PermissionDenied("Usuário não aprovado pelo administrador.")

        if not getattr(user, "is_active", True):
            raise AuthenticationFailed(
                self.default_error_messages["no_active_account"],
                code="no_active_account",
            )

        tokens = create_tokens_for_user(user)

        return {"access": tokens["access"]}

