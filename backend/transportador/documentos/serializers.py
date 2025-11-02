from rest_framework import serializers
from .models import Documento

class DocumentoSerializer(serializers.ModelSerializer):
    veiculo_placa = serializers.CharField(source='veiculo.placa', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    dias_para_vencer_calc = serializers.IntegerField(source='dias_para_vencer', read_only=True)
    
    class Meta:
        model = Documento
        fields = '__all__'
        read_only_fields = ['criado_em', 'atualizado_em', 'status']
