"""
Views para o módulo de Almoxarifado
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Almoxarifado, LocalEstoque, MovimentacaoAlmoxarifado,
    InventarioAlmoxarifado, ItemInventario, RequisicaoMaterial, ItemRequisicao
)
from .serializers import (
    AlmoxarifadoSerializer, LocalEstoqueSerializer, MovimentacaoAlmoxarifadoSerializer,
    InventarioAlmoxarifadoSerializer, ItemInventarioSerializer,
    RequisicaoMaterialSerializer, ItemRequisicaoSerializer
)


class AlmoxarifadoViewSet(viewsets.ModelViewSet):
    """ViewSet para Almoxarifado"""
    permission_classes = [IsAuthenticated]
    serializer_class = AlmoxarifadoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo', 'ativo']
    search_fields = ['codigo', 'nome', 'cidade']
    ordering_fields = ['nome', 'codigo']
    ordering = ['nome']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Almoxarifado.objects.all()
        return Almoxarifado.objects.filter(empresa=user.empresa)


class LocalEstoqueViewSet(viewsets.ModelViewSet):
    """ViewSet para Local de Estoque"""
    permission_classes = [IsAuthenticated]
    serializer_class = LocalEstoqueSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['almoxarifado', 'ativo']
    search_fields = ['codigo', 'descricao']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return LocalEstoque.objects.all()
        return LocalEstoque.objects.filter(almoxarifado__empresa=user.empresa)


class MovimentacaoAlmoxarifadoViewSet(viewsets.ModelViewSet):
    """ViewSet para Movimentação de Almoxarifado"""
    permission_classes = [IsAuthenticated]
    serializer_class = MovimentacaoAlmoxarifadoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['almoxarifado', 'tipo']
    search_fields = ['numero', 'codigo_produto', 'descricao_produto']
    ordering_fields = ['data_movimentacao']
    ordering = ['-data_movimentacao']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return MovimentacaoAlmoxarifado.objects.all()
        return MovimentacaoAlmoxarifado.objects.filter(almoxarifado__empresa=user.empresa)


class InventarioAlmoxarifadoViewSet(viewsets.ModelViewSet):
    """ViewSet para Inventário de Almoxarifado"""
    permission_classes = [IsAuthenticated]
    serializer_class = InventarioAlmoxarifadoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['almoxarifado', 'status']
    ordering_fields = ['data_inventario']
    ordering = ['-data_inventario']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return InventarioAlmoxarifado.objects.all()
        return InventarioAlmoxarifado.objects.filter(almoxarifado__empresa=user.empresa)


class ItemInventarioViewSet(viewsets.ModelViewSet):
    """ViewSet para Item de Inventário"""
    permission_classes = [IsAuthenticated]
    serializer_class = ItemInventarioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['inventario']
    search_fields = ['codigo_produto', 'descricao_produto']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ItemInventario.objects.all()
        return ItemInventario.objects.filter(inventario__almoxarifado__empresa=user.empresa)


class RequisicaoMaterialViewSet(viewsets.ModelViewSet):
    """ViewSet para Requisição de Material"""
    permission_classes = [IsAuthenticated]
    serializer_class = RequisicaoMaterialSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['almoxarifado', 'status', 'solicitante']
    search_fields = ['numero']
    ordering_fields = ['data_requisicao']
    ordering = ['-data_requisicao']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return RequisicaoMaterial.objects.all()
        return RequisicaoMaterial.objects.filter(almoxarifado__empresa=user.empresa)


class ItemRequisicaoViewSet(viewsets.ModelViewSet):
    """ViewSet para Item de Requisição"""
    permission_classes = [IsAuthenticated]
    serializer_class = ItemRequisicaoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['requisicao']
    search_fields = ['codigo_produto', 'descricao_produto']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ItemRequisicao.objects.all()
        return ItemRequisicao.objects.filter(requisicao__almoxarifado__empresa=user.empresa)
