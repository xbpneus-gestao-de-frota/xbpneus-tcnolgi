from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from backend.transportador.frota.models import Vehicle, Position
from backend.transportador.pneus.models import Tire, Application
from backend.transportador.estoque.models import StockMove
from backend.transportador.manutencao.models import WorkOrder, Teste

class MetricsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = {
            "vehicles": Vehicle.objects.count(),
            "positions": Position.objects.count(),
            "tires": Tire.objects.count(),
            "applications": Application.objects.count(),
            "stock_moves": StockMove.objects.count(),
            "work_orders": WorkOrder.objects.count(),
            "tests": Teste.objects.count(),
        }
        return Response(data)
