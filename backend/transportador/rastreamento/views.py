from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.common.permissions import OptionalRolePermission
from backend.common.audit import AuditedModelViewSet
from .models import Posicao, CercaEletronica, ViolacaoCerca, HistoricoRastreamento
from .serializers import PosicaoSerializer, CercaEletronicaSerializer, ViolacaoCercaSerializer, HistoricoRastreamentoSerializer

class PosicaoViewSet(AuditedModelViewSet):
    queryset = Posicao.objects.all().order_by('-data_hora')
    serializer_class = PosicaoSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['veiculo']
    
    @action(detail=False, methods=['get'])
    def ultima_por_veiculo(self, request):
        from django.db.models import Max
        ultimas = Posicao.objects.values('veiculo').annotate(ultima=Max('data_hora'))
        posicoes = []
        for u in ultimas:
            pos = Posicao.objects.filter(veiculo=u['veiculo'], data_hora=u['ultima']).first()
            if pos:
                posicoes.append(pos)
        return Response(self.get_serializer(posicoes, many=True).data)

class CercaEletronicaViewSet(AuditedModelViewSet):
    queryset = CercaEletronica.objects.all().order_by('nome')
    serializer_class = CercaEletronicaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['tipo', 'ativa']

class ViolacaoCercaViewSet(AuditedModelViewSet):
    queryset = ViolacaoCerca.objects.all().order_by('-data_hora')
    serializer_class = ViolacaoCercaSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['cerca', 'veiculo', 'tipo', 'status']
    
    @action(detail=False, methods=['get'])
    def abertas(self, request):
        violacoes = self.get_queryset().filter(status='ABERTO')
        return Response(self.get_serializer(violacoes, many=True).data)

class HistoricoRastreamentoViewSet(AuditedModelViewSet):
    queryset = HistoricoRastreamento.objects.all().order_by('-data')
    serializer_class = HistoricoRastreamentoSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['veiculo', 'data']
