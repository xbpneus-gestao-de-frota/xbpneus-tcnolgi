"""
Views para o módulo de Pecas
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import CategoriaPeca, Peca, EstoquePeca, MovimentacaoPeca, FornecedorPeca
from .serializers import CategoriaPecaSerializer, PecaSerializer, EstoquePecaSerializer, MovimentacaoPecaSerializer, FornecedorPecaSerializer


class CategoriaPecaViewSet(viewsets.ModelViewSet):
    """ViewSet para CategoriaPeca"""
    permission_classes = [IsAuthenticated]
    serializer_class = CategoriaPecaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return CategoriaPeca.objects.all()
        return CategoriaPeca.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class PecaViewSet(viewsets.ModelViewSet):
    """ViewSet para Peca"""
    permission_classes = [IsAuthenticated]
    serializer_class = PecaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Peca.objects.all()
        return Peca.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class EstoquePecaViewSet(viewsets.ModelViewSet):
    """ViewSet para EstoquePeca"""
    permission_classes = [IsAuthenticated]
    serializer_class = EstoquePecaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return EstoquePeca.objects.all()
        return EstoquePeca.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class MovimentacaoPecaViewSet(viewsets.ModelViewSet):
    """ViewSet para MovimentacaoPeca"""
    permission_classes = [IsAuthenticated]
    serializer_class = MovimentacaoPecaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return MovimentacaoPeca.objects.all()
        return MovimentacaoPeca.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class FornecedorPecaViewSet(viewsets.ModelViewSet):
    """ViewSet para FornecedorPeca"""
    permission_classes = [IsAuthenticated]
    serializer_class = FornecedorPecaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return FornecedorPeca.objects.all()
        return FornecedorPeca.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


