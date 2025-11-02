from rest_framework import serializers
from .models import UsuarioMotorista


class UsuarioMotoristaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioMotorista
        fields = ['id', 'email', 'nome_completo', 'cpf', 'cnh', 'categoria_cnh', 'telefone', 'aprovado', 'is_active', 'criado_em']
        read_only_fields = ['id', 'aprovado', 'is_active', 'criado_em']


class RegistroMotoristaSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = UsuarioMotorista
        fields = ['email', 'nome_completo', 'cpf', 'cnh', 'categoria_cnh', 'telefone', 'password', 'password_confirm']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "As senhas não coincidem"})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = UsuarioMotorista.objects.create_user(password=password, **validated_data)
        return user


class LoginMotoristaSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
