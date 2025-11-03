from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from backend.common.jwt_utils import create_tokens_for_user, get_dashboard_redirect

from .models import UsuarioMotorista
from .serializers import LoginMotoristaSerializer, RegistroMotoristaSerializer, UsuarioMotoristaSerializer








@api_view(['GET'])
@permission_classes([IsAuthenticated])
def perfil_motorista(request):
    if not isinstance(request.user, UsuarioMotorista):
        return Response({'error': 'Acesso negado'}, status=status.HTTP_403_FORBIDDEN)
    return Response(UsuarioMotoristaSerializer(request.user).data)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_motorista(request):
    serializer = LoginMotoristaSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data['email']
    password = serializer.validated_data['password']

    try:
        user = UsuarioMotorista.objects.get(email__iexact=email)
    except UsuarioMotorista.DoesNotExist as exc:
        raise AuthenticationFailed(
            "No active account found with the given credentials",
            code="no_active_account",
        ) from exc

    if not user.check_password(password):
        raise AuthenticationFailed(
            "No active account found with the given credentials",
            code="no_active_account",
        )

    if not user.aprovado:
        return Response(
            {"error": "Seu cadastro ainda não foi aprovado pelo administrador."},
            status=status.HTTP_403_FORBIDDEN,
        )

    if not user.is_active:
        raise AuthenticationFailed(
            "No active account found with the given credentials",
            code="no_active_account",
        )

    tokens = create_tokens_for_user(user)

    payload = {
        "access": tokens["access"],
        "refresh": tokens["refresh"],
        "tokens": tokens,
        "redirect": get_dashboard_redirect(user),
        "user": {
            "id": user.pk,
            "email": user.email,
            "nome": user.nome_completo,
            "aprovado": user.aprovado,
            "is_active": user.is_active,
            "tipo": "motorista",
        },
    }

    return Response(payload, status=status.HTTP_200_OK)
