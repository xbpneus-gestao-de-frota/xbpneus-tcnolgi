from rest_framework import serializers

from .models import UsuarioMotorista


class UsuarioMotoristaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioMotorista
        fields = [
            'id',
            'email',
            'nome_completo',
            'cpf',
            'cnh',
            'categoria_cnh',
            'telefone',
            'aprovado',
            'is_active',
            'criado_em',
        ]
        read_only_fields = ['id', 'aprovado', 'is_active', 'criado_em']
