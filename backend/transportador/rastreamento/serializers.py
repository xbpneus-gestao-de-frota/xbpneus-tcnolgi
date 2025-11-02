from rest_framework import serializers
from .models import Posicao, CercaEletronica, ViolacaoCerca, HistoricoRastreamento

class PosicaoSerializer(serializers.ModelSerializer):
    veiculo_placa = serializers.CharField(source='veiculo.placa', read_only=True)
    
    class Meta:
        model = Posicao
        fields = '__all__'
        read_only_fields = ['criado_em']

class CercaEletronicaSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = CercaEletronica
        fields = '__all__'
        read_only_fields = ['criado_em', 'atualizado_em']

class ViolacaoCercaSerializer(serializers.ModelSerializer):
    cerca_nome = serializers.CharField(source='cerca.nome', read_only=True)
    veiculo_placa = serializers.CharField(source='veiculo.placa', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = ViolacaoCerca
        fields = '__all__'
        read_only_fields = ['criado_em']

class HistoricoRastreamentoSerializer(serializers.ModelSerializer):
    veiculo_placa = serializers.CharField(source='veiculo.placa', read_only=True)
    
    class Meta:
        model = HistoricoRastreamento
        fields = '__all__'
        read_only_fields = ['criado_em']
