"""
Serializers para o módulo de Treinamentos
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework import serializers
from .models import CursoTreinamento, TreinamentoRealizado, CertificadoTreinamento, InstrutorTreinamento


class CursoTreinamentoSerializer(serializers.ModelSerializer):
    """Serializer para CursoTreinamento"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = CursoTreinamento
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class TreinamentoRealizadoSerializer(serializers.ModelSerializer):
    """Serializer para TreinamentoRealizado"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = TreinamentoRealizado
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class CertificadoTreinamentoSerializer(serializers.ModelSerializer):
    """Serializer para CertificadoTreinamento"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = CertificadoTreinamento
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class InstrutorTreinamentoSerializer(serializers.ModelSerializer):
    """Serializer para InstrutorTreinamento"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = InstrutorTreinamento
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


