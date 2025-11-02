"""
Utilitários JWT Customizados para Múltiplos Tipos de Usuário
Sistema XBPNEUS v10

Este módulo fornece funções para gerar tokens JWT que funcionam
com múltiplos modelos de usuário independentes, sem depender do
AUTH_USER_MODEL do Django.
"""

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.contenttypes.models import ContentType


def create_tokens_for_user(user):
    """
    Cria tokens JWT (access e refresh) para qualquer tipo de usuário.
    
    Esta função contorna o problema do OutstandingToken que depende
    do AUTH_USER_MODEL, criando tokens sem registrá-los no blacklist.
    
    Args:
        user: Instância de qualquer modelo de usuário (UsuarioTransportador,
              UsuarioMotorista, UsuarioBorracharia, UsuarioRevenda, UsuarioRecapagem)
    
    Returns:
        dict: Dicionário com 'access' e 'refresh' tokens
    
    Example:
        >>> from backend.motorista.models import UsuarioMotorista
        >>> user = UsuarioMotorista.objects.get(email='teste@example.com')
        >>> tokens = create_tokens_for_user(user)
        >>> print(tokens['access'])
    """
    
    # Cria o refresh token
    refresh = RefreshToken()
    
    # Adiciona claims customizados
    refresh['user_id'] = user.id
    refresh['email'] = user.email

    # Identifica o tipo de usuário usando ContentType
    content_type = ContentType.objects.get_for_model(user)
    user_type = f"{content_type.app_label}.{content_type.model}"
    refresh['user_type'] = user_type

    # Define o papel (role) do usuário para ser utilizado no frontend
    role_map = {
        'usuariotransportador': 'transportador',
        'usuariomotorista': 'motorista',
        'usuarioborracharia': 'borracharia',
        'usuariorevenda': 'revenda',
        'usuariorecapagem': 'recapagem',
        'motoristaexterno': 'motorista_externo',
    }
    refresh['user_role'] = role_map.get(content_type.model, 'transportador')
    
    # Adiciona nome do usuário
    if hasattr(user, 'nome_completo'):
        refresh['name'] = user.nome_completo
    elif hasattr(user, 'nome_razao_social'):
        refresh['name'] = user.nome_razao_social
    else:
        refresh['name'] = user.email
    
    # Adiciona informações de aprovação
    refresh['aprovado'] = getattr(user, 'aprovado', True)
    refresh['is_active'] = user.is_active
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def get_user_from_token(token):
    """
    Recupera o usuário a partir de um token JWT.
    
    Args:
        token: Token JWT (access ou refresh)
    
    Returns:
        Instância do usuário ou None se não encontrado
    
    Example:
        >>> from rest_framework_simplejwt.tokens import AccessToken
        >>> token = AccessToken(token_string)
        >>> user = get_user_from_token(token)
    """
    try:
        user_type = token.get('user_type')
        user_id = token.get('user_id')
        
        if not user_type or not user_id:
            return None
        
        # Separa app_label e model
        app_label, model = user_type.split('.')
        
        # Obtém o ContentType
        content_type = ContentType.objects.get(app_label=app_label, model=model)
        
        # Obtém o modelo
        model_class = content_type.model_class()
        
        # Busca o usuário
        return model_class.objects.get(id=user_id)
        
    except Exception:
        return None


def verify_user_access(user, required_type=None):
    """
    Verifica se o usuário tem acesso permitido.
    
    Args:
        user: Instância do usuário
        required_type: Tipo de usuário requerido (opcional)
    
    Returns:
        tuple: (bool, str) - (tem_acesso, mensagem_erro)
    
    Example:
        >>> has_access, error = verify_user_access(user, 'motorista')
        >>> if not has_access:
        >>>     return Response({'error': error}, status=403)
    """
    
    # Verifica se o usuário está aprovado
    if hasattr(user, 'aprovado') and not user.aprovado:
        return False, 'Seu cadastro ainda não foi aprovado pelo administrador'
    
    # Verifica se o usuário está ativo
    if not user.is_active:
        return False, 'Sua conta está inativa'
    
    # Verifica o tipo de usuário se especificado
    if required_type:
        content_type = ContentType.objects.get_for_model(user)
        user_type = content_type.model
        
        if user_type != f'usuario{required_type}':
            return False, f'Acesso negado. Esta área é restrita a usuários do tipo {required_type}'
    
    return True, ''


def get_dashboard_redirect(user):
    """
    Retorna a URL de redirecionamento do dashboard baseado no tipo de usuário.
    
    Args:
        user: Instância do usuário
    
    Returns:
        str: URL do dashboard
    
    Example:
        >>> redirect_url = get_dashboard_redirect(user)
        >>> return Response({'redirect': redirect_url})
    """
    
    content_type = ContentType.objects.get_for_model(user)
    user_type = content_type.model
    
    # Mapeamento de tipos de usuário para dashboards
    dashboard_map = {
        'usuariotransportador': '/transportador/dashboard/',
        'usuariomotorista': '/motorista/dashboard/',
        'usuarioborracharia': '/borracharia/dashboard/',
        'usuariorevenda': '/revenda/dashboard/',
        'usuariorecapagem': '/recapagem/dashboard/',
    }
    
    return dashboard_map.get(user_type, '/')


# Função auxiliar para compatibilidade com código existente
def for_user(user):
    """
    Função de compatibilidade que imita RefreshToken.for_user()
    mas funciona com múltiplos tipos de usuário.
    
    Args:
        user: Instância de qualquer modelo de usuário
    
    Returns:
        dict: Tokens JWT
    """
    return create_tokens_for_user(user)

