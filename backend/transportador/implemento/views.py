from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

class ImplementoViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response([{"id": 1, "nome": "Implemento Teste"}], status=status.HTTP_200_OK)

