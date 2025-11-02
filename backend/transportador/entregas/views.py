from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.common.permissions import OptionalRolePermission
from backend.common.audit import AuditedModelViewSet
from .models import Entrega, POD, Ocorrencia, Tentativa
from .serializers import EntregaSerializer, PODSerializer, OcorrenciaSerializer, TentativaSerializer

class EntregaViewSet(AuditedModelViewSet):
    queryset = Entrega.objects.all().order_by('-data_prevista')
    serializer_class = EntregaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['numero_entrega', 'destinatario_nome', 'numero_nota_fiscal']
    ordering_fields = ['data_prevista', 'data_entrega']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['viagem', 'cliente', 'status']
    
    @action(detail=False, methods=['get'])
    def atrasadas(self, request):
        entregas = [e for e in self.get_queryset() if e.esta_atrasada()]
        return Response(self.get_serializer(entregas, many=True).data)
    
    @action(detail=False, methods=['get'])
    def pendentes(self, request):
        entregas = self.get_queryset().filter(status='PENDENTE')
        return Response(self.get_serializer(entregas, many=True).data)
    
    @action(detail=True, methods=['post'])
    def entregar(self, request, pk=None):
        entrega = self.get_object()
        entrega.status = 'ENTREGUE'
        entrega.data_entrega = timezone.now()
        entrega.save()
        return Response(self.get_serializer(entrega).data)

class PODViewSet(AuditedModelViewSet):
    queryset = POD.objects.all().order_by('-data_hora_recebimento')
    serializer_class = PODSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['entrega']

class OcorrenciaViewSet(AuditedModelViewSet):
    queryset = Ocorrencia.objects.all().order_by('-data_hora')
    serializer_class = OcorrenciaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['descricao']
    ordering_fields = ['data_hora']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['entrega', 'tipo']

class TentativaViewSet(AuditedModelViewSet):
    queryset = Tentativa.objects.all().order_by('entrega', 'numero_tentativa')
    serializer_class = TentativaSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['entrega', 'sucesso']
