"""
Serializers para o módulo de Pecas
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework import serializers
from .models import CategoriaPeca, Peca, EstoquePeca, MovimentacaoPeca, FornecedorPeca


class CategoriaPecaSerializer(serializers.ModelSerializer):
    """Serializer para CategoriaPeca"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = CategoriaPeca
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class PecaSerializer(serializers.ModelSerializer):
    """Serializer para Peca"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = Peca
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class EstoquePecaSerializer(serializers.ModelSerializer):
    """Serializer para EstoquePeca"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = EstoquePeca
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class MovimentacaoPecaSerializer(serializers.ModelSerializer):
    """Serializer para MovimentacaoPeca"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = MovimentacaoPeca
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class FornecedorPecaSerializer(serializers.ModelSerializer):
    """Serializer para FornecedorPeca"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = FornecedorPeca
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


