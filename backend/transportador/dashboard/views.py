from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.transportador.dashboard_views import collect_dashboard_payload


class MetricsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        _, _, metrics = collect_dashboard_payload(request.user)
        return Response(metrics)
