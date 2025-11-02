from rest_framework import serializers
from .models import Entrega, POD, Ocorrencia, Tentativa

class PODSerializer(serializers.ModelSerializer):
    entrega_numero = serializers.CharField(source='entrega.numero_entrega', read_only=True)
    
    class Meta:
        model = POD
        fields = '__all__'
        read_only_fields = ['criado_em']

class OcorrenciaSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = Ocorrencia
        fields = '__all__'
        read_only_fields = ['criado_em']

class TentativaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tentativa
        fields = '__all__'
        read_only_fields = ['criado_em']

class EntregaSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='cliente.nome_razao_social', read_only=True)
    viagem_numero = serializers.CharField(source='viagem.numero_viagem', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    esta_atrasada_calc = serializers.BooleanField(source='esta_atrasada', read_only=True)
    pod = PODSerializer(read_only=True)
    ocorrencias = OcorrenciaSerializer(many=True, read_only=True)
    tentativas = TentativaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Entrega
        fields = '__all__'
        read_only_fields = ['criado_em', 'atualizado_em']
