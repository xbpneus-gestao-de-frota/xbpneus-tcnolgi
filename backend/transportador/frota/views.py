from rest_framework import viewsets, permissions, filters
from backend.common.permissions import OptionalRolePermission
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.common.audit import AuditedModelViewSet
from backend.common.export import export_csv, export_xlsx, export_csv_streaming
from .models import Vehicle, Position
from .serializers import VehicleSerializer, PositionSerializer

class VehicleViewSet(AuditedModelViewSet):
    queryset = Vehicle.objects.select_related(
        'empresa', 'filial', 'modelo_veiculo', 'configuracao_operacional'
    ).all().order_by("id")
    serializer_class = VehicleSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'id', 'placa', 'chassi',
        'modelo_veiculo__familia_modelo', 'modelo_veiculo__marca',
        'configuracao_operacional__op_code'
    ]
    ordering_fields = [
        'id', 'placa', 'km',
        'modelo_veiculo__familia_modelo', 'modelo_veiculo__marca',
        'configuracao_operacional__op_code'
    ]
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = [
        'placa', 'motorista', 'empresa', 'filial', 'tipo', 'status',
        'modelo_veiculo__marca', 'modelo_veiculo__familia_modelo',
        'configuracao_operacional__op_code'
    ]

    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        fmt = request.query_params.get("format", "csv")
        qs = self.filter_queryset(self.get_queryset())
        fields = [
            'id', 'placa', 'modelo_veiculo__familia_modelo', 'modelo_veiculo__marca',
            'km', 'motorista', 'configuracao_operacional__op_code'
        ]
        filename = f"vehicleviewset." + ("xlsx" if fmt == "xlsx" else "csv")
        if fmt == "xlsx":
            return export_xlsx(qs, fields, filename=filename)
        return export_csv_streaming(qs, fields, filename=filename) if request.query_params.get("stream") in {"1","true","True"} else export_csv(qs, fields, filename=filename)

class PositionViewSet(AuditedModelViewSet):
    queryset = Position.objects.select_related(
        'veiculo', 'mapa_posicao', 'medida_recomendada'
    ).all().order_by("id")
    serializer_class = PositionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'id', 'veiculo__placa',
        'mapa_posicao__position_id', 'medida_recomendada__medidas_tipicas'
    ]
    ordering_fields = [
        'id', 'ordem',
        'mapa_posicao__position_id', 'medida_recomendada__medidas_tipicas'
    ]
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = [
        'veiculo', 'mapa_posicao__config_id', 'mapa_posicao__posicao_tipo',
        'medida_recomendada__medidas_tipicas'
    ]

