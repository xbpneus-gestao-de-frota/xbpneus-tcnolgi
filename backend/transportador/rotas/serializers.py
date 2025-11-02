from rest_framework import serializers
from .models import Rota, PontoRota, RotaOtimizada

class PontoRotaSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = PontoRota
        fields = '__all__'
        read_only_fields = ['criado_em']

class RotaOtimizadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RotaOtimizada
        fields = '__all__'
        read_only_fields = ['criado_em']

class RotaSerializer(serializers.ModelSerializer):
    veiculo_placa = serializers.CharField(source='veiculo.placa', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    pontos = PontoRotaSerializer(many=True, read_only=True)
    otimizacoes = RotaOtimizadaSerializer(many=True, read_only=True)
    custo_total_calc = serializers.DecimalField(source='calcular_custo_total', max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Rota
        fields = '__all__'
        read_only_fields = ['criado_em', 'atualizado_em']
