from rest_framework import serializers
from .models import UsuarioTransportador


class UsuarioTransportadorSerializer(serializers.ModelSerializer):
    """Serializer para UsuarioTransportador"""
    
    class Meta:
        model = UsuarioTransportador
        fields = ["id", "email", "nome_razao_social", "cnpj", "telefone", "aprovado", "is_active", "criado_em"]
        read_only_fields = ["id", "aprovado", "is_active", "criado_em"]


class RegistroTransportadorSerializer(serializers.ModelSerializer):
    """Serializer para registro de novo transportador"""
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = UsuarioTransportador
        fields = ["email", "nome_razao_social", "cnpj", "telefone", "password", "password_confirm"]

    
    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError({"password": "As senhas não coincidem"})

        return data
    
    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("password_confirm")

        # O create_user do manager já chama set_password internamente
        user = UsuarioTransportador.objects.create_user(password=password, **validated_data)

        return user


class LoginTransportadorSerializer(serializers.Serializer):
    """Serializer para login de transportador"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)




