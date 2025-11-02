from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action, api_view, permission_classes as drf_permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django_filters.rest_framework import DjangoFilterBackend

from .models import Empresa, Filial, Transportador
from .serializers import (
    EmpresaSerializer,
    EmpresaListSerializer,
    FilialSerializer,
    FilialListSerializer,
)


class EmpresaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Empresas.
    Fornece operações CRUD completas com filtros e buscas.
    """
    queryset = Empresa.objects.all().order_by('nome')
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo', 'ativa', 'estado', 'cidade']
    search_fields = ['nome', 'cnpj', 'razao_social', 'nome_fantasia', 'email']
    ordering_fields = ['nome', 'tipo', 'criado_em']
    
    def get_serializer_class(self):
        """Retorna serializer apropriado para a ação"""
        if self.action == 'list':
            return EmpresaListSerializer
        return EmpresaSerializer
    
    @action(detail=True, methods=['get'])
    def filiais(self, request, pk=None):
        """Retorna todas as filiais de uma empresa"""
        empresa = self.get_object()
        filiais = empresa.filiais.all()
        serializer = FilialListSerializer(filiais, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def ativar(self, request, pk=None):
        """Ativa uma empresa"""
        empresa = self.get_object()
        empresa.ativa = True
        empresa.save()
        return Response({'status': 'Empresa ativada com sucesso'})
    
    @action(detail=True, methods=['post'])
    def desativar(self, request, pk=None):
        """Desativa uma empresa"""
        empresa = self.get_object()
        empresa.ativa = False
        empresa.save()
        return Response({'status': 'Empresa desativada com sucesso'})


class FilialViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Filiais.
    Fornece operações CRUD completas com filtros e buscas.
    """
    queryset = Filial.objects.all().select_related('empresa').order_by('empresa', 'codigo')
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['empresa', 'ativa', 'matriz', 'estado', 'cidade']
    search_fields = ['nome', 'codigo', 'cnpj', 'email']
    ordering_fields = ['nome', 'codigo', 'criado_em']
    
    def get_serializer_class(self):
        """Retorna serializer apropriado para a ação"""
        if self.action == 'list':
            return FilialListSerializer
        return FilialSerializer
    
    @action(detail=True, methods=['post'])
    def ativar(self, request, pk=None):
        """Ativa uma filial"""
        filial = self.get_object()
        filial.ativa = True
        filial.save()
        return Response({'status': 'Filial ativada com sucesso'})
    
    @action(detail=True, methods=['post'])
    def desativar(self, request, pk=None):
        """Desativa uma filial"""
        filial = self.get_object()
        filial.ativa = False
        filial.save()
        return Response({'status': 'Filial desativada com sucesso'})
    
    @action(detail=True, methods=['post'])
    def definir_matriz(self, request, pk=None):
        """Define uma filial como matriz"""
        filial = self.get_object()
        
        # Remove flag de matriz de outras filiais da mesma empresa
        Filial.objects.filter(empresa=filial.empresa, matriz=True).update(matriz=False)
        
        # Define esta filial como matriz
        filial.matriz = True
        filial.save()
        
        return Response({'status': 'Filial definida como matriz com sucesso'})


# Endpoint de registro de transportador (mantido da versão anterior)
@api_view(['POST'])
@drf_permission_classes([AllowAny])
def register_transportador(request):
    """
    Endpoint para cadastro de transportador.
    Cria registro com status PENDENTE aguardando aprovação do admin.
    """
    data = request.data
    
    # Validar campos obrigatórios
    required_fields = ['nome', 'cnpj', 'email', 'senha', 'contato']
    for field in required_fields:
        if not data.get(field):
            return Response(
                {'detail': f'Campo obrigatório: {field}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # Verificar se email já existe
    if Transportador.objects.filter(email=data['email']).exists():
        return Response(
            {'detail': 'Email já cadastrado'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Verificar se CNPJ já existe
    if Transportador.objects.filter(cnpj=data['cnpj']).exists():
        return Response(
            {'detail': 'CNPJ já cadastrado'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Criar registro de transportador com status PENDENTE
    try:
        transportador = Transportador.objects.create(
            razao=data['nome'],
            cnpj=data['cnpj'],
            email=data['email'],
            senha=make_password(data['senha']),
            telefone=data.get('contato', ''),
            estado=data.get('estado', ''),
            cidade=data.get('cidade', ''),
            status='PENDENTE'
        )
        
        return Response({
            'detail': 'Cadastro realizado com sucesso! Aguarde aprovação do administrador.',
            'transportador': {
                'id': transportador.id,
                'nome': transportador.razao,
                'email': transportador.email,
                'status': transportador.status
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'detail': f'Erro ao criar cadastro: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

