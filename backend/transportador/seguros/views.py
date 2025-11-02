from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.common.permissions import OptionalRolePermission
from backend.common.audit import AuditedModelViewSet
from backend.common.export import export_csv, export_xlsx, export_csv_streaming
from .models import Seguradora, Apolice, Sinistro
from .serializers import SeguradoraSerializer, ApoliceSerializer, SinistroSerializer


class SeguradoraViewSet(AuditedModelViewSet):
    queryset = Seguradora.objects.all().order_by('nome')
    serializer_class = SeguradoraSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'cnpj']
    ordering_fields = ['nome']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['ativo']


class ApoliceViewSet(AuditedModelViewSet):
    queryset = Apolice.objects.all().order_by('-data_inicio')
    serializer_class = ApoliceSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['numero_apolice', 'veiculo__placa']
    ordering_fields = ['data_inicio', 'data_fim', 'valor_premio']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['seguradora', 'veiculo', 'tipo', 'status']
    
    @action(detail=False, methods=['get'])
    def vencidas(self, request):
        apolices = [a for a in self.get_queryset() if a.esta_vencida()]
        return Response(self.get_serializer(apolices, many=True).data)
    
    @action(detail=False, methods=['get'])
    def vencendo(self, request):
        apolices = [a for a in self.get_queryset() if a.esta_vencendo()]
        return Response(self.get_serializer(apolices, many=True).data)
    
    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        fmt = request.query_params.get("format", "csv")
        qs = self.filter_queryset(self.get_queryset())
        fields = ['id', 'numero_apolice', 'tipo', 'data_inicio', 'data_fim', 'valor_premio', 'status']
        filename = f"apolices." + ("xlsx" if fmt == "xlsx" else "csv")
        if fmt == "xlsx":
            return export_xlsx(qs, fields, filename=filename)
        return export_csv_streaming(qs, fields, filename=filename) if request.query_params.get("stream") in {"1","true","True"} else export_csv(qs, fields, filename=filename)


class SinistroViewSet(AuditedModelViewSet):
    queryset = Sinistro.objects.all().order_by('-data_ocorrencia')
    serializer_class = SinistroSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['numero_sinistro', 'local_ocorrencia']
    ordering_fields = ['data_ocorrencia', 'valor_estimado']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['apolice', 'tipo', 'status']
