"""
Views para o módulo de Relatorios
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import RelatorioTemplate, RelatorioAgendado, RelatorioGerado, DashboardPersonalizado
from .serializers import RelatorioTemplateSerializer, RelatorioAgendadoSerializer, RelatorioGeradoSerializer, DashboardPersonalizadoSerializer


class RelatorioTemplateViewSet(viewsets.ModelViewSet):
    """ViewSet para RelatorioTemplate"""
    permission_classes = [IsAuthenticated]
    serializer_class = RelatorioTemplateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return RelatorioTemplate.objects.all()
        return RelatorioTemplate.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class RelatorioAgendadoViewSet(viewsets.ModelViewSet):
    """ViewSet para RelatorioAgendado"""
    permission_classes = [IsAuthenticated]
    serializer_class = RelatorioAgendadoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return RelatorioAgendado.objects.all()
        return RelatorioAgendado.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class RelatorioGeradoViewSet(viewsets.ModelViewSet):
    """ViewSet para RelatorioGerado"""
    permission_classes = [IsAuthenticated]
    serializer_class = RelatorioGeradoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return RelatorioGerado.objects.all()
        return RelatorioGerado.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class DashboardPersonalizadoViewSet(viewsets.ModelViewSet):
    """ViewSet para DashboardPersonalizado"""
    permission_classes = [IsAuthenticated]
    serializer_class = DashboardPersonalizadoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return DashboardPersonalizado.objects.all()
        return DashboardPersonalizado.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


