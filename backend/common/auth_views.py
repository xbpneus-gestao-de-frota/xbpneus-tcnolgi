"""
Views de Autenticação Unificadas
Sistema XBPneus
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Endpoint unificado de logout
    """
    try:
        # Adicionar o token de refresh à blacklist
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({
            'message': 'Logout realizado com sucesso'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


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

