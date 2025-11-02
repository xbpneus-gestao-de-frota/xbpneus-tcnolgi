"""
Serializers para o módulo de Notas Fiscais
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework import serializers
from .models import NotaFiscal, ItemNotaFiscal, ImpostoNotaFiscal, AnexoNotaFiscal


class ItemNotaFiscalSerializer(serializers.ModelSerializer):
    """Serializer para Item de Nota Fiscal"""
    
    class Meta:
        model = ItemNotaFiscal
        fields = [
            'id', 'nota_fiscal', 'numero_item', 'codigo_produto', 'descricao',
            'ncm', 'cfop', 'unidade', 'quantidade', 'valor_unitario',
            'valor_total', 'valor_desconto', 'aliquota_icms', 'valor_icms',
            'aliquota_ipi', 'valor_ipi', 'informacoes_adicionais',
            'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['id', 'valor_total', 'valor_icms', 'valor_ipi', 'criado_em', 'atualizado_em']


class ImpostoNotaFiscalSerializer(serializers.ModelSerializer):
    """Serializer para Imposto de Nota Fiscal"""
    
    class Meta:
        model = ImpostoNotaFiscal
        fields = [
            'id', 'nota_fiscal', 'tipo_imposto', 'base_calculo',
            'aliquota', 'valor_imposto', 'descricao',
            'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['id', 'criado_em', 'atualizado_em']


class AnexoNotaFiscalSerializer(serializers.ModelSerializer):
    """Serializer para Anexo de Nota Fiscal"""
    
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = AnexoNotaFiscal
        fields = [
            'id', 'nota_fiscal', 'titulo', 'descricao', 'arquivo',
            'tipo_arquivo', 'tamanho_arquivo', 'criado_em',
            'criado_por', 'criado_por_nome'
        ]
        read_only_fields = ['id', 'tamanho_arquivo', 'criado_em', 'criado_por']


class NotaFiscalListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de Notas Fiscais"""
    
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = NotaFiscal
        fields = [
            'id', 'empresa', 'empresa_nome', 'numero', 'serie', 'modelo',
            'tipo', 'status', 'data_emissao', 'destinatario_nome',
            'valor_total', 'chave_acesso', 'criado_em', 'criado_por_nome'
        ]
        read_only_fields = ['id', 'criado_em']


class NotaFiscalDetailSerializer(serializers.ModelSerializer):
    """Serializer completo para Nota Fiscal"""
    
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    itens = ItemNotaFiscalSerializer(many=True, read_only=True)
    impostos = ImpostoNotaFiscalSerializer(many=True, read_only=True)
    anexos = AnexoNotaFiscalSerializer(many=True, read_only=True)
    
    class Meta:
        model = NotaFiscal
        fields = [
            'id', 'empresa', 'empresa_nome', 'numero', 'serie', 'modelo',
            'tipo', 'status', 'data_emissao', 'data_autorizacao', 'data_cancelamento',
            'emitente_cnpj', 'emitente_nome', 'emitente_ie',
            'destinatario_cpf_cnpj', 'destinatario_nome', 'destinatario_ie',
            'destinatario_endereco', 'valor_produtos', 'valor_servicos',
            'valor_desconto', 'valor_frete', 'valor_seguro',
            'valor_outras_despesas', 'valor_total', 'base_calculo_icms',
            'valor_icms', 'valor_ipi', 'valor_pis', 'valor_cofins',
            'chave_acesso', 'protocolo_autorizacao', 'motivo_cancelamento',
            'xml_enviado', 'xml_retorno', 'observacoes',
            'informacoes_complementares', 'criado_em', 'atualizado_em',
            'criado_por', 'criado_por_nome', 'itens', 'impostos', 'anexos'
        ]
        read_only_fields = ['id', 'valor_total', 'criado_em', 'atualizado_em', 'criado_por']


class NotaFiscalCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer para criação e atualização de Nota Fiscal"""
    
    class Meta:
        model = NotaFiscal
        fields = [
            'id', 'empresa', 'numero', 'serie', 'modelo', 'tipo', 'status',
            'data_emissao', 'data_autorizacao', 'data_cancelamento',
            'emitente_cnpj', 'emitente_nome', 'emitente_ie',
            'destinatario_cpf_cnpj', 'destinatario_nome', 'destinatario_ie',
            'destinatario_endereco', 'valor_produtos', 'valor_servicos',
            'valor_desconto', 'valor_frete', 'valor_seguro',
            'valor_outras_despesas', 'base_calculo_icms', 'valor_icms',
            'valor_ipi', 'valor_pis', 'valor_cofins', 'chave_acesso',
            'protocolo_autorizacao', 'motivo_cancelamento', 'xml_enviado',
            'xml_retorno', 'observacoes', 'informacoes_complementares'
        ]
        read_only_fields = ['id']
    
    def validate(self, data):
        """Validações customizadas"""
        # Validar CNPJ/CPF
        if 'destinatario_cpf_cnpj' in data:
            cpf_cnpj = data['destinatario_cpf_cnpj'].replace('.', '').replace('-', '').replace('/', '')
            if len(cpf_cnpj) not in [11, 14]:
                raise serializers.ValidationError({
                    'destinatario_cpf_cnpj': 'CPF/CNPJ inválido'
                })
        
        # Validar chave de acesso
        if 'chave_acesso' in data and data['chave_acesso']:
            if len(data['chave_acesso']) != 44:
                raise serializers.ValidationError({
                    'chave_acesso': 'Chave de acesso deve ter 44 caracteres'
                })
        
        return data
