from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from backend.common.permissions import OptionalRolePermission
from backend.common.audit import AuditedModelViewSet
from backend.common.export import export_csv, export_xlsx, export_csv_streaming
from .models import CategoriaCusto, Custo, CustoPorKm
from .serializers import CategoriaCustoSerializer, CustoSerializer, CustoPorKmSerializer


class CategoriaCustoViewSet(AuditedModelViewSet):
    queryset = CategoriaCusto.objects.all().order_by('nome')
    serializer_class = CategoriaCustoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome']
    ordering_fields = ['nome', 'tipo']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['tipo', 'ativo']


class CustoViewSet(AuditedModelViewSet):
    queryset = Custo.objects.all().order_by('-data_custo')
    serializer_class = CustoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['descricao', 'fornecedor', 'numero_documento']
    ordering_fields = ['data_custo', 'valor', 'data_vencimento']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['categoria', 'veiculo', 'status']
    
    @action(detail=False, methods=['get'])
    def vencidos(self, request):
        """Lista custos vencidos"""
        custos_vencidos = [c for c in self.get_queryset() if c.esta_vencido()]
        serializer = self.get_serializer(custos_vencidos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def pagar(self, request, pk=None):
        """Marca custo como pago"""
        custo = self.get_object()
        data_pagamento = request.data.get('data_pagamento', timezone.now().date())
        
        custo.status = 'PAGO'
        custo.data_pagamento = data_pagamento
        custo.save()
        
        return Response(self.get_serializer(custo).data)
    
    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        fmt = request.query_params.get("format", "csv")
        qs = self.filter_queryset(self.get_queryset())
        fields = ['id', 'descricao', 'valor', 'data_custo', 'status']
        filename = f"custos." + ("xlsx" if fmt == "xlsx" else "csv")
        if fmt == "xlsx":
            return export_xlsx(qs, fields, filename=filename)
        return export_csv_streaming(qs, fields, filename=filename) if request.query_params.get("stream") in {"1","true","True"} else export_csv(qs, fields, filename=filename)


class CustoPorKmViewSet(AuditedModelViewSet):
    queryset = CustoPorKm.objects.all().order_by('-mes_referencia')
    serializer_class = CustoPorKmSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['veiculo', 'mes_referencia']
