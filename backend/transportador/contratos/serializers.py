from rest_framework import serializers
from .models import Contrato, Aditivo


class AditivoSerializer(serializers.ModelSerializer):
    contrato_numero = serializers.CharField(source='contrato.numero_contrato', read_only=True)
    
    class Meta:
        model = Aditivo
        fields = '__all__'
        read_only_fields = ['criado_em']


class ContratoSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='cliente.nome_razao_social', read_only=True)
    fornecedor_nome = serializers.CharField(source='fornecedor.nome_razao_social', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    dias_para_vencer_calc = serializers.IntegerField(source='dias_para_vencer', read_only=True)
    aditivos = AditivoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Contrato
        fields = '__all__'
        read_only_fields = ['criado_em', 'atualizado_em']
