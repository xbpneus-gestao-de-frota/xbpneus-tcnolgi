from rest_framework import serializers
from .models import Seguradora, Apolice, Sinistro


class SeguradoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seguradora
        fields = '__all__'
        read_only_fields = ['criado_em']


class ApoliceSerializer(serializers.ModelSerializer):
    seguradora_nome = serializers.CharField(source='seguradora.nome', read_only=True)
    veiculo_placa = serializers.CharField(source='veiculo.placa', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    dias_para_vencer_calc = serializers.IntegerField(source='dias_para_vencer', read_only=True)
    
    class Meta:
        model = Apolice
        fields = '__all__'
        read_only_fields = ['criado_em', 'atualizado_em']


class SinistroSerializer(serializers.ModelSerializer):
    apolice_numero = serializers.CharField(source='apolice.numero_apolice', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    valor_liquido_calc = serializers.DecimalField(source='valor_liquido', max_digits=12, decimal_places=2, read_only=True)
    
    class Meta:
        model = Sinistro
        fields = '__all__'
        read_only_fields = ['criado_em', 'atualizado_em']
