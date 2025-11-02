"""
Serializers para o módulo de Compliance
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework import serializers
from .models import NormaCompliance, AuditoriaCompliance, NaoConformidade, PlanoAcaoCompliance


class NormaComplianceSerializer(serializers.ModelSerializer):
    """Serializer para NormaCompliance"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = NormaCompliance
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class AuditoriaComplianceSerializer(serializers.ModelSerializer):
    """Serializer para AuditoriaCompliance"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = AuditoriaCompliance
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class NaoConformidadeSerializer(serializers.ModelSerializer):
    """Serializer para NaoConformidade"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = NaoConformidade
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class PlanoAcaoComplianceSerializer(serializers.ModelSerializer):
    """Serializer para PlanoAcaoCompliance"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = PlanoAcaoCompliance
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


