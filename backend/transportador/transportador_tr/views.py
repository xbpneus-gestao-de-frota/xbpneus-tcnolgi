from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

class TRViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response([{"id": 1, "descricao": "TR Teste", "status": "ativo"}], status=status.HTTP_200_OK)

