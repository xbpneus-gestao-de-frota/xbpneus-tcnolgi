from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.common.permissions import OptionalRolePermission
from backend.common.audit import AuditedModelViewSet
from backend.common.export import export_csv, export_xlsx, export_csv_streaming
from .models import Multa, RecursoMulta, PontuacaoCNH
from .serializers import MultaSerializer, RecursoMultaSerializer, PontuacaoCNHSerializer


class MultaViewSet(AuditedModelViewSet):
    queryset = Multa.objects.all().order_by('-data_infracao')
    serializer_class = MultaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['numero_auto', 'veiculo__placa', 'motorista_nome']
    ordering_fields = ['data_infracao', 'valor', 'data_vencimento']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['veiculo', 'gravidade', 'status']
    
    @action(detail=False, methods=['get'])
    def vencidas(self, request):
        """Lista multas vencidas"""
        multas_vencidas = [m for m in self.get_queryset() if m.esta_vencida()]
        serializer = self.get_serializer(multas_vencidas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def pagar(self, request, pk=None):
        """Registra pagamento de multa"""
        multa = self.get_object()
        valor_pago = request.data.get('valor_pago', multa.valor_com_desconto())
        data_pagamento = request.data.get('data_pagamento')
        
        multa.valor_pago = valor_pago
        multa.data_pagamento = data_pagamento
        multa.status = 'PAGA'
        multa.save()
        
        return Response(self.get_serializer(multa).data)
    
    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        fmt = request.query_params.get("format", "csv")
        qs = self.filter_queryset(self.get_queryset())
        fields = ['id', 'numero_auto', 'veiculo__placa', 'data_infracao', 'valor', 'status']
        filename = f"multas." + ("xlsx" if fmt == "xlsx" else "csv")
        if fmt == "xlsx":
            return export_xlsx(qs, fields, filename=filename)
        return export_csv_streaming(qs, fields, filename=filename) if request.query_params.get("stream") in {"1","true","True"} else export_csv(qs, fields, filename=filename)


class RecursoMultaViewSet(AuditedModelViewSet):
    queryset = RecursoMulta.objects.all().order_by('-data_recurso')
    serializer_class = RecursoMultaSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['multa', 'status']


class PontuacaoCNHViewSet(AuditedModelViewSet):
    queryset = PontuacaoCNH.objects.all().order_by('-pontos_atuais')
    serializer_class = PontuacaoCNHSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['motorista_nome', 'motorista_cnh']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    
    @action(detail=False, methods=['get'])
    def em_risco(self, request):
        """Lista motoristas em risco de suspensão"""
        em_risco = [p for p in self.get_queryset() if p.em_risco()]
        serializer = self.get_serializer(em_risco, many=True)
        return Response(serializer.data)
