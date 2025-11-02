from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from backend.common.jwt_utils import create_tokens_for_user, get_dashboard_redirect
from .models import UsuarioBorracharia
from .serializers import UsuarioBorrachariaSerializer, RegistroBorrachariaSerializer, LoginBorrachariaSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def registro_borracharia(request):
    serializer = RegistroBorrachariaSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': 'Cadastro realizado com sucesso! Aguarde aprovação do administrador.',
            'user': UsuarioBorrachariaSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_borracharia(request):
    serializer = LoginBorrachariaSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']
    
    try:
        user = UsuarioBorracharia.objects.get(email=email)
    except UsuarioBorracharia.DoesNotExist:
        return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if not user.check_password(password):
        return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if not user.aprovado:
        return Response({'error': 'Seu cadastro ainda não foi aprovado pelo administrador'}, status=status.HTTP_403_FORBIDDEN)
    
    if not user.is_active:
        return Response({'error': 'Sua conta está inativa'}, status=status.HTTP_403_FORBIDDEN)
    
    tokens = create_tokens_for_user(user)
    redirect_url = get_dashboard_redirect(user)
    
    return Response({
        'message': 'Login realizado com sucesso',
        'user': UsuarioBorrachariaSerializer(user).data,
        'tokens': tokens,
        'redirect': redirect_url
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def perfil_borracharia(request):
    if not isinstance(request.user, UsuarioBorracharia):
        return Response({'error': 'Acesso negado'}, status=status.HTTP_403_FORBIDDEN)
    return Response(UsuarioBorrachariaSerializer(request.user).data)
