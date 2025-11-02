from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

class AnalisePneusViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response([{"id": 1, "tipo": "Desgaste", "resultado": "Normal"}], status=status.HTTP_200_OK)

