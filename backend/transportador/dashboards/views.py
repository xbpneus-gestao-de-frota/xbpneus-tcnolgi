from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Sum, Avg
from backend.common.permissions import OptionalRolePermission
from backend.common.audit import AuditedModelViewSet
from .models import Dashboard, Widget, KPI
from .serializers import DashboardSerializer, WidgetSerializer, KPISerializer

class DashboardViewSet(AuditedModelViewSet):
    queryset = Dashboard.objects.all().order_by('nome')
    serializer_class = DashboardSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['padrao', 'ativo']
    
    @action(detail=False, methods=['get'])
    def padrao(self, request):
        dashboard = self.get_queryset().filter(padrao=True).first()
        if dashboard:
            return Response(self.get_serializer(dashboard).data)
        return Response({'error': 'Nenhum dashboard padrão configurado'}, status=404)

class WidgetViewSet(AuditedModelViewSet):
    queryset = Widget.objects.all().order_by('dashboard', 'posicao_y', 'posicao_x')
    serializer_class = WidgetSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['dashboard', 'tipo', 'ativo']

class KPIViewSet(AuditedModelViewSet):
    queryset = KPI.objects.all().order_by('categoria', 'nome')
    serializer_class = KPISerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome']
    ordering_fields = ['nome', 'valor_atual', 'data_referencia']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['categoria']
    
    @action(detail=False, methods=['get'])
    def resumo(self, request):
        kpis = self.get_queryset()
        resumo = {
            'total': kpis.count(),
            'por_categoria': {}
        }
        for categoria, nome in KPI.CATEGORIA_CHOICES:
            kpis_categoria = kpis.filter(categoria=categoria)
            resumo['por_categoria'][categoria] = {
                'nome': nome,
                'total': kpis_categoria.count(),
                'kpis': self.get_serializer(kpis_categoria, many=True).data
            }
        return Response(resumo)
