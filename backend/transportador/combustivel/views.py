from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.common.permissions import OptionalRolePermission
from backend.common.audit import AuditedModelViewSet
from backend.common.export import export_csv, export_xlsx, export_csv_streaming
from .models import PostoCombustivel, Abastecimento, ConsumoMensal
from .serializers import PostoCombustivelSerializer, AbastecimentoSerializer, ConsumoMensalSerializer


class PostoCombustivelViewSet(AuditedModelViewSet):
    queryset = PostoCombustivel.objects.all().order_by('nome')
    serializer_class = PostoCombustivelSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'cnpj', 'cidade']
    ordering_fields = ['nome', 'cidade']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['ativo', 'estado']


class AbastecimentoViewSet(AuditedModelViewSet):
    queryset = Abastecimento.objects.all().order_by('-data_abastecimento')
    serializer_class = AbastecimentoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['veiculo__placa', 'posto__nome', 'numero_nota']
    ordering_fields = ['data_abastecimento', 'valor_total', 'litros']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['veiculo', 'posto', 'tipo_combustivel', 'forma_pagamento']
    
    @action(detail=False, methods=['get'])
    def consumo_baixo(self, request):
        """Lista abastecimentos com consumo abaixo de 2 km/l"""
        abastecimentos = self.get_queryset().filter(consumo_medio__lt=2, consumo_medio__isnull=False)
        serializer = self.get_serializer(abastecimentos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        fmt = request.query_params.get("format", "csv")
        qs = self.filter_queryset(self.get_queryset())
        fields = ['id', 'data_abastecimento', 'veiculo__placa', 'litros', 'valor_total', 'consumo_medio']
        filename = f"abastecimentos." + ("xlsx" if fmt == "xlsx" else "csv")
        if fmt == "xlsx":
            return export_xlsx(qs, fields, filename=filename)
        return export_csv_streaming(qs, fields, filename=filename) if request.query_params.get("stream") in {"1","true","True"} else export_csv(qs, fields, filename=filename)


class ConsumoMensalViewSet(AuditedModelViewSet):
    queryset = ConsumoMensal.objects.all().order_by('-mes_referencia')
    serializer_class = ConsumoMensalSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['veiculo', 'mes_referencia']
