"""
Serializers para o módulo de Integracoes
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework import serializers
from .models import IntegracaoExterna, LogIntegracao, WebhookConfig, APICredential


class IntegracaoExternaSerializer(serializers.ModelSerializer):
    """Serializer para IntegracaoExterna"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = IntegracaoExterna
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class LogIntegracaoSerializer(serializers.ModelSerializer):
    """Serializer para LogIntegracao"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = LogIntegracao
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class WebhookConfigSerializer(serializers.ModelSerializer):
    """Serializer para WebhookConfig"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = WebhookConfig
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class APICredentialSerializer(serializers.ModelSerializer):
    """Serializer para APICredential"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = APICredential
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


