"""
Views para o módulo de Ferramentas
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Ferramenta, EmprestimoFerramenta, ManutencaoFerramenta, CalibracaoFerramenta
from .serializers import FerramentaSerializer, EmprestimoFerramentaSerializer, ManutencaoFerramentaSerializer, CalibracaoFerramentaSerializer


class FerramentaViewSet(viewsets.ModelViewSet):
    """ViewSet para Ferramenta"""
    permission_classes = [IsAuthenticated]
    serializer_class = FerramentaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Ferramenta.objects.all()
        return Ferramenta.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class EmprestimoFerramentaViewSet(viewsets.ModelViewSet):
    """ViewSet para EmprestimoFerramenta"""
    permission_classes = [IsAuthenticated]
    serializer_class = EmprestimoFerramentaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return EmprestimoFerramenta.objects.all()
        return EmprestimoFerramenta.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class ManutencaoFerramentaViewSet(viewsets.ModelViewSet):
    """ViewSet para ManutencaoFerramenta"""
    permission_classes = [IsAuthenticated]
    serializer_class = ManutencaoFerramentaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ManutencaoFerramenta.objects.all()
        return ManutencaoFerramenta.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class CalibracaoFerramentaViewSet(viewsets.ModelViewSet):
    """ViewSet para CalibracaoFerramenta"""
    permission_classes = [IsAuthenticated]
    serializer_class = CalibracaoFerramentaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return CalibracaoFerramenta.objects.all()
        return CalibracaoFerramenta.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


