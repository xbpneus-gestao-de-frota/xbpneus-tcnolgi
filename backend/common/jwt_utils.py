"""
Utilitários JWT customizados para múltiplos tipos de usuário.

Este módulo fornece funções para gerar tokens JWT compatíveis com
múltiplos modelos de usuário independentes, ao mesmo tempo em que
mantém a integração com os recursos nativos do SimpleJWT (como
blacklist e rotação de tokens) através do uso do RefreshToken.for_user.
"""

from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from rest_framework_simplejwt.tokens import RefreshToken


def create_tokens_for_user(user):
    """
    Cria tokens JWT (access e refresh) para qualquer tipo de usuário.
    
    Sempre que possível utilizamos RefreshToken.for_user para registrar o token
    no banco de dados do SimpleJWT, habilitando blacklist e rotação. Para
    modelos que não são o AUTH_USER_MODEL padrão, recuamos para um token em
    memória mantendo as mesmas claims personalizadas.
    
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
    
    transportador_model = apps.get_model(settings.AUTH_USER_MODEL)
    use_registered_token = isinstance(user, transportador_model)

    if use_registered_token:
        refresh = RefreshToken.for_user(user)
    else:
        refresh = RefreshToken()
        refresh['user_id'] = user.id

    # Adiciona claims customizados mantidos tanto no refresh quanto no access
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
    user_role = role_map.get(content_type.model, 'transportador')
    refresh['user_role'] = user_role
    
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

    # Propaga as informações relevantes também para o access token
    access_token = refresh.access_token
    access_token['user_type'] = user_type
    access_token['user_role'] = user_role
    access_token['email'] = user.email
    access_token['aprovado'] = getattr(user, 'aprovado', True)
    access_token['is_active'] = user.is_active
    
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

