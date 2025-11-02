from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

from backend.common.jwt_utils import get_user_from_token

class CustomUserAuthenticationRule:
    """
    Regra de autenticação customizada para JWT que verifica se o usuário
    está ativo e aprovado.
    """
    def authenticate(self, user):
        # A autenticação básica do JWT já foi feita.
        # Aqui, verificamos as regras de negócio adicionais.
        
        if not user.is_active:
            # Esta verificação é redundante, pois o ModelBackend já a faz,
            # mas a mantemos para ser explícita no fluxo do SimpleJWT.
            raise InvalidToken("Usuário inativo.")
        
        # O campo 'aprovado' é customizado para o sistema XBPneus.
        # O problema no login da API é que a autenticação falha antes de chegar aqui,
        # mas esta regra é crucial para a validação do token após a obtenção.
        if hasattr(user, 'aprovado') and not user.aprovado:
            raise InvalidToken("Usuário não aprovado pelo administrador.")

        return user


class MultiModelJWTAuthentication(JWTAuthentication):
    """Autenticação JWT que suporta múltiplos modelos de usuário."""

    def get_user(self, validated_token):
        user = get_user_from_token(validated_token)

        if user is None:
            raise InvalidToken("Token inválido: usuário não encontrado.")

        if hasattr(user, 'aprovado') and not user.aprovado:
            raise InvalidToken("Usuário não aprovado pelo administrador.")

        if not getattr(user, 'is_active', True):
            raise InvalidToken("Usuário inativo.")

        return user
