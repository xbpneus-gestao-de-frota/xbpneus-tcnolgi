from rest_framework import serializers
from .models import Fatura, ItemFatura, NotaFiscal

class ItemFaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemFatura
        fields = '__all__'
        read_only_fields = ['criado_em', 'valor_total']

class NotaFiscalSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = NotaFiscal
        fields = '__all__'
        read_only_fields = ['criado_em', 'atualizado_em']

class FaturaSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='cliente.nome_razao_social', read_only=True)
    viagem_numero = serializers.CharField(source='viagem.numero_viagem', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    dias_ate_vencimento_calc = serializers.IntegerField(source='dias_ate_vencimento', read_only=True)
    itens = ItemFaturaSerializer(many=True, read_only=True)
    notas_fiscais = NotaFiscalSerializer(many=True, read_only=True)
    
    class Meta:
        model = Fatura
        fields = '__all__'
        read_only_fields = ['criado_em', 'atualizado_em', 'valor_liquido']
