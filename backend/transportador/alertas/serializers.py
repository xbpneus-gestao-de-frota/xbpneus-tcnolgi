"""
Serializers para o módulo de Alertas
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework import serializers
from .models import TipoAlerta, Alerta, ConfiguracaoAlerta, HistoricoAlerta


class TipoAlertaSerializer(serializers.ModelSerializer):
    """Serializer para TipoAlerta"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = TipoAlerta
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class AlertaSerializer(serializers.ModelSerializer):
    """Serializer para Alerta"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = Alerta
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class ConfiguracaoAlertaSerializer(serializers.ModelSerializer):
    """Serializer para ConfiguracaoAlerta"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = ConfiguracaoAlerta
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class HistoricoAlertaSerializer(serializers.ModelSerializer):
    """Serializer para HistoricoAlerta"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = HistoricoAlerta
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


