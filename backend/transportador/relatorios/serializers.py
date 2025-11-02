"""
Serializers para o módulo de Relatorios
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework import serializers
from .models import RelatorioTemplate, RelatorioAgendado, RelatorioGerado, DashboardPersonalizado


class RelatorioTemplateSerializer(serializers.ModelSerializer):
    """Serializer para RelatorioTemplate"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = RelatorioTemplate
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class RelatorioAgendadoSerializer(serializers.ModelSerializer):
    """Serializer para RelatorioAgendado"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = RelatorioAgendado
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class RelatorioGeradoSerializer(serializers.ModelSerializer):
    """Serializer para RelatorioGerado"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = RelatorioGerado
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class DashboardPersonalizadoSerializer(serializers.ModelSerializer):
    """Serializer para DashboardPersonalizado"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = DashboardPersonalizado
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


