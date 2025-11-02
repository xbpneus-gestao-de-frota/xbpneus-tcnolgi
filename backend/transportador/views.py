from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from backend.common.jwt_utils import create_tokens_for_user, get_dashboard_redirect
from django.contrib.auth import authenticate
from .models import UsuarioTransportador
from .serializers import (
    UsuarioTransportadorSerializer,
    RegistroTransportadorSerializer,
    LoginTransportadorSerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])
def registro_transportador(request):
    """Endpoint para registro de novo transportador"""
    serializer = RegistroTransportadorSerializer(data=request.data)
    
    print(f"Dados recebidos para registro: {request.data}")
    if not serializer.is_valid():
        print(f"Erros de validação do serializer: {serializer.errors}")
    if serializer.is_valid():
        print("Serializer é válido.")
        user = serializer.save()
        return Response({
            'message': 'Cadastro realizado com sucesso! Aguarde aprovação do administrador.',
            'user': UsuarioTransportadorSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_transportador(request):
    """Endpoint para login de transportador"""
    serializer = LoginTransportadorSerializer(data=request.data)
    
    if not serializer.is_valid():
        print(f"Erros de validação do serializer: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']
    
    try:
        user = UsuarioTransportador.objects.get(email=email)
    except UsuarioTransportador.DoesNotExist:
        return Response({
            'error': 'Credenciais inválidas'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    if not user.check_password(password):
        return Response({
            'error': 'Credenciais inválidas'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    if not user.aprovado:
        return Response({
            'error': 'Seu cadastro ainda não foi aprovado pelo administrador'
        }, status=status.HTTP_403_FORBIDDEN)
    
    if not user.is_active:
        return Response({
            'error': 'Sua conta está inativa'
        }, status=status.HTTP_403_FORBIDDEN)
    
    # Cria tokens JWT customizados que funcionam com múltiplos tipos de usuário
    tokens = create_tokens_for_user(user)
    redirect_url = get_dashboard_redirect(user)
    
    return Response({
        'message': 'Login realizado com sucesso',
        'user': UsuarioTransportadorSerializer(user).data,
        'tokens': tokens,
        'redirect': redirect_url
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def perfil_transportador(request):
    """Endpoint para obter perfil do transportador logado"""
    if not isinstance(request.user, UsuarioTransportador):
        return Response({
            'error': 'Acesso negado'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = UsuarioTransportadorSerializer(request.user)
    return Response(serializer.data)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_transportador(request):
    """Endpoint para logout de transportador"""
    try:
        # Invalidar token se estiver usando JWT com blacklist
        # Por enquanto, apenas retorna sucesso pois o token expira naturalmente
        return Response({
            'message': 'Logout realizado com sucesso'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

