"""
Serializers para o módulo de Cargas
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework import serializers
from .models import TipoCarga, Carga, ItemCarga, ManifestoCarga, RastreamentoCarga


class TipoCargaSerializer(serializers.ModelSerializer):
    """Serializer para TipoCarga"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = TipoCarga
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class CargaSerializer(serializers.ModelSerializer):
    """Serializer para Carga"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = Carga
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class ItemCargaSerializer(serializers.ModelSerializer):
    """Serializer para ItemCarga"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = ItemCarga
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class ManifestoCargaSerializer(serializers.ModelSerializer):
    """Serializer para ManifestoCarga"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = ManifestoCarga
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class RastreamentoCargaSerializer(serializers.ModelSerializer):
    """Serializer para RastreamentoCarga"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = RastreamentoCarga
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


