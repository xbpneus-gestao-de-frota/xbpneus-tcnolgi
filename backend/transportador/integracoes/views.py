"""
Views para o módulo de Integracoes
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import IntegracaoExterna, LogIntegracao, WebhookConfig, APICredential
from .serializers import IntegracaoExternaSerializer, LogIntegracaoSerializer, WebhookConfigSerializer, APICredentialSerializer


class IntegracaoExternaViewSet(viewsets.ModelViewSet):
    """ViewSet para IntegracaoExterna"""
    permission_classes = [IsAuthenticated]
    serializer_class = IntegracaoExternaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return IntegracaoExterna.objects.all()
        return IntegracaoExterna.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class LogIntegracaoViewSet(viewsets.ModelViewSet):
    """ViewSet para LogIntegracao"""
    permission_classes = [IsAuthenticated]
    serializer_class = LogIntegracaoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return LogIntegracao.objects.all()
        return LogIntegracao.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class WebhookConfigViewSet(viewsets.ModelViewSet):
    """ViewSet para WebhookConfig"""
    permission_classes = [IsAuthenticated]
    serializer_class = WebhookConfigSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return WebhookConfig.objects.all()
        return WebhookConfig.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class APICredentialViewSet(viewsets.ModelViewSet):
    """ViewSet para APICredential"""
    permission_classes = [IsAuthenticated]
    serializer_class = APICredentialSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return APICredential.objects.all()
        return APICredential.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


