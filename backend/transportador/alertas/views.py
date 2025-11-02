"""
Views para o módulo de Alertas
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import TipoAlerta, Alerta, ConfiguracaoAlerta, HistoricoAlerta
from .serializers import TipoAlertaSerializer, AlertaSerializer, ConfiguracaoAlertaSerializer, HistoricoAlertaSerializer


class TipoAlertaViewSet(viewsets.ModelViewSet):
    """ViewSet para TipoAlerta"""
    permission_classes = [IsAuthenticated]
    serializer_class = TipoAlertaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return TipoAlerta.objects.all()
        return TipoAlerta.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class AlertaViewSet(viewsets.ModelViewSet):
    """ViewSet para Alerta"""
    permission_classes = [IsAuthenticated]
    serializer_class = AlertaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Alerta.objects.all()
        return Alerta.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class ConfiguracaoAlertaViewSet(viewsets.ModelViewSet):
    """ViewSet para ConfiguracaoAlerta"""
    permission_classes = [IsAuthenticated]
    serializer_class = ConfiguracaoAlertaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ConfiguracaoAlerta.objects.all()
        return ConfiguracaoAlerta.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class HistoricoAlertaViewSet(viewsets.ModelViewSet):
    """ViewSet para HistoricoAlerta"""
    permission_classes = [IsAuthenticated]
    serializer_class = HistoricoAlertaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return HistoricoAlerta.objects.all()
        return HistoricoAlerta.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


