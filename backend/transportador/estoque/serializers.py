"""
Serializers expandidos para o módulo de Estoque
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework import serializers
from .models import (
    CategoriaProduto, Produto, SaldoEstoque, StockMove,
    MovimentacaoEstoque, PrevisaoDemanda, CurvaABC
)


class CategoriaProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaProduto
        fields = '__all__'


class ProdutoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    estoque_atual = serializers.ReadOnlyField()
    necessita_reposicao = serializers.ReadOnlyField()
    
    class Meta:
        model = Produto
        fields = '__all__'


class SaldoEstoqueSerializer(serializers.ModelSerializer):
    produto_codigo = serializers.CharField(source='produto.codigo', read_only=True)
    produto_descricao = serializers.CharField(source='produto.descricao', read_only=True)
    
    class Meta:
        model = SaldoEstoque
        fields = '__all__'


class MovimentacaoEstoqueSerializer(serializers.ModelSerializer):
    produto_codigo = serializers.CharField(source='produto.codigo', read_only=True)
    responsavel_nome = serializers.CharField(source='responsavel.get_full_name', read_only=True)
    
    class Meta:
        model = MovimentacaoEstoque
        fields = '__all__'
        read_only_fields = ['valor_total', 'criado_em']


class PrevisaoDemandaSerializer(serializers.ModelSerializer):
    produto_codigo = serializers.CharField(source='produto.codigo', read_only=True)
    acuracia = serializers.ReadOnlyField()
    
    class Meta:
        model = PrevisaoDemanda
        fields = '__all__'


class CurvaABCSerializer(serializers.ModelSerializer):
    produto_codigo = serializers.CharField(source='produto.codigo', read_only=True)
    
    class Meta:
        model = CurvaABC
        fields = '__all__'
