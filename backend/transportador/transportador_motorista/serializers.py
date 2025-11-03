from rest_framework import serializers


class MotoristaTransportadorSerializer(serializers.Serializer):
    """Serializador de visão unificada de motoristas internos e externos."""

    id = serializers.CharField()
    tipo = serializers.ChoiceField(choices=["interno", "externo"])
    origem_id = serializers.CharField()
    nome = serializers.CharField()
    cpf = serializers.CharField(allow_blank=True, allow_null=True)
    cnh = serializers.CharField(allow_blank=True, allow_null=True)
    status = serializers.CharField(allow_blank=True, allow_null=True)
    empresa_id = serializers.IntegerField(allow_null=True)
    filial_id = serializers.IntegerField(allow_null=True, required=False)
    telefone = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    email = serializers.EmailField(allow_blank=True, allow_null=True, required=False)
    conectado_app = serializers.BooleanField(required=False)
    ultimo_acesso_app = serializers.DateTimeField(allow_null=True, required=False)
    aprovado = serializers.BooleanField(required=False)
