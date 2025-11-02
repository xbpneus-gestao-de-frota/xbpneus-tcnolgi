from rest_framework import serializers
from .models import CategoriaCusto, Custo, CustoPorKm


class CategoriaCustoSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = CategoriaCusto
        fields = '__all__'


class CustoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    veiculo_placa = serializers.CharField(source='veiculo.placa', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    esta_vencido_flag = serializers.BooleanField(source='esta_vencido', read_only=True)
    
    class Meta:
        model = Custo
        fields = '__all__'
        read_only_fields = ['criado_em', 'atualizado_em']


class CustoPorKmSerializer(serializers.ModelSerializer):
    veiculo_placa = serializers.CharField(source='veiculo.placa', read_only=True)
    
    class Meta:
        model = CustoPorKm
        fields = '__all__'
        read_only_fields = ['criado_em', 'custo_por_km']
