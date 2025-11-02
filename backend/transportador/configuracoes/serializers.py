"""
Serializers para o módulo de Configuracoes
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework import serializers
from .models import ConfiguracaoSistema, ParametroEmpresa, PerfilUsuario, PermissaoCustomizada


class ConfiguracaoSistemaSerializer(serializers.ModelSerializer):
    """Serializer para ConfiguracaoSistema"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = ConfiguracaoSistema
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class ParametroEmpresaSerializer(serializers.ModelSerializer):
    """Serializer para ParametroEmpresa"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = ParametroEmpresa
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class PerfilUsuarioSerializer(serializers.ModelSerializer):
    """Serializer para PerfilUsuario"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = PerfilUsuario
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']


class PermissaoCustomizadaSerializer(serializers.ModelSerializer):
    """Serializer para PermissaoCustomizada"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = PermissaoCustomizada
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']





# =============================================================================
# SERIALIZERS PARA TABELAS AUXILIARES
# =============================================================================

from .models import (
    CatalogoModeloVeiculo,
    MapaPosicaoPneu,
    OperacaoConfiguracao,
    MedidaPorPosicao,
    PressaoRecomendada,
    CatalogoPneuXBRI
)


class CatalogoModeloVeiculoSerializer(serializers.ModelSerializer):
    """Serializer para CatalogoModeloVeiculo"""
    
    class Meta:
        model = CatalogoModeloVeiculo
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em']


class MapaPosicaoPneuSerializer(serializers.ModelSerializer):
    """Serializer para MapaPosicaoPneu"""
    
    class Meta:
        model = MapaPosicaoPneu
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em']


class OperacaoConfiguracaoSerializer(serializers.ModelSerializer):
    """Serializer para OperacaoConfiguracao"""
    
    class Meta:
        model = OperacaoConfiguracao
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em']


class MedidaPorPosicaoSerializer(serializers.ModelSerializer):
    """Serializer para MedidaPorPosicao"""
    
    class Meta:
        model = MedidaPorPosicao
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em']


class PressaoRecomendadaSerializer(serializers.ModelSerializer):
    """Serializer para PressaoRecomendada"""
    
    class Meta:
        model = PressaoRecomendada
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em']


class CatalogoPneuXBRISerializer(serializers.ModelSerializer):
    """Serializer para CatalogoPneuXBRI"""
    
    class Meta:
        model = CatalogoPneuXBRI
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em']

