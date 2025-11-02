from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

class GarantiaViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response([{"id": 1, "tipo": "Garantia Teste", "validade": "2026-10-16"}], status=status.HTTP_200_OK)

