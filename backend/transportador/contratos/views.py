from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.common.permissions import OptionalRolePermission
from backend.common.audit import AuditedModelViewSet
from backend.common.export import export_csv, export_xlsx, export_csv_streaming
from .models import Contrato, Aditivo
from .serializers import ContratoSerializer, AditivoSerializer


class ContratoViewSet(AuditedModelViewSet):
    queryset = Contrato.objects.all().order_by('-data_inicio')
    serializer_class = ContratoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['numero_contrato', 'titulo']
    ordering_fields = ['data_inicio', 'data_fim', 'valor_total']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['cliente', 'fornecedor', 'tipo', 'status']
    
    @action(detail=False, methods=['get'])
    def vencidos(self, request):
        contratos = [c for c in self.get_queryset() if c.esta_vencido()]
        return Response(self.get_serializer(contratos, many=True).data)
    
    @action(detail=False, methods=['get'])
    def vencendo(self, request):
        contratos = [c for c in self.get_queryset() if c.esta_vencendo()]
        return Response(self.get_serializer(contratos, many=True).data)
    
    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        fmt = request.query_params.get("format", "csv")
        qs = self.filter_queryset(self.get_queryset())
        fields = ['id', 'numero_contrato', 'titulo', 'tipo', 'data_inicio', 'data_fim', 'valor_total', 'status']
        filename = f"contratos." + ("xlsx" if fmt == "xlsx" else "csv")
        if fmt == "xlsx":
            return export_xlsx(qs, fields, filename=filename)
        return export_csv_streaming(qs, fields, filename=filename) if request.query_params.get("stream") in {"1","true","True"} else export_csv(qs, fields, filename=filename)


class AditivoViewSet(AuditedModelViewSet):
    queryset = Aditivo.objects.all().order_by('-data_aditivo')
    serializer_class = AditivoSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['contrato']
