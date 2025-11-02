"""
Views para o módulo de Epis
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import TipoEPI, EPI, EntregaEPI, FichaEPI
from .serializers import TipoEPISerializer, EPISerializer, EntregaEPISerializer, FichaEPISerializer


class TipoEPIViewSet(viewsets.ModelViewSet):
    """ViewSet para TipoEPI"""
    permission_classes = [IsAuthenticated]
    serializer_class = TipoEPISerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return TipoEPI.objects.all()
        return TipoEPI.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class EPIViewSet(viewsets.ModelViewSet):
    """ViewSet para EPI"""
    permission_classes = [IsAuthenticated]
    serializer_class = EPISerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return EPI.objects.all()
        return EPI.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class EntregaEPIViewSet(viewsets.ModelViewSet):
    """ViewSet para EntregaEPI"""
    permission_classes = [IsAuthenticated]
    serializer_class = EntregaEPISerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return EntregaEPI.objects.all()
        return EntregaEPI.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class FichaEPIViewSet(viewsets.ModelViewSet):
    """ViewSet para FichaEPI"""
    permission_classes = [IsAuthenticated]
    serializer_class = FichaEPISerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return FichaEPI.objects.all()
        return FichaEPI.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


