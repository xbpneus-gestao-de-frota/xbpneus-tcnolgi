"""
Serializers para o módulo de Auditoria
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework import serializers
from .models import (
    LogAuditoria,
    LogAcesso,
    LogAlteracao,
    SessaoUsuario,
    ConfiguracaoAuditoria
)


class LogAuditoriaSerializer(serializers.ModelSerializer):
    """Serializer para Log de Auditoria"""
    
    usuario_nome = serializers.CharField(source='usuario.get_full_name', read_only=True)
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    alteracoes = serializers.ReadOnlyField()
    
    class Meta:
        model = LogAuditoria
        fields = [
            'id', 'usuario', 'usuario_nome', 'empresa', 'empresa_nome',
            'acao', 'descricao', 'severidade', 'content_type', 'object_id',
            'ip_address', 'user_agent', 'metodo_http', 'url',
            'dados_anteriores', 'dados_novos', 'alteracoes',
            'modulo', 'funcao', 'mensagem_erro', 'stack_trace',
            'criado_em'
        ]
        read_only_fields = ['id', 'criado_em']


class LogAcessoSerializer(serializers.ModelSerializer):
    """Serializer para Log de Acesso"""
    
    usuario_nome = serializers.CharField(source='usuario.username', read_only=True)
    
    class Meta:
        model = LogAcesso
        fields = [
            'id', 'usuario', 'usuario_nome', 'tipo_acesso',
            'ip_address', 'user_agent', 'dispositivo', 'navegador',
            'sistema_operacional', 'pais', 'cidade', 'sucesso',
            'motivo_falha', 'criado_em'
        ]
        read_only_fields = ['id', 'criado_em']


class LogAlteracaoSerializer(serializers.ModelSerializer):
    """Serializer para Log de Alteração"""
    
    usuario_nome = serializers.CharField(source='usuario.get_full_name', read_only=True)
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    tipo_objeto = serializers.CharField(source='content_type.model', read_only=True)
    
    class Meta:
        model = LogAlteracao
        fields = [
            'id', 'usuario', 'usuario_nome', 'empresa', 'empresa_nome',
            'content_type', 'tipo_objeto', 'object_id', 'object_repr',
            'tipo_alteracao', 'campo', 'valor_anterior', 'valor_novo',
            'criado_em'
        ]
        read_only_fields = ['id', 'criado_em']


class SessaoUsuarioSerializer(serializers.ModelSerializer):
    """Serializer para Sessão de Usuário"""
    
    usuario_nome = serializers.CharField(source='usuario.get_full_name', read_only=True)
    duracao = serializers.ReadOnlyField()
    
    class Meta:
        model = SessaoUsuario
        fields = [
            'id', 'usuario', 'usuario_nome', 'session_key',
            'ip_address', 'user_agent', 'dispositivo', 'ativa',
            'iniciada_em', 'ultima_atividade', 'encerrada_em',
            'motivo_encerramento', 'duracao'
        ]
        read_only_fields = ['id', 'iniciada_em', 'ultima_atividade']


class ConfiguracaoAuditoriaSerializer(serializers.ModelSerializer):
    """Serializer para Configuração de Auditoria"""
    
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    
    class Meta:
        model = ConfiguracaoAuditoria
        fields = [
            'id', 'empresa', 'empresa_nome', 'registrar_visualizacoes',
            'registrar_exportacoes', 'registrar_alteracoes',
            'registrar_exclusoes', 'dias_retencao_logs',
            'dias_retencao_logs_acesso', 'notificar_acessos_suspeitos',
            'notificar_alteracoes_criticas', 'email_notificacao',
            'modulos_auditados', 'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['id', 'criado_em', 'atualizado_em']
