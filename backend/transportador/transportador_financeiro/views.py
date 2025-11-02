from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

class DespesaViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response([{"id": 1, "descricao": "Despesa Teste", "valor": 100.00}], status=status.HTTP_200_OK)

class LancamentoViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response([{"id": 1, "descricao": "Lancamento Teste", "valor": 200.00}], status=status.HTTP_200_OK)

