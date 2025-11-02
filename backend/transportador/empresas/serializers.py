from rest_framework import serializers
from .models import Empresa, Filial


class FilialSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Filial"""
    empresa_nome = serializers.CharField(source='empresa.nome', read_only=True)
    
    class Meta:
        model = Filial
        fields = [
            'id',
            'empresa',
            'empresa_nome',
            'codigo',
            'nome',
            'cnpj',
            'inscricao_estadual',
            'inscricao_municipal',
            'cep',
            'endereco',
            'numero',
            'complemento',
            'bairro',
            'cidade',
            'estado',
            'telefone',
            'celular',
            'email',
            'matriz',
            'ativa',
            'criado_em',
            'atualizado_em',
        ]
        read_only_fields = ['criado_em', 'atualizado_em']


class FilialListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de Filiais"""
    empresa_nome = serializers.CharField(source='empresa.nome', read_only=True)
    
    class Meta:
        model = Filial
        fields = [
            'id',
            'empresa',
            'empresa_nome',
            'codigo',
            'nome',
            'cidade',
            'estado',
            'matriz',
            'ativa',
        ]


class EmpresaSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Empresa"""
    filiais = FilialListSerializer(many=True, read_only=True)
    total_filiais = serializers.SerializerMethodField()
    
    class Meta:
        model = Empresa
        fields = [
            'id',
            'nome',
            'tipo',
            'cnpj',
            'razao_social',
            'nome_fantasia',
            'inscricao_estadual',
            'inscricao_municipal',
            'cep',
            'endereco',
            'numero',
            'complemento',
            'bairro',
            'cidade',
            'estado',
            'telefone',
            'celular',
            'email',
            'site',
            'ativa',
            'criado_em',
            'atualizado_em',
            'filiais',
            'total_filiais',
        ]
        read_only_fields = ['criado_em', 'atualizado_em']
    
    def get_total_filiais(self, obj):
        """Retorna o total de filiais da empresa"""
        return obj.filiais.count()


class EmpresaListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de Empresas"""
    total_filiais = serializers.SerializerMethodField()
    
    class Meta:
        model = Empresa
        fields = [
            'id',
            'nome',
            'tipo',
            'cnpj',
            'cidade',
            'estado',
            'ativa',
            'total_filiais',
        ]
    
    def get_total_filiais(self, obj):
        """Retorna o total de filiais da empresa"""
        return obj.filiais.count()

