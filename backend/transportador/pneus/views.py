from django.utils import timezone
from rest_framework import viewsets, permissions, filters
from backend.common.permissions import OptionalRolePermission
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.common.audit import AuditedModelViewSet
from backend.common.export import export_csv, export_xlsx, export_csv_streaming
from .models import Tire, Application
import logging
from .serializers import TireSerializer, ApplicationSerializer

logger = logging.getLogger(__name__)
class TireViewSet(AuditedModelViewSet):
    def create(self, request, *args, **kwargs):
        logger.info(f"[DEBUG] Chegou no TireViewSet.create. Método: {request.method}")
        logger.info(f"[DEBUG] Usuário: {request.user}")
        logger.info(f"[DEBUG] Dados da Requisição: {request.data}")

        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"[DEBUG] Erro ao criar pneu: {e}", exc_info=True)
            raise

    queryset = Tire.objects.all().order_by("id")
    serializer_class = TireSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']
    permission_classes = [permissions.IsAuthenticated, OptionalRolePermission]

    @action(detail=True, methods=["post"], url_path="aplicar")
    def aplicar(self, request, pk=None):
        """Aplica/monta um pneu em uma posição do veículo"""
        pneu = self.get_object()
        posicao = request.data.get('posicao')
        placa = request.data.get('placa')
        
        if not posicao or not placa:
            return Response({"error": "Posição e placa são obrigatórios"}, status=400)
        
        pneu.status = 'MONTADO'
        pneu.posicao_atual = f"{placa}-{posicao}"
        pneu.data_montagem = timezone.now().date()
        pneu.save()
        
        # Registrar movimentação
        from .models import MovimentacaoPneu
        MovimentacaoPneu.objects.create(
            pneu=pneu,
            tipo='MONTAGEM',
            destino=pneu.posicao_atual,
            km_pneu=pneu.km_atual,
            observacoes=f"Montado na posição {posicao} do veículo {placa}"
        )
        
        return Response(self.get_serializer(pneu).data)
    
    @action(detail=True, methods=["post"], url_path="remover")
    def remover(self, request, pk=None):
        """Remove/desmonta um pneu de uma posição do veículo"""
        pneu = self.get_object()
        motivo = request.data.get('motivo', 'Desmontagem')
        
        origem = pneu.posicao_atual
        pneu.status = 'ESTOQUE'
        pneu.posicao_atual = ''
        pneu.data_desmontagem = timezone.now().date()
        pneu.save()
        
        # Registrar movimentação
        from .models import MovimentacaoPneu
        MovimentacaoPneu.objects.create(
            pneu=pneu,
            tipo='DESMONTAGEM',
            origem=origem,
            destino='ESTOQUE',
            km_pneu=pneu.km_atual,
            motivo=motivo,
            observacoes=f"Desmontado da posição {origem}"
        )
        
        return Response(self.get_serializer(pneu).data)

class ApplicationViewSet(AuditedModelViewSet):
    queryset = Application.objects.all().order_by("id")
    serializer_class = ApplicationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']
    permission_classes = [permissions.IsAuthenticated, OptionalRolePermission]
    filterset_fields = ['medida','status','posicao_atual']

    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        fmt = request.query_params.get("format", "csv")
        qs = self.filter_queryset(self.get_queryset())
        fields = ['id', 'codigo', 'medida', 'dot', 'status', 'posicao_atual']
        filename = f"tireviewset." + ("xlsx" if fmt == "xlsx" else "csv")
        if fmt == "xlsx":
            return export_xlsx(qs, fields, filename=filename)
        return export_csv_streaming(qs, fields, filename=filename) if request.query_params.get("stream") in {"1","true","True"} else export_csv(qs, fields, filename=filename)
