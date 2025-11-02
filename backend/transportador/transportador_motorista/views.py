from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

class MotoristaTransportadorViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response([{"id": 1, "nome": "Motorista Teste", "cpf": "111.111.111-11"}], status=status.HTTP_200_OK)

