from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

class RelatorioTransportadorViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response([{"id": 1, "nome": "Relatorio Teste", "data": "2025-10-16"}], status=status.HTTP_200_OK)

