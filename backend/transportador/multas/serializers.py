from rest_framework import serializers
from .models import Multa, RecursoMulta, PontuacaoCNH


class MultaSerializer(serializers.ModelSerializer):
    veiculo_placa = serializers.CharField(source='veiculo.placa', read_only=True)
    gravidade_display = serializers.CharField(source='get_gravidade_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    esta_vencida_flag = serializers.BooleanField(source='esta_vencida', read_only=True)
    valor_com_desconto_calc = serializers.DecimalField(source='valor_com_desconto', max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Multa
        fields = '__all__'
        read_only_fields = ['criado_em', 'atualizado_em']


class RecursoMultaSerializer(serializers.ModelSerializer):
    multa_numero = serializers.CharField(source='multa.numero_auto', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = RecursoMulta
        fields = '__all__'
        read_only_fields = ['criado_em']


class PontuacaoCNHSerializer(serializers.ModelSerializer):
    em_risco_flag = serializers.BooleanField(source='em_risco', read_only=True)
    
    class Meta:
        model = PontuacaoCNH
        fields = '__all__'
