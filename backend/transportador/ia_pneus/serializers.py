from rest_framework import serializers
from .models import AnaliseIA, Gamificacao, Garantia


class AnaliseIASerializer(serializers.ModelSerializer):
    """Serializer para análises de IA"""
    
    class Meta:
        model = AnaliseIA
        fields = ['id', 'usuario', 'data_analise', 'tipo_analise', 'arquivo', 
                  'resultado', 'precisao', 'tempo_processamento', 'status']
        read_only_fields = ['id', 'data_analise', 'resultado', 'precisao', 
                            'tempo_processamento', 'status']


class GamificacaoSerializer(serializers.ModelSerializer):
    """Serializer para gamificação"""
    
    class Meta:
        model = Gamificacao
        fields = ['id', 'usuario', 'pontos', 'nivel', 'conquistas']
        read_only_fields = ['id']


class GarantiaSerializer(serializers.ModelSerializer):
    """Serializer para garantias"""
    
    class Meta:
        model = Garantia
        fields = ['id', 'usuario', 'analise', 'protocolo', 'status', 
                  'hash_blockchain', 'data_abertura', 'data_atualizacao']
        read_only_fields = ['id', 'protocolo', 'hash_blockchain', 'data_abertura', 'data_atualizacao']

