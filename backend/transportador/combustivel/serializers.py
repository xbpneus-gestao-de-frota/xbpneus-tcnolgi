from rest_framework import serializers
from .models import PostoCombustivel, Abastecimento, ConsumoMensal


class PostoCombustivelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostoCombustivel
        fields = '__all__'
        read_only_fields = ['criado_em']


class AbastecimentoSerializer(serializers.ModelSerializer):
    veiculo_placa = serializers.CharField(source='veiculo.placa', read_only=True)
    posto_nome = serializers.CharField(source='posto.nome', read_only=True)
    tipo_combustivel_display = serializers.CharField(source='get_tipo_combustivel_display', read_only=True)
    forma_pagamento_display = serializers.CharField(source='get_forma_pagamento_display', read_only=True)
    
    class Meta:
        model = Abastecimento
        fields = '__all__'
        read_only_fields = ['criado_em', 'valor_total', 'km_desde_ultimo', 'consumo_medio']


class ConsumoMensalSerializer(serializers.ModelSerializer):
    veiculo_placa = serializers.CharField(source='veiculo.placa', read_only=True)
    
    class Meta:
        model = ConsumoMensal
        fields = '__all__'
        read_only_fields = ['criado_em']
