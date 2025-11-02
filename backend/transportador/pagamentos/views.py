from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.common.permissions import OptionalRolePermission
from backend.common.audit import AuditedModelViewSet
from backend.common.export import export_csv, export_xlsx, export_csv_streaming
from .models import ContaPagar, ContaReceber, Pagamento
from .serializers import ContaPagarSerializer, ContaReceberSerializer, PagamentoSerializer

class ContaPagarViewSet(AuditedModelViewSet):
    queryset = ContaPagar.objects.all().order_by('data_vencimento')
    serializer_class = ContaPagarSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['numero_documento', 'descricao', 'fornecedor__nome_razao_social']
    ordering_fields = ['data_vencimento', 'valor_original']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['fornecedor', 'tipo', 'status']
    
    @action(detail=False, methods=['get'])
    def vencidas(self, request):
        contas = [c for c in self.get_queryset() if c.esta_vencida()]
        return Response(self.get_serializer(contas, many=True).data)
    
    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        fmt = request.query_params.get("format", "csv")
        qs = self.filter_queryset(self.get_queryset())
        fields = ['id', 'numero_documento', 'descricao', 'data_vencimento', 'valor_original', 'status']
        filename = f"contas_pagar." + ("xlsx" if fmt == "xlsx" else "csv")
        if fmt == "xlsx":
            return export_xlsx(qs, fields, filename=filename)
        return export_csv_streaming(qs, fields, filename=filename) if request.query_params.get("stream") in {"1","true","True"} else export_csv(qs, fields, filename=filename)

class ContaReceberViewSet(AuditedModelViewSet):
    queryset = ContaReceber.objects.all().order_by('data_vencimento')
    serializer_class = ContaReceberSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['numero_documento', 'descricao', 'cliente__nome_razao_social']
    ordering_fields = ['data_vencimento', 'valor_original']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['cliente', 'status']
    
    @action(detail=False, methods=['get'])
    def vencidas(self, request):
        contas = [c for c in self.get_queryset() if c.esta_vencida()]
        return Response(self.get_serializer(contas, many=True).data)
    
    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        fmt = request.query_params.get("format", "csv")
        qs = self.filter_queryset(self.get_queryset())
        fields = ['id', 'numero_documento', 'descricao', 'data_vencimento', 'valor_original', 'status']
        filename = f"contas_receber." + ("xlsx" if fmt == "xlsx" else "csv")
        if fmt == "xlsx":
            return export_xlsx(qs, fields, filename=filename)
        return export_csv_streaming(qs, fields, filename=filename) if request.query_params.get("stream") in {"1","true","True"} else export_csv(qs, fields, filename=filename)

class PagamentoViewSet(AuditedModelViewSet):
    queryset = Pagamento.objects.all().order_by('-data_pagamento')
    serializer_class = PagamentoSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['conta_pagar', 'conta_receber', 'forma_pagamento']
