"""
Views para o módulo de Compliance
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import NormaCompliance, AuditoriaCompliance, NaoConformidade, PlanoAcaoCompliance
from .serializers import NormaComplianceSerializer, AuditoriaComplianceSerializer, NaoConformidadeSerializer, PlanoAcaoComplianceSerializer


class NormaComplianceViewSet(viewsets.ModelViewSet):
    """ViewSet para NormaCompliance"""
    permission_classes = [IsAuthenticated]
    serializer_class = NormaComplianceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return NormaCompliance.objects.all()
        return NormaCompliance.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class AuditoriaComplianceViewSet(viewsets.ModelViewSet):
    """ViewSet para AuditoriaCompliance"""
    permission_classes = [IsAuthenticated]
    serializer_class = AuditoriaComplianceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return AuditoriaCompliance.objects.all()
        return AuditoriaCompliance.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class NaoConformidadeViewSet(viewsets.ModelViewSet):
    """ViewSet para NaoConformidade"""
    permission_classes = [IsAuthenticated]
    serializer_class = NaoConformidadeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return NaoConformidade.objects.all()
        return NaoConformidade.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class PlanoAcaoComplianceViewSet(viewsets.ModelViewSet):
    """ViewSet para PlanoAcaoCompliance"""
    permission_classes = [IsAuthenticated]
    serializer_class = PlanoAcaoComplianceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return PlanoAcaoCompliance.objects.all()
        return PlanoAcaoCompliance.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


