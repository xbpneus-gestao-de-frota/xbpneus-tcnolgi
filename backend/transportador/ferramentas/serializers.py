"""
Serializers para o módulo de Ferramentas
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework import serializers
from .models import Ferramenta, EmprestimoFerramenta, ManutencaoFerramenta, CalibracaoFerramenta


class FerramentaSerializer(serializers.ModelSerializer):
    """Serializer para Ferramenta"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = Ferramenta
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class EmprestimoFerramentaSerializer(serializers.ModelSerializer):
    """Serializer para EmprestimoFerramenta"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = EmprestimoFerramenta
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class ManutencaoFerramentaSerializer(serializers.ModelSerializer):
    """Serializer para ManutencaoFerramenta"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = ManutencaoFerramenta
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class CalibracaoFerramentaSerializer(serializers.ModelSerializer):
    """Serializer para CalibracaoFerramenta"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = CalibracaoFerramenta
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


