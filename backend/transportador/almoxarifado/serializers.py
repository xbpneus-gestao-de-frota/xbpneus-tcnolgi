"""
Serializers para o módulo de Almoxarifado
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework import serializers
from .models import (
    Almoxarifado, LocalEstoque, MovimentacaoAlmoxarifado,
    InventarioAlmoxarifado, ItemInventario, RequisicaoMaterial, ItemRequisicao
)


class LocalEstoqueSerializer(serializers.ModelSerializer):
    """Serializer para Local de Estoque"""
    almoxarifado_nome = serializers.CharField(source='almoxarifado.nome', read_only=True)
    
    class Meta:
        model = LocalEstoque
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em']


class AlmoxarifadoSerializer(serializers.ModelSerializer):
    """Serializer para Almoxarifado"""
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    responsavel_nome = serializers.CharField(source='responsavel.get_full_name', read_only=True)
    total_locais = serializers.IntegerField(source='locais.count', read_only=True)
    
    class Meta:
        model = Almoxarifado
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em']


class MovimentacaoAlmoxarifadoSerializer(serializers.ModelSerializer):
    """Serializer para Movimentação de Almoxarifado"""
    almoxarifado_nome = serializers.CharField(source='almoxarifado.nome', read_only=True)
    responsavel_nome = serializers.CharField(source='responsavel.get_full_name', read_only=True)
    
    class Meta:
        model = MovimentacaoAlmoxarifado
        fields = '__all__'
        read_only_fields = ['id', 'valor_total', 'criado_em', 'atualizado_em']


class ItemInventarioSerializer(serializers.ModelSerializer):
    """Serializer para Item de Inventário"""
    class Meta:
        model = ItemInventario
        fields = '__all__'
        read_only_fields = ['id', 'diferenca', 'valor_diferenca']


class InventarioAlmoxarifadoSerializer(serializers.ModelSerializer):
    """Serializer para Inventário de Almoxarifado"""
    almoxarifado_nome = serializers.CharField(source='almoxarifado.nome', read_only=True)
    responsavel_nome = serializers.CharField(source='responsavel.get_full_name', read_only=True)
    itens = ItemInventarioSerializer(many=True, read_only=True)
    total_itens = serializers.IntegerField(source='itens.count', read_only=True)
    
    class Meta:
        model = InventarioAlmoxarifado
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em']


class ItemRequisicaoSerializer(serializers.ModelSerializer):
    """Serializer para Item de Requisição"""
    class Meta:
        model = ItemRequisicao
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em']


class RequisicaoMaterialSerializer(serializers.ModelSerializer):
    """Serializer para Requisição de Material"""
    almoxarifado_nome = serializers.CharField(source='almoxarifado.nome', read_only=True)
    solicitante_nome = serializers.CharField(source='solicitante.get_full_name', read_only=True)
    itens = ItemRequisicaoSerializer(many=True, read_only=True)
    total_itens = serializers.IntegerField(source='itens.count', read_only=True)
    
    class Meta:
        model = RequisicaoMaterial
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em']
