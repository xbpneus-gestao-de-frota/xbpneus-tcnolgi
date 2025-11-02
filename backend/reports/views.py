
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from backend.core.permissions import IsTransportador
from django.db.models import Avg, Sum, Count
from backend.transportador.pneus.models import MedicaoPneu
from backend.transportador.manutencao.models import ItemOS
from backend.transportador.estoque.models import MovimentacaoEstoque


class CustosPorPosicao(APIView):
    """Custos por posição de pneu"""
    permission_classes = [IsAuthenticated, IsTransportador]
    def get(self, request):
        empresa_id = request.query_params.get("empresa_id") or getattr(request.user,"empresa_id",None)
        qs = ItemOS.objects.select_related("posicao", "os")
        if empresa_id:
            qs = qs.filter(os__empresa_id=empresa_id)
        data = (qs.values("posicao__veiculo__placa","posicao__eixo","posicao__posicao_tipo")
                  .annotate(total=Sum("custo_unitario"))
                  .order_by("posicao__veiculo__placa","posicao__eixo","posicao__posicao_tipo"))
        return Response(list(data))


class MedicoesPorPosicao(APIView):
    permission_classes = [IsAuthenticated, IsTransportador]
    def get(self, request):
        empresa_id = request.query_params.get("empresa_id") or getattr(request.user,"empresa_id",None)
        qs = MedicaoPneu.objects.all()
        if empresa_id: qs = qs.filter(pneu__empresa_id=empresa_id)
        data = qs.values("posicao_tipo").annotate(
            sulco_avg=Avg("profundidade_sulco_mm"),
            pressao_avg=Avg("pressao_psi")
        ).order_by("posicao_tipo")
        return Response(list(data))

class CustosPorOS(APIView):
    permission_classes = [IsAuthenticated, IsTransportador]
    def get(self, request):
        empresa_id = request.query_params.get("empresa_id") or getattr(request.user,"empresa_id",None)
        qs = ItemOS.objects.all()
        if empresa_id: qs = qs.filter(os__empresa_id=empresa_id)
        data = qs.values("os_id").annotate(total=Sum("custo_unitario")).order_by("-total")[:50]
        return Response(list(data))

class GiroEstoque(APIView):
    permission_classes = [IsAuthenticated, IsTransportador]
    def get(self, request):
        empresa_id = request.query_params.get("empresa_id") or getattr(request.user,"empresa_id",None)
        qs = MovimentacaoEstoque.objects.all()
        if empresa_id: qs = qs.filter(empresa_id=empresa_id)
        data = qs.values("tipo").annotate(qtd=Count("id")).order_by("-qtd")
        return Response(list(data))
