"""
Views expandidas para o módulo de Estoque
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    CategoriaProduto, Produto, SaldoEstoque,
    MovimentacaoEstoque, PrevisaoDemanda, CurvaABC
)
from .serializers import (
    CategoriaProdutoSerializer, ProdutoSerializer, SaldoEstoqueSerializer,
    MovimentacaoEstoqueSerializer, PrevisaoDemandaSerializer, CurvaABCSerializer
)


class CategoriaProdutoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CategoriaProdutoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['ativo']
    search_fields = ['codigo', 'nome']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return CategoriaProduto.objects.all()
        return CategoriaProduto.objects.filter(empresa=user.empresa)


class ProdutoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProdutoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'ativo']
    search_fields = ['codigo', 'descricao', 'codigo_barras']
    ordering_fields = ['codigo', 'descricao', 'custo_medio']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Produto.objects.all()
        return Produto.objects.filter(empresa=user.empresa)
    
    @action(detail=False, methods=['get'])
    def reposicao(self, request):
        """Produtos que necessitam reposição"""
        queryset = self.get_queryset()
        produtos_reposicao = [p for p in queryset if p.necessita_reposicao]
        serializer = self.get_serializer(produtos_reposicao, many=True)
        return Response(serializer.data)


class SaldoEstoqueViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SaldoEstoqueSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['produto', 'ativo']
    search_fields = ['produto__codigo', 'produto__descricao']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return SaldoEstoque.objects.all()
        return SaldoEstoque.objects.filter(produto__empresa=user.empresa)


class MovimentacaoEstoqueViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MovimentacaoEstoqueSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['produto', 'tipo']
    search_fields = ['produto__codigo', 'documento_referencia']
    ordering_fields = ['data_movimentacao']
    ordering = ['-data_movimentacao']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return MovimentacaoEstoque.objects.all()
        return MovimentacaoEstoque.objects.filter(produto__empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(responsavel=self.request.user)


class PrevisaoDemandaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PrevisaoDemandaSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['produto', 'metodo_previsao']
    ordering_fields = ['mes_referencia']
    ordering = ['-mes_referencia']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return PrevisaoDemanda.objects.all()
        return PrevisaoDemanda.objects.filter(produto__empresa=user.empresa)


class CurvaABCViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CurvaABCSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['produto', 'classificacao']
    ordering_fields = ['valor_total_vendas']
    ordering = ['-valor_total_vendas']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return CurvaABC.objects.all()
        return CurvaABC.objects.filter(produto__empresa=user.empresa)
