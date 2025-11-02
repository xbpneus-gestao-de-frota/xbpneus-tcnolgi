from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.common.permissions import OptionalRolePermission
from backend.common.audit import AuditedModelViewSet
from .models import Dispositivo, Leitura, Alerta
from .serializers import DispositivoSerializer, LeituraSerializer, AlertaSerializer

class DispositivoViewSet(AuditedModelViewSet):
    queryset = Dispositivo.objects.all().order_by('veiculo', 'tipo')
    serializer_class = DispositivoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['numero_serie', 'veiculo__placa']
    ordering_fields = ['data_instalacao']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['veiculo', 'tipo', 'status']

class LeituraViewSet(AuditedModelViewSet):
    queryset = Leitura.objects.all().order_by('-data_hora')
    serializer_class = LeituraSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['dispositivo']
    
    @action(detail=False, methods=['get'])
    def ultimas(self, request):
        dispositivo_id = request.query_params.get('dispositivo')
        if dispositivo_id:
            leituras = self.get_queryset().filter(dispositivo_id=dispositivo_id)[:100]
        else:
            leituras = self.get_queryset()[:100]
        return Response(self.get_serializer(leituras, many=True).data)

class AlertaViewSet(AuditedModelViewSet):
    queryset = Alerta.objects.all().order_by('-data_hora')
    serializer_class = AlertaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['mensagem']
    ordering_fields = ['data_hora', 'severidade']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['dispositivo', 'tipo', 'severidade', 'status']
    
    @action(detail=False, methods=['get'])
    def abertos(self, request):
        alertas = self.get_queryset().filter(status='ABERTO')
        return Response(self.get_serializer(alertas, many=True).data)
    
    @action(detail=True, methods=['post'])
    def reconhecer(self, request, pk=None):
        alerta = self.get_object()
        alerta.status = 'RECONHECIDO'
        alerta.data_reconhecimento = timezone.now()
        alerta.save()
        return Response(self.get_serializer(alerta).data)
