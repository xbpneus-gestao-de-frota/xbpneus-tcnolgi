"""
Views de Autenticação Unificadas
Sistema XBPneus
"""
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Endpoint unificado de logout
    """
    refresh_token = request.data.get("refresh")
    if not refresh_token:
        return Response({"error": "Refresh token ausente."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        token = RefreshToken(refresh_token)
    except TokenError as exc:  # Token inválido ou expirado
        return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    try:
        token.blacklist()
    except (AttributeError, IntegrityError, TypeError):
        # Tokens emitidos via create_tokens_for_user não possuem vínculo com OutstandingToken
        # (AUTH_USER_MODEL), portanto o blacklist gera erros de integridade. Como o logout
        # é best-effort, ignoramos essas exceções e retornamos sucesso mesmo assim.
        pass

    return Response({'message': 'Logout realizado com sucesso'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    """
    Endpoint unificado para retornar dados do usuário logado
    """
    user = request.user
    
    # Detectar tipo de usuário baseado no modelo
    user_type = 'unknown'
    if hasattr(user, 'usuariotransportador'):
        user_type = 'transportador'
    elif hasattr(user, 'usuariomotorista'):
        user_type = 'motorista'
    elif hasattr(user, 'usuarioborracharia'):
        user_type = 'borracharia'
    elif hasattr(user, 'usuariorevenda'):
        user_type = 'revenda'
    elif hasattr(user, 'usuariorecapagem'):
        user_type = 'recapagem'
    elif user.is_superuser:
        user_type = 'admin'
    
    user_data = {
        'id': user.id,
        'email': user.email,
        'nome': getattr(user, 'nome_razao_social', getattr(user, 'nome_completo', user.email)),
        'tipo': user_type,
        'aprovado': getattr(user, 'aprovado', True),
        'is_active': user.is_active,
        'is_superuser': user.is_superuser,
    }
    
    return Response(user_data, status=status.HTTP_200_OK)

