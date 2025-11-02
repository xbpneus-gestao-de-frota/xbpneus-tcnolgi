"""
Views para o módulo de Treinamentos
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import CursoTreinamento, TreinamentoRealizado, CertificadoTreinamento, InstrutorTreinamento
from .serializers import CursoTreinamentoSerializer, TreinamentoRealizadoSerializer, CertificadoTreinamentoSerializer, InstrutorTreinamentoSerializer


class CursoTreinamentoViewSet(viewsets.ModelViewSet):
    """ViewSet para CursoTreinamento"""
    permission_classes = [IsAuthenticated]
    serializer_class = CursoTreinamentoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return CursoTreinamento.objects.all()
        return CursoTreinamento.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class TreinamentoRealizadoViewSet(viewsets.ModelViewSet):
    """ViewSet para TreinamentoRealizado"""
    permission_classes = [IsAuthenticated]
    serializer_class = TreinamentoRealizadoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return TreinamentoRealizado.objects.all()
        return TreinamentoRealizado.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class CertificadoTreinamentoViewSet(viewsets.ModelViewSet):
    """ViewSet para CertificadoTreinamento"""
    permission_classes = [IsAuthenticated]
    serializer_class = CertificadoTreinamentoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return CertificadoTreinamento.objects.all()
        return CertificadoTreinamento.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class InstrutorTreinamentoViewSet(viewsets.ModelViewSet):
    """ViewSet para InstrutorTreinamento"""
    permission_classes = [IsAuthenticated]
    serializer_class = InstrutorTreinamentoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return InstrutorTreinamento.objects.all()
        return InstrutorTreinamento.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


