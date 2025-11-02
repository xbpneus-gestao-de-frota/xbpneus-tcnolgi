from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.common.permissions import OptionalRolePermission
from backend.common.audit import AuditedModelViewSet
from backend.common.export import export_csv, export_xlsx, export_csv_streaming
from .models import CategoriaProduto, Produto, Pedido, ItemPedido, MovimentacaoEstoqueLoja
from .serializers import (
    CategoriaProdutoSerializer, ProdutoSerializer, PedidoSerializer,
    ItemPedidoSerializer, MovimentacaoEstoqueLojaSerializer
)


class CategoriaProdutoViewSet(AuditedModelViewSet):
    queryset = CategoriaProduto.objects.all().order_by('nome')
    serializer_class = CategoriaProdutoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'tipo']
    ordering_fields = ['nome', 'tipo', 'criado_em']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['tipo', 'ativo']


class ProdutoViewSet(AuditedModelViewSet):
    queryset = Produto.objects.all().order_by('nome')
    serializer_class = ProdutoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['codigo', 'nome', 'fabricante', 'codigo_fabricante']
    ordering_fields = ['nome', 'codigo', 'preco_venda', 'quantidade_estoque', 'criado_em']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['categoria', 'status', 'ativo']
    
    @action(detail=False, methods=['get'])
    def estoque_baixo(self, request):
        """Lista produtos com estoque abaixo do mínimo"""
        produtos_baixo = [p for p in self.get_queryset() if p.estoque_baixo()]
        serializer = self.get_serializer(produtos_baixo, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def ajustar_estoque(self, request, pk=None):
        """Ajusta o estoque de um produto"""
        produto = self.get_object()
        nova_quantidade = request.data.get('quantidade')
        motivo = request.data.get('motivo', 'Ajuste manual')
        
        if nova_quantidade is None:
            return Response(
                {'error': 'Quantidade é obrigatória'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            nova_quantidade = float(nova_quantidade)
        except ValueError:
            return Response(
                {'error': 'Quantidade inválida'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Criar movimentação
        MovimentacaoEstoqueLoja.objects.create(
            empresa=produto.empresa,
            produto=produto,
            tipo='AJUSTE',
            quantidade=nova_quantidade - produto.quantidade_estoque,
            quantidade_anterior=produto.quantidade_estoque,
            quantidade_nova=nova_quantidade,
            motivo=motivo
        )
        
        produto.quantidade_estoque = nova_quantidade
        produto.save()
        
        return Response(self.get_serializer(produto).data)
    
    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        fmt = request.query_params.get("format", "csv")
        qs = self.filter_queryset(self.get_queryset())
        fields = ['id', 'codigo', 'nome', 'preco_venda', 'quantidade_estoque', 'status']
        filename = f"produtos." + ("xlsx" if fmt == "xlsx" else "csv")
        if fmt == "xlsx":
            return export_xlsx(qs, fields, filename=filename)
        return export_csv_streaming(qs, fields, filename=filename) if request.query_params.get("stream") in {"1","true","True"} else export_csv(qs, fields, filename=filename)


class PedidoViewSet(AuditedModelViewSet):
    queryset = Pedido.objects.all().order_by('-data_pedido')
    serializer_class = PedidoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['numero_pedido', 'cliente_nome', 'cliente_documento']
    ordering_fields = ['data_pedido', 'valor_total', 'status']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['status', 'tipo']
    
    @action(detail=True, methods=['post'])
    def confirmar(self, request, pk=None):
        """Confirma um pedido"""
        pedido = self.get_object()
        
        if pedido.status != 'PENDENTE':
            return Response(
                {'error': 'Apenas pedidos pendentes podem ser confirmados'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        pedido.status = 'CONFIRMADO'
        from django.utils import timezone
        pedido.data_confirmacao = timezone.now()
        pedido.save()
        
        return Response(self.get_serializer(pedido).data)
    
    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        """Cancela um pedido"""
        pedido = self.get_object()
        motivo = request.data.get('motivo', 'Cancelamento solicitado')
        
        if pedido.status in ['ENTREGUE', 'CANCELADO']:
            return Response(
                {'error': 'Pedido não pode ser cancelado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        pedido.status = 'CANCELADO'
        pedido.observacoes_internas = f"{pedido.observacoes_internas or ''}\nCancelado: {motivo}"
        pedido.save()
        
        return Response(self.get_serializer(pedido).data)
    
    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        fmt = request.query_params.get("format", "csv")
        qs = self.filter_queryset(self.get_queryset())
        fields = ['id', 'numero_pedido', 'cliente_nome', 'valor_total', 'status', 'data_pedido']
        filename = f"pedidos." + ("xlsx" if fmt == "xlsx" else "csv")
        if fmt == "xlsx":
            return export_xlsx(qs, fields, filename=filename)
        return export_csv_streaming(qs, fields, filename=filename) if request.query_params.get("stream") in {"1","true","True"} else export_csv(qs, fields, filename=filename)


class ItemPedidoViewSet(AuditedModelViewSet):
    queryset = ItemPedido.objects.all()
    serializer_class = ItemPedidoSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['pedido', 'produto']


class MovimentacaoEstoqueLojaViewSet(AuditedModelViewSet):
    queryset = MovimentacaoEstoqueLoja.objects.all().order_by('-data_movimentacao')
    serializer_class = MovimentacaoEstoqueLojaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['produto__nome', 'produto__codigo', 'motivo']
    ordering_fields = ['data_movimentacao', 'quantidade']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['tipo', 'produto', 'pedido']
