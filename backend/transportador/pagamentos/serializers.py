from rest_framework import serializers
from .models import ContaPagar, ContaReceber, Pagamento

class PagamentoSerializer(serializers.ModelSerializer):
    forma_pagamento_display = serializers.CharField(source='get_forma_pagamento_display', read_only=True)
    
    class Meta:
        model = Pagamento
        fields = '__all__'
        read_only_fields = ['criado_em']

class ContaPagarSerializer(serializers.ModelSerializer):
    fornecedor_nome = serializers.CharField(source='fornecedor.nome_razao_social', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    valor_total_calc = serializers.DecimalField(source='valor_total', max_digits=12, decimal_places=2, read_only=True)
    dias_ate_vencimento_calc = serializers.IntegerField(source='dias_ate_vencimento', read_only=True)
    pagamentos = PagamentoSerializer(many=True, read_only=True)
    
    class Meta:
        model = ContaPagar
        fields = '__all__'
        read_only_fields = ['criado_em', 'atualizado_em']

class ContaReceberSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='cliente.nome_razao_social', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    valor_total_calc = serializers.DecimalField(source='valor_total', max_digits=12, decimal_places=2, read_only=True)
    dias_ate_vencimento_calc = serializers.IntegerField(source='dias_ate_vencimento', read_only=True)
    recebimentos = PagamentoSerializer(many=True, read_only=True)
    
    class Meta:
        model = ContaReceber
        fields = '__all__'
        read_only_fields = ['criado_em', 'atualizado_em']
