from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.common.permissions import OptionalRolePermission
from backend.common.audit import AuditedModelViewSet
from backend.common.export import export_csv, export_xlsx, export_csv_streaming
from .models import Fatura, ItemFatura, NotaFiscal
from .serializers import FaturaSerializer, ItemFaturaSerializer, NotaFiscalSerializer

class FaturaViewSet(AuditedModelViewSet):
    queryset = Fatura.objects.all().order_by('-data_emissao')
    serializer_class = FaturaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['numero_fatura', 'cliente__nome_razao_social']
    ordering_fields = ['data_emissao', 'data_vencimento', 'valor_liquido']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['cliente', 'viagem', 'status']
    
    @action(detail=False, methods=['get'])
    def vencidas(self, request):
        faturas = [f for f in self.get_queryset() if f.esta_vencida()]
        return Response(self.get_serializer(faturas, many=True).data)
    
    @action(detail=True, methods=['post'])
    def pagar(self, request, pk=None):
        fatura = self.get_object()
        fatura.status = 'PAGA'
        fatura.data_pagamento = request.data.get('data_pagamento', timezone.now().date())
        fatura.save()
        return Response(self.get_serializer(fatura).data)
    
    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        fmt = request.query_params.get("format", "csv")
        qs = self.filter_queryset(self.get_queryset())
        fields = ['id', 'numero_fatura', 'cliente__nome_razao_social', 'data_emissao', 'data_vencimento', 'valor_liquido', 'status']
        filename = f"faturas." + ("xlsx" if fmt == "xlsx" else "csv")
        if fmt == "xlsx":
            return export_xlsx(qs, fields, filename=filename)
        return export_csv_streaming(qs, fields, filename=filename) if request.query_params.get("stream") in {"1","true","True"} else export_csv(qs, fields, filename=filename)

class ItemFaturaViewSet(AuditedModelViewSet):
    queryset = ItemFatura.objects.all().order_by('-criado_em')
    serializer_class = ItemFaturaSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['fatura']

class NotaFiscalViewSet(AuditedModelViewSet):
    queryset = NotaFiscal.objects.all().order_by('-data_emissao')
    serializer_class = NotaFiscalSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['numero', 'serie', 'chave_acesso']
    ordering_fields = ['data_emissao', 'numero']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['fatura', 'tipo', 'status']
