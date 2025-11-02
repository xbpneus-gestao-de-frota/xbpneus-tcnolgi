from rest_framework import serializers
from .models import CategoriaProduto, Produto, Pedido, ItemPedido, MovimentacaoEstoqueLoja


class CategoriaProdutoSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = CategoriaProduto
        fields = '__all__'


class ProdutoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    estoque_baixo_flag = serializers.BooleanField(source='estoque_baixo', read_only=True)
    
    class Meta:
        model = Produto
        fields = '__all__'
        read_only_fields = ['criado_em', 'atualizado_em']


class ItemPedidoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    produto_codigo = serializers.CharField(source='produto.codigo', read_only=True)
    
    class Meta:
        model = ItemPedido
        fields = '__all__'
        read_only_fields = ['valor_total']


class PedidoSerializer(serializers.ModelSerializer):
    itens = ItemPedidoSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = Pedido
        fields = '__all__'
        read_only_fields = ['criado_em', 'atualizado_em', 'valor_produtos', 'valor_total']


class MovimentacaoEstoqueLojaSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = MovimentacaoEstoqueLoja
        fields = '__all__'
        read_only_fields = ['data_movimentacao']
