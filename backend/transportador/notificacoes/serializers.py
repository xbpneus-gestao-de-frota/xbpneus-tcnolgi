from rest_framework import serializers
from .models import CanalNotificacao, Notificacao, TemplateNotificacao, PreferenciaNotificacao

class CanalNotificacaoSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = CanalNotificacao
        fields = '__all__'
        read_only_fields = ['criado_em', 'atualizado_em']

class NotificacaoSerializer(serializers.ModelSerializer):
    canal_nome = serializers.CharField(source='canal.nome', read_only=True)
    prioridade_display = serializers.CharField(source='get_prioridade_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    pode_reenviar_calc = serializers.BooleanField(source='pode_reenviar', read_only=True)
    
    class Meta:
        model = Notificacao
        fields = '__all__'
        read_only_fields = ['criado_em', 'enviada_em', 'entregue_em', 'lida_em']

class TemplateNotificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateNotificacao
        fields = '__all__'
        read_only_fields = ['criado_em', 'atualizado_em']

class PreferenciaNotificacaoSerializer(serializers.ModelSerializer):
    usuario_username = serializers.CharField(source='usuario.username', read_only=True)
    esta_em_silencio_calc = serializers.BooleanField(source='esta_em_silencio', read_only=True)
    
    class Meta:
        model = PreferenciaNotificacao
        fields = '__all__'
        read_only_fields = ['criado_em', 'atualizado_em']
