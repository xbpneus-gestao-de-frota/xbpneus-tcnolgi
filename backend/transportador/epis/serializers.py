"""
Serializers para o módulo de Epis
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework import serializers
from .models import TipoEPI, EPI, EntregaEPI, FichaEPI


class TipoEPISerializer(serializers.ModelSerializer):
    """Serializer para TipoEPI"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = TipoEPI
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class EPISerializer(serializers.ModelSerializer):
    """Serializer para EPI"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = EPI
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class EntregaEPISerializer(serializers.ModelSerializer):
    """Serializer para EntregaEPI"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = EntregaEPI
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class FichaEPISerializer(serializers.ModelSerializer):
    """Serializer para FichaEPI"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = FichaEPI
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


