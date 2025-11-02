from rest_framework import viewsets
from .models import MotoristaExterno, AlocacaoMotorista
from .serializers import MotoristaExternoSerializer, AlocacaoMotoristaSerializer

class MotoristaExternoViewSet(viewsets.ModelViewSet):
    queryset = MotoristaExterno.objects.all()
    serializer_class = MotoristaExternoSerializer

class AlocacaoMotoristaViewSet(viewsets.ModelViewSet):
    queryset = AlocacaoMotorista.objects.all()
    serializer_class = AlocacaoMotoristaSerializer

