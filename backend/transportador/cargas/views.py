"""
Views para o módulo de Cargas
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import TipoCarga, Carga, ItemCarga, ManifestoCarga, RastreamentoCarga
from .serializers import TipoCargaSerializer, CargaSerializer, ItemCargaSerializer, ManifestoCargaSerializer, RastreamentoCargaSerializer


class TipoCargaViewSet(viewsets.ModelViewSet):
    """ViewSet para TipoCarga"""
    permission_classes = [IsAuthenticated]
    serializer_class = TipoCargaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return TipoCarga.objects.all()
        return TipoCarga.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class CargaViewSet(viewsets.ModelViewSet):
    """ViewSet para Carga"""
    permission_classes = [IsAuthenticated]
    serializer_class = CargaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Carga.objects.all()
        return Carga.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class ItemCargaViewSet(viewsets.ModelViewSet):
    """ViewSet para ItemCarga"""
    permission_classes = [IsAuthenticated]
    serializer_class = ItemCargaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ItemCarga.objects.all()
        return ItemCarga.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class ManifestoCargaViewSet(viewsets.ModelViewSet):
    """ViewSet para ManifestoCarga"""
    permission_classes = [IsAuthenticated]
    serializer_class = ManifestoCargaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ManifestoCarga.objects.all()
        return ManifestoCarga.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class RastreamentoCargaViewSet(viewsets.ModelViewSet):
    """ViewSet para RastreamentoCarga"""
    permission_classes = [IsAuthenticated]
    serializer_class = RastreamentoCargaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return RastreamentoCarga.objects.all()
        return RastreamentoCarga.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


