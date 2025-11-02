from rest_framework import serializers
from .models import (
    MotoristaInterno, VinculoMotoristaVeiculo, RegistroJornada,
    MensagemMotorista, AlertaMotorista
)


class MotoristaInternoSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    tipo_contrato_display = serializers.CharField(source='get_tipo_contrato_display', read_only=True)
    cnh_valida_flag = serializers.BooleanField(source='cnh_valida', read_only=True)
    
    class Meta:
        model = MotoristaInterno
        fields = '__all__'
        read_only_fields = ['criado_em', 'atualizado_em', 'ultimo_acesso_app']


class VinculoMotoristaVeiculoSerializer(serializers.ModelSerializer):
    motorista_nome = serializers.CharField(source='motorista.nome_completo', read_only=True)
    veiculo_placa = serializers.CharField(source='veiculo.placa', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = VinculoMotoristaVeiculo
        fields = '__all__'


class RegistroJornadaSerializer(serializers.ModelSerializer):
    motorista_nome = serializers.CharField(source='motorista.nome_completo', read_only=True)
    veiculo_placa = serializers.CharField(source='veiculo.placa', read_only=True)
    tipo_registro_display = serializers.CharField(source='get_tipo_registro_display', read_only=True)
    origem_display = serializers.CharField(source='get_origem_display', read_only=True)
    
    class Meta:
        model = RegistroJornada
        fields = '__all__'
        read_only_fields = ['criado_em']


class MensagemMotoristaSerializer(serializers.ModelSerializer):
    motorista_nome = serializers.CharField(source='motorista.nome_completo', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = MensagemMotorista
        fields = '__all__'
        read_only_fields = ['criado_em', 'data_entrega', 'data_leitura']


class AlertaMotoristaSerializer(serializers.ModelSerializer):
    motorista_nome = serializers.CharField(source='motorista.nome_completo', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    prioridade_display = serializers.CharField(source='get_prioridade_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = AlertaMotorista
        fields = '__all__'
        read_only_fields = ['criado_em', 'data_alerta']
