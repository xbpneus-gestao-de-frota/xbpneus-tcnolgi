from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.common.permissions import OptionalRolePermission
from backend.common.audit import AuditedModelViewSet
from .models import Rota, PontoRota, RotaOtimizada
from .serializers import RotaSerializer, PontoRotaSerializer, RotaOtimizadaSerializer

class RotaViewSet(AuditedModelViewSet):
    queryset = Rota.objects.all().order_by('-data_inicio_prevista')
    serializer_class = RotaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'origem', 'destino']
    ordering_fields = ['data_inicio_prevista', 'distancia_km']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['veiculo', 'status']
    
    @action(detail=False, methods=['get'])
    def em_andamento(self, request):
        rotas = self.get_queryset().filter(status='EM_ANDAMENTO')
        return Response(self.get_serializer(rotas, many=True).data)
    
    @action(detail=True, methods=['post'])
    def iniciar(self, request, pk=None):
        rota = self.get_object()
        rota.status = 'EM_ANDAMENTO'
        rota.data_inicio_real = timezone.now()
        rota.save()
        return Response(self.get_serializer(rota).data)
    
    @action(detail=True, methods=['post'])
    def concluir(self, request, pk=None):
        rota = self.get_object()
        rota.status = 'CONCLUIDA'
        rota.data_fim_real = timezone.now()
        rota.save()
        return Response(self.get_serializer(rota).data)

class PontoRotaViewSet(AuditedModelViewSet):
    queryset = PontoRota.objects.all().order_by('rota', 'ordem')
    serializer_class = PontoRotaSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['rota', 'tipo']

class RotaOtimizadaViewSet(AuditedModelViewSet):
    queryset = RotaOtimizada.objects.all().order_by('-criado_em')
    serializer_class = RotaOtimizadaSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['rota_original']
