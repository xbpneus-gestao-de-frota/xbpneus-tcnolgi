from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.common.permissions import OptionalRolePermission
from backend.common.audit import AuditedModelViewSet
from backend.common.export import export_csv, export_xlsx, export_csv_streaming
from .models import Viagem, Carga, Parada
from .serializers import ViagemSerializer, CargaSerializer, ParadaSerializer


class ViagemViewSet(AuditedModelViewSet):
    queryset = Viagem.objects.all().order_by('-data_saida_prevista')
    serializer_class = ViagemSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['numero_viagem', 'origem', 'destino', 'motorista_nome']
    ordering_fields = ['data_saida_prevista', 'valor_frete']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['veiculo', 'status']
    
    @action(detail=True, methods=['post'])
    def iniciar(self, request, pk=None):
        """Inicia viagem"""
        viagem = self.get_object()
        viagem.status = 'EM_ANDAMENTO'
        viagem.data_saida_real = request.data.get('data_saida_real', timezone.now())
        viagem.save()
        return Response(self.get_serializer(viagem).data)
    
    @action(detail=True, methods=['post'])
    def finalizar(self, request, pk=None):
        """Finaliza viagem"""
        viagem = self.get_object()
        viagem.status = 'CONCLUIDA'
        viagem.data_chegada_real = request.data.get('data_chegada_real', timezone.now())
        viagem.km_final = request.data.get('km_final')
        viagem.calcular_km()
        viagem.save()
        return Response(self.get_serializer(viagem).data)
    
    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        fmt = request.query_params.get("format", "csv")
        qs = self.filter_queryset(self.get_queryset())
        fields = ['id', 'numero_viagem', 'origem', 'destino', 'status', 'valor_frete']
        filename = f"viagens." + ("xlsx" if fmt == "xlsx" else "csv")
        if fmt == "xlsx":
            return export_xlsx(qs, fields, filename=filename)
        return export_csv_streaming(qs, fields, filename=filename) if request.query_params.get("stream") in {"1","true","True"} else export_csv(qs, fields, filename=filename)


class CargaViewSet(AuditedModelViewSet):
    queryset = Carga.objects.all().order_by('-criado_em')
    serializer_class = CargaSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['viagem']


class ParadaViewSet(AuditedModelViewSet):
    queryset = Parada.objects.all().order_by('-data_hora_entrada')
    serializer_class = ParadaSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['viagem', 'tipo']
