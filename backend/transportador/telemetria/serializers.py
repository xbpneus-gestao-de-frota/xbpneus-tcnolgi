from rest_framework import serializers
from .models import Dispositivo, Leitura, Alerta

class DispositivoSerializer(serializers.ModelSerializer):
    veiculo_placa = serializers.CharField(source='veiculo.placa', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Dispositivo
        fields = '__all__'
        read_only_fields = ['criado_em', 'atualizado_em']

class LeituraSerializer(serializers.ModelSerializer):
    dispositivo_tipo = serializers.CharField(source='dispositivo.get_tipo_display', read_only=True)
    
    class Meta:
        model = Leitura
        fields = '__all__'
        read_only_fields = ['criado_em']

class AlertaSerializer(serializers.ModelSerializer):
    dispositivo_veiculo = serializers.CharField(source='dispositivo.veiculo.placa', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    severidade_display = serializers.CharField(source='get_severidade_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Alerta
        fields = '__all__'
        read_only_fields = ['criado_em']
