from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from backend.common.jwt_utils import create_tokens_for_user, get_dashboard_redirect
from .models import UsuarioMotorista
from .serializers import UsuarioMotoristaSerializer, RegistroMotoristaSerializer, LoginMotoristaSerializer








@api_view(['GET'])
@permission_classes([IsAuthenticated])
def perfil_motorista(request):
    if not isinstance(request.user, UsuarioMotorista):
        return Response({'error': 'Acesso negado'}, status=status.HTTP_403_FORBIDDEN)
    return Response(UsuarioMotoristaSerializer(request.user).data)
