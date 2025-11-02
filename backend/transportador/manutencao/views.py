"""
Views completas para o módulo de Manutenção
Sistema XBPneus - Gestão de Frotas de Transporte
Expandido para 100% de completude
"""

from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta

try:
    from backend.common.permissions import OptionalRolePermission
    from backend.common.audit import AuditedModelViewSet
    from backend.common.export import export_csv, export_xlsx, export_csv_streaming
    HAS_COMMON = True
except ImportError:
    HAS_COMMON = False
    AuditedModelViewSet = viewsets.ModelViewSet

from .models import (
    OrdemServico, ItemOS, ChecklistManutencao,
    PlanoManutencaoPreventiva, HistoricoManutencao,
    WorkOrder, Teste
)
from .serializers import (
    OrdemServicoSerializer, ItemOSSerializer, ChecklistManutencaoSerializer,
    PlanoManutencaoPreventivaSerializer, HistoricoManutencaoSerializer,
    WorkOrderSerializer, TesteSerializer
)


class OrdemServicoViewSet(viewsets.ModelViewSet):
    """ViewSet para Ordem de Serviço"""
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrdemServicoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['veiculo', 'tipo', 'status', 'prioridade']
    search_fields = ['numero', 'descricao_problema', 'veiculo__placa']
    ordering_fields = ['data_abertura', 'data_agendamento', 'prioridade', 'custo_total']
    ordering = ['-data_abertura']
    
    def get_queryset(self):
        return OrdemServico.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(aberta_por=self.request.user)
    
    @action(detail=False, methods=['get'])
    def abertas(self, request):
        """Retorna OSs abertas"""
        queryset = self.get_queryset().filter(status__in=['ABERTA', 'AGENDADA', 'EM_ANDAMENTO'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def atrasadas(self, request):
        """Retorna OSs atrasadas"""
        queryset = self.get_queryset().filter(
            data_agendamento__lt=timezone.now(),
            status__in=['ABERTA', 'AGENDADA', 'EM_ANDAMENTO']
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Retorna estatísticas de OSs"""
        queryset = self.get_queryset()
        
        # Filtrar por período
        periodo = request.query_params.get('periodo', '30')  # dias
        data_inicio = timezone.now() - timedelta(days=int(periodo))
        queryset_periodo = queryset.filter(data_abertura__gte=data_inicio)
        
        stats = {
            'total': queryset.count(),
            'abertas': queryset.filter(status='ABERTA').count(),
            'em_andamento': queryset.filter(status='EM_ANDAMENTO').count(),
            'concluidas': queryset.filter(status='CONCLUIDA').count(),
            'atrasadas': queryset.filter(
                data_agendamento__lt=timezone.now(),
                status__in=['ABERTA', 'AGENDADA', 'EM_ANDAMENTO']
            ).count(),
            'custo_total_periodo': queryset_periodo.aggregate(
                total=Sum('custo_total')
            )['total'] or 0,
            'por_tipo': {},
            'por_prioridade': {}
        }
        
        # Por tipo
        for tipo in queryset_periodo.values('tipo').annotate(total=Count('id')):
            stats['por_tipo'][tipo['tipo']] = tipo['total']
        
        # Por prioridade
        for prio in queryset_periodo.values('prioridade').annotate(total=Count('id')):
            stats['por_prioridade'][prio['prioridade']] = prio['total']
        
        return Response(stats)
    
    @action(detail=True, methods=['post'])
    def iniciar(self, request, pk=None):
        """Inicia uma OS"""
        os = self.get_object()
        
        if os.status not in ['ABERTA', 'AGENDADA']:
            return Response(
                {'erro': 'OS não pode ser iniciada neste status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        os.status = 'EM_ANDAMENTO'
        os.data_inicio = timezone.now()
        os.mecanico = request.user
        os.save()
        
        serializer = self.get_serializer(os)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def concluir(self, request, pk=None):
        """Conclui uma OS"""
        os = self.get_object()
        
        if os.status != 'EM_ANDAMENTO':
            return Response(
                {'erro': 'OS não está em andamento'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        os.status = 'CONCLUIDA'
        os.data_conclusao = timezone.now()
        os.descricao_servico = request.data.get('descricao_servico', os.descricao_servico)
        os.km_conclusao = request.data.get('km_conclusao', os.km_conclusao)
        os.save()
        
        # Criar histórico
        HistoricoManutencao.objects.create(
            veiculo=os.veiculo,
            os=os,
            data=os.data_conclusao,
            tipo=os.tipo,
            descricao=os.descricao_servico or os.descricao_problema,
            km=os.km_conclusao,
            custo=os.custo_total
        )
        
        serializer = self.get_serializer(os)
        return Response(serializer.data)


class ItemOSViewSet(viewsets.ModelViewSet):
    """ViewSet para Item da OS"""
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ItemOSSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['os', 'tipo', 'aplicado']
    search_fields = ['codigo', 'descricao']
    
    def get_queryset(self):
        return ItemOS.objects.all()


class ChecklistManutencaoViewSet(viewsets.ModelViewSet):
    """ViewSet para Checklist de Manutenção"""
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChecklistManutencaoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['os']
    
    def get_queryset(self):
        return ChecklistManutencao.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(realizado_por=self.request.user)


class PlanoManutencaoPreventivaViewSet(viewsets.ModelViewSet):
    """ViewSet para Plano de Manutenção Preventiva"""
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PlanoManutencaoPreventivaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['veiculo', 'ativo']
    search_fields = ['nome', 'descricao']
    
    def get_queryset(self):
        return PlanoManutencaoPreventiva.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)
    
    @action(detail=False, methods=['get'])
    def vencidos(self, request):
        """Retorna planos com manutenção vencida"""
        queryset = self.get_queryset().filter(
            ativo=True,
            proxima_manutencao_data__lt=timezone.now().date()
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class HistoricoManutencaoViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para Histórico de Manutenção"""
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HistoricoManutencaoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['veiculo', 'tipo']
    ordering_fields = ['data', 'km', 'custo']
    ordering = ['-data']
    
    def get_queryset(self):
        return HistoricoManutencao.objects.all()


# ViewSets legados (para compatibilidade)
class WorkOrderViewSet(AuditedModelViewSet):
    """ViewSet para Work Order (legado)"""
    
    queryset = WorkOrder.objects.all().order_by("id")
    serializer_class = WorkOrderSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']
    
    if HAS_COMMON:
        permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    else:
        permission_classes = [permissions.IsAuthenticated]


class TesteViewSet(AuditedModelViewSet):
    """ViewSet para Teste (legado)"""
    
    queryset = Teste.objects.all().order_by("id")
    serializer_class = TesteSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']
    filterset_fields = ['os_id']
    
    if HAS_COMMON:
        permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    else:
        permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        """Exporta dados (requer backend.common)"""
        if not HAS_COMMON:
            return Response(
                {'erro': 'Funcionalidade de exportação não disponível'},
                status=status.HTTP_501_NOT_IMPLEMENTED
            )
        
        fmt = request.query_params.get("format", "csv")
        qs = self.filter_queryset(self.get_queryset())
        fields = ['id', 'os_id', 'torque_ok', 'pressao_ok', 'rodagem_ok', 'data']
        filename = f"testes." + ("xlsx" if fmt == "xlsx" else "csv")
        
        if fmt == "xlsx":
            return export_xlsx(qs, fields, filename=filename)
        
        if request.query_params.get("stream") in {"1","true","True"}:
            return export_csv_streaming(qs, fields, filename=filename)
        
        return export_csv(qs, fields, filename=filename)
