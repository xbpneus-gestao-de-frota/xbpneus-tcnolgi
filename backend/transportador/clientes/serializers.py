from rest_framework import serializers
from .models import Cliente, ContatoCliente


class ContatoClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContatoCliente
        fields = '__all__'
        read_only_fields = ['criado_em']


class ClienteSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    contatos = ContatoClienteSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cliente
        fields = '__all__'
        read_only_fields = ['criado_em', 'atualizado_em']
