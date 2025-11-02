from rest_framework import serializers
from .models import MotoristaExterno, AlocacaoMotorista

class MotoristaExternoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotoristaExterno
        fields = '__all__'

class AlocacaoMotoristaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlocacaoMotorista
        fields = '__all__'

