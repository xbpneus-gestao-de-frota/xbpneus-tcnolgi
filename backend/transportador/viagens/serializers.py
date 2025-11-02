from rest_framework import serializers
from .models import Viagem, Carga, Parada


class CargaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carga
        fields = '__all__'
        read_only_fields = ['criado_em']


class ParadaSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = Parada
        fields = '__all__'
        read_only_fields = ['criado_em', 'duracao_minutos']


class ViagemSerializer(serializers.ModelSerializer):
    veiculo_placa = serializers.CharField(source='veiculo.placa', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    cargas = CargaSerializer(many=True, read_only=True)
    paradas = ParadaSerializer(many=True, read_only=True)
    lucro_calc = serializers.DecimalField(source='lucro', max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Viagem
        fields = '__all__'
        read_only_fields = ['criado_em', 'atualizado_em', 'km_percorrido']
