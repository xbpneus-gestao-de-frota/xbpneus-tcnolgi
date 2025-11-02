from rest_framework import serializers
from .models import Fornecedor, ContatoFornecedor


class ContatoFornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContatoFornecedor
        fields = '__all__'
        read_only_fields = ['criado_em']


class FornecedorSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    categoria_display = serializers.CharField(source='get_categoria_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    contatos = ContatoFornecedorSerializer(many=True, read_only=True)
    
    class Meta:
        model = Fornecedor
        fields = '__all__'
        read_only_fields = ['criado_em', 'atualizado_em']
