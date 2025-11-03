from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from backend.common.serializers import CustomTokenObtainPairSerializer

from .models import UsuarioMotorista
from .serializers import UsuarioMotoristaSerializer








@api_view(['GET'])
@permission_classes([IsAuthenticated])
def perfil_motorista(request):
    if not isinstance(request.user, UsuarioMotorista):
        return Response({'error': 'Acesso negado'}, status=status.HTTP_403_FORBIDDEN)
    return Response(UsuarioMotoristaSerializer(request.user).data)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_motorista(request):
    serializer = CustomTokenObtainPairSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = getattr(serializer, "user", None)
    if not isinstance(user, UsuarioMotorista):
        return Response(
            {"error": "As credenciais não correspondem a um usuário motorista."},
            status=status.HTTP_403_FORBIDDEN,
        )

    data = serializer.validated_data.copy()
    data["tokens"] = {"access": data["access"], "refresh": data["refresh"]}

    return Response(data, status=status.HTTP_200_OK)
