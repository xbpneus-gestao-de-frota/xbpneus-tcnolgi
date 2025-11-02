from rest_framework import serializers
from .models import UsuarioRevenda


class UsuarioRevendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioRevenda
        fields = ['id', 'email', 'nome_razao_social', 'cnpj', 'telefone', 'endereco', 'aprovado', 'is_active', 'criado_em']
        read_only_fields = ['id', 'aprovado', 'is_active', 'criado_em']


class RegistroRevendaSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = UsuarioRevenda
        fields = ['email', 'nome_razao_social', 'cnpj', 'telefone', 'endereco', 'password', 'password_confirm']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "As senhas não coincidem"})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = UsuarioRevenda.objects.create_user(password=password, **validated_data)
        return user


class LoginRevendaSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
