from django.db.models import (
    Avg,
    Count,
    ExpressionWrapper,
    F,
    IntegerField,
    Max,
    Min,
    Sum,
)
from rest_framework import filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from backend.common.audit import AuditedModelViewSet
from backend.common.export import export_csv, export_csv_streaming, export_xlsx

from .models import Position, Vehicle
from .serializers import PositionSerializer, VehicleSerializer


def _build_fleet_metrics(queryset):
    km_stats = queryset.aggregate(
        total_veiculos=Count("id"),
        km_total=Sum("km"),
        km_medio=Avg("km"),
        km_maximo=Max("km"),
        km_minimo=Min("km"),
    )

    total_veiculos = km_stats.get("total_veiculos") or 0

    status_counts = {
        entry["status"]: entry["total"]
        for entry in queryset.values("status").annotate(total=Count("id")).order_by("status")
    }
    tipo_counts = {
        entry["tipo"]: entry["total"]
        for entry in queryset.values("tipo").annotate(total=Count("id")).order_by("tipo")
    }

    due_for_maintenance = queryset.filter(
        km_proxima_manutencao__isnull=False,
        km__gte=F("km_proxima_manutencao"),
    ).count()

    without_schedule = queryset.filter(km_proxima_manutencao__isnull=True).count()

    km_restante_expr = ExpressionWrapper(
        F("km_proxima_manutencao") - F("km"),
        output_field=IntegerField(),
    )
    upcoming_queryset = (
        queryset.filter(
            km_proxima_manutencao__isnull=False,
            km__lt=F("km_proxima_manutencao"),
        )
        .annotate(km_restante=km_restante_expr)
        .filter(km_restante__lte=500, km_restante__gte=0)
        .order_by("km_restante")[:5]
    )

    proximas_manutencoes = [
        {
            "id": veiculo.id,
            "placa": veiculo.placa,
            "km_atual": veiculo.km,
            "km_proxima_manutencao": veiculo.km_proxima_manutencao,
            "km_restante": max(0, veiculo.km_restante if veiculo.km_restante is not None else 0),
            "status": veiculo.status,
        }
        for veiculo in upcoming_queryset
    ]

    response_data = {
        "total_veiculos": total_veiculos,
        "por_status": status_counts,
        "por_tipo": tipo_counts,
        "km": {
            "total": float(km_stats.get("km_total") or 0),
            "media": float(km_stats.get("km_medio") or 0),
            "maximo": km_stats.get("km_maximo") or 0,
            "minimo": km_stats.get("km_minimo") or 0,
        },
        "manutencao": {
            "precisam_manutencao": due_for_maintenance,
            "sem_agendamento": without_schedule,
            "proximas_manutencoes": proximas_manutencoes,
        },
    }

    if total_veiculos:
        response_data["taxa_manutencao"] = round(due_for_maintenance / total_veiculos * 100, 2)
    else:
        response_data["taxa_manutencao"] = 0.0

    return response_data


class VehicleViewSet(AuditedModelViewSet):
    queryset = (
        Vehicle.objects.select_related(
            "empresa",
            "filial",
            "modelo_veiculo",
            "configuracao_operacional",
        )
        .all()
        .order_by("id")
    )
    serializer_class = VehicleSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "id",
        "placa",
        "chassi",
        "modelo_veiculo__familia_modelo",
        "modelo_veiculo__marca",
        "configuracao_operacional__op_code",
    ]
    ordering_fields = [
        "id",
        "placa",
        "km",
        "modelo_veiculo__familia_modelo",
        "modelo_veiculo__marca",
        "configuracao_operacional__op_code",
    ]
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = [
        "placa",
        "motorista",
        "empresa",
        "filial",
        "tipo",
        "status",
        "modelo_veiculo__marca",
        "modelo_veiculo__familia_modelo",
        "configuracao_operacional__op_code",
    ]

    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        fmt = request.query_params.get("format", "csv")
        qs = self.filter_queryset(self.get_queryset())
        fields = [
            "id",
            "placa",
            "modelo_veiculo__familia_modelo",
            "modelo_veiculo__marca",
            "km",
            "motorista",
            "configuracao_operacional__op_code",
        ]
        filename = f"vehicleviewset." + ("xlsx" if fmt == "xlsx" else "csv")
        if fmt == "xlsx":
            return export_xlsx(qs, fields, filename=filename)
        stream_flag = request.query_params.get("stream")
        if stream_flag in {"1", "true", "True"}:
            return export_csv_streaming(qs, fields, filename=filename)
        return export_csv(qs, fields, filename=filename)


class FleetAnalysisViewSet(GenericViewSet):
    """Endpoint dedicado à análise agregada da frota."""

    serializer_class = VehicleSerializer
    queryset = VehicleViewSet.queryset
    permission_classes = VehicleViewSet.permission_classes
    filter_backends = VehicleViewSet.filter_backends
    search_fields = VehicleViewSet.search_fields
    ordering_fields = VehicleViewSet.ordering_fields
    filterset_fields = VehicleViewSet.filterset_fields
    pagination_class = None
    http_method_names = ["get"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return Response(_build_fleet_metrics(queryset))


class PositionViewSet(AuditedModelViewSet):
    queryset = (
        Position.objects.select_related(
            "veiculo",
            "mapa_posicao",
            "medida_recomendada",
        )
        .all()
        .order_by("id")
    )
    serializer_class = PositionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "id",
        "veiculo__placa",
        "mapa_posicao__position_id",
        "medida_recomendada__medidas_tipicas",
    ]
    ordering_fields = [
        "id",
        "ordem",
        "mapa_posicao__position_id",
        "medida_recomendada__medidas_tipicas",
    ]
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = [
        "veiculo",
        "mapa_posicao__config_id",
        "mapa_posicao__posicao_tipo",
        "medida_recomendada__medidas_tipicas",
    ]

