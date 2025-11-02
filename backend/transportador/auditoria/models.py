from django.conf import settings
"""
Models para o módulo de Auditoria
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
import json


class TipoAcao(models.TextChoices):
    """Tipos de ação de auditoria"""
    CRIAR = 'CRIAR', 'Criar'
    ATUALIZAR = 'ATUALIZAR', 'Atualizar'
    DELETAR = 'DELETAR', 'Deletar'
    VISUALIZAR = 'VISUALIZAR', 'Visualizar'
    EXPORTAR = 'EXPORTAR', 'Exportar'
    IMPORTAR = 'IMPORTAR', 'Importar'
    LOGIN = 'LOGIN', 'Login'
    LOGOUT = 'LOGOUT', 'Logout'
    ERRO = 'ERRO', 'Erro'


class NivelSeveridade(models.TextChoices):
    """Níveis de severidade"""
    INFO = 'INFO', 'Informação'
    WARNING = 'WARNING', 'Aviso'
    ERROR = 'ERROR', 'Erro'
    CRITICAL = 'CRITICAL', 'Crítico'


class LogAuditoria(models.Model):
    """Log de Auditoria do Sistema"""
    
    # Usuário e empresa
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='logs_auditoria',
        verbose_name='Usuário'
    )
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='logs_auditoria_empresa',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa à qual o log de auditoria pertence"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='logs_auditoria_filial',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial à qual o log de auditoria está associado"
    )
    
    # Ação
    acao = models.CharField(
        'Ação',
        max_length=20,
        choices=TipoAcao.choices
    )
    descricao = models.TextField('Descrição')
    severidade = models.CharField(
        'Severidade',
        max_length=20,
        choices=NivelSeveridade.choices,
        default=NivelSeveridade.INFO
    )
    
    # Objeto relacionado (Generic Foreign Key)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Tipo de Conteúdo'
    )
    object_id = models.PositiveIntegerField('ID do Objeto', null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Dados da requisição
    ip_address = models.GenericIPAddressField('Endereço IP', null=True, blank=True)
    user_agent = models.TextField('User Agent', blank=True)
    metodo_http = models.CharField('Método HTTP', max_length=10, blank=True)
    url = models.TextField('URL', blank=True)
    
    # Dados antes e depois (para UPDATE)
    dados_anteriores = models.JSONField('Dados Anteriores', null=True, blank=True)
    dados_novos = models.JSONField('Dados Novos', null=True, blank=True)
    
    # Informações adicionais
    modulo = models.CharField('Módulo', max_length=100, blank=True)
    funcao = models.CharField('Função', max_length=100, blank=True)
    mensagem_erro = models.TextField('Mensagem de Erro', blank=True)
    stack_trace = models.TextField('Stack Trace', blank=True)
    
    # Timestamp
    criado_em = models.DateTimeField('Criado em', auto_now_add=True, db_index=True)
    
    class Meta:
        verbose_name = 'Log de Auditoria'
        verbose_name_plural = 'Logs de Auditoria'
        ordering = ['-criado_em']
        indexes = [
            models.Index(fields=['usuario', 'criado_em']),
            models.Index(fields=['empresa', 'criado_em']),
            models.Index(fields=['acao', 'criado_em']),
            models.Index(fields=['severidade', 'criado_em']),
            models.Index(fields=['content_type', 'object_id']),
        ]
    
    def __str__(self):
        usuario_nome = self.usuario.get_full_name() if self.usuario else 'Sistema'
        return f"{self.acao} - {usuario_nome} - {self.criado_em.strftime('%d/%m/%Y %H:%M')}"
    
    @property
    def alteracoes(self):
        """Retorna as alterações realizadas"""
        if not self.dados_anteriores or not self.dados_novos:
            return []
        
        alteracoes = []
        for campo, valor_novo in self.dados_novos.items():
            valor_anterior = self.dados_anteriores.get(campo)
            if valor_anterior != valor_novo:
                alteracoes.append({
                    'campo': campo,
                    'valor_anterior': valor_anterior,
                    'valor_novo': valor_novo
                })
        
        return alteracoes


class LogAcesso(models.Model):
    """Log de Acesso ao Sistema"""
    
    # Usuário
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='logs_acesso',
        verbose_name='Usuário'
    )
    
    # Tipo de acesso
    tipo_acesso = models.CharField(
        'Tipo de Acesso',
        max_length=20,
        choices=[
            ('LOGIN', 'Login'),
            ('LOGOUT', 'Logout'),
            ('LOGIN_FALHO', 'Login Falho'),
            ('SESSAO_EXPIRADA', 'Sessão Expirada'),
        ]
    )
    
    # Informações de acesso
    ip_address = models.GenericIPAddressField('Endereço IP', null=True, blank=True)
    user_agent = models.TextField('User Agent', blank=True)
    dispositivo = models.CharField('Dispositivo', max_length=100, blank=True)
    navegador = models.CharField('Navegador', max_length=100, blank=True)
    sistema_operacional = models.CharField('Sistema Operacional', max_length=100, blank=True)
    
    # Localização (se disponível)
    pais = models.CharField('País', max_length=100, blank=True)
    cidade = models.CharField('Cidade', max_length=100, blank=True)
    
    # Resultado
    sucesso = models.BooleanField('Sucesso', default=True)
    motivo_falha = models.TextField('Motivo da Falha', blank=True)
    
    # Timestamp
    criado_em = models.DateTimeField('Criado em', auto_now_add=True, db_index=True)
    
    class Meta:
        verbose_name = 'Log de Acesso'
        verbose_name_plural = 'Logs de Acesso'
        ordering = ['-criado_em']
        indexes = [
            models.Index(fields=['usuario', 'criado_em']),
            models.Index(fields=['tipo_acesso', 'criado_em']),
            models.Index(fields=['ip_address', 'criado_em']),
        ]
    
    def __str__(self):
        usuario_nome = self.usuario.username if self.usuario else 'Desconhecido'
        return f"{self.tipo_acesso} - {usuario_nome} - {self.criado_em.strftime('%d/%m/%Y %H:%M')}"


class LogAlteracao(models.Model):
    """Log detalhado de alterações em registros"""
    
    # Usuário
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='logs_alteracao',
        verbose_name='Usuário'
    )
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='logs_alteracao_empresa',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa à qual o log de alteração pertence"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='logs_alteracao_filial',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial à qual o log de alteração está associado"
    )
    
    # Objeto alterado
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name='Tipo de Conteúdo'
    )
    object_id = models.PositiveIntegerField('ID do Objeto')
    content_object = GenericForeignKey('content_type', 'object_id')
    object_repr = models.CharField('Representação do Objeto', max_length=200)
    
    # Tipo de alteração
    tipo_alteracao = models.CharField(
        'Tipo de Alteração',
        max_length=20,
        choices=[
            ('CREATE', 'Criação'),
            ('UPDATE', 'Atualização'),
            ('DELETE', 'Exclusão'),
        ]
    )
    
    # Campos alterados
    campo = models.CharField('Campo', max_length=100)
    valor_anterior = models.TextField('Valor Anterior', blank=True)
    valor_novo = models.TextField('Valor Novo', blank=True)
    
    # Timestamp
    criado_em = models.DateTimeField('Criado em', auto_now_add=True, db_index=True)
    
    class Meta:
        verbose_name = 'Log de Alteração'
        verbose_name_plural = 'Logs de Alteração'
        ordering = ['-criado_em']
        indexes = [
            models.Index(fields=['content_type', 'object_id', 'criado_em']),
            models.Index(fields=['usuario', 'criado_em']),
            models.Index(fields=['tipo_alteracao', 'criado_em']),
        ]
    
    def __str__(self):
        return f"{self.tipo_alteracao} - {self.object_repr} - {self.campo}"


class SessaoUsuario(models.Model):
    """Sessões ativas de usuários"""
    
    # Usuário
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sessoes',
        verbose_name='Usuário'
    )
    
    # Dados da sessão
    session_key = models.CharField('Chave da Sessão', max_length=40, unique=True)
    ip_address = models.GenericIPAddressField('Endereço IP', null=True, blank=True)
    user_agent = models.TextField('User Agent', blank=True)
    dispositivo = models.CharField('Dispositivo', max_length=100, blank=True)
    
    # Status
    ativa = models.BooleanField('Ativa', default=True)
    
    # Timestamps
    iniciada_em = models.DateTimeField('Iniciada em', auto_now_add=True)
    ultima_atividade = models.DateTimeField('Última Atividade', auto_now=True)
    encerrada_em = models.DateTimeField('Encerrada em', null=True, blank=True)
    
    # Motivo do encerramento
    motivo_encerramento = models.CharField(
        'Motivo do Encerramento',
        max_length=50,
        blank=True,
        choices=[
            ('LOGOUT', 'Logout'),
            ('TIMEOUT', 'Timeout'),
            ('ADMIN', 'Encerrada pelo Admin'),
            ('NOVA_SESSAO', 'Nova Sessão Iniciada'),
        ]
    )
    
    class Meta:
        verbose_name = 'Sessão de Usuário'
        verbose_name_plural = 'Sessões de Usuário'
        ordering = ['-iniciada_em']
        indexes = [
            models.Index(fields=['usuario', 'ativa']),
            models.Index(fields=['session_key']),
            models.Index(fields=['ultima_atividade']),
        ]
    
    def __str__(self):
        status = 'Ativa' if self.ativa else 'Encerrada'
        return f"{self.usuario.username} - {status} - {self.iniciada_em.strftime('%d/%m/%Y %H:%M')}"
    
    @property
    def duracao(self):
        """Retorna a duração da sessão"""
        if self.encerrada_em:
            return self.encerrada_em - self.iniciada_em
        from django.utils import timezone
        return timezone.now() - self.iniciada_em


class ConfiguracaoAuditoria(models.Model):
    """Configurações de auditoria por empresa"""
    
    # Empresa
    empresa = models.OneToOneField(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='configuracao_auditoria',
        verbose_name='Empresa',
        null=True,
        blank=True,
        help_text="Empresa à qual a configuração de auditoria pertence"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='configuracoes_auditoria_filial',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial à qual a configuração de auditoria está associada"
    )
    
    # Configurações de log
    registrar_visualizacoes = models.BooleanField('Registrar Visualizações', default=False)
    registrar_exportacoes = models.BooleanField('Registrar Exportações', default=True)
    registrar_alteracoes = models.BooleanField('Registrar Alterações', default=True)
    registrar_exclusoes = models.BooleanField('Registrar Exclusões', default=True)
    
    # Retenção de logs
    dias_retencao_logs = models.PositiveIntegerField('Dias de Retenção de Logs', default=365)
    dias_retencao_logs_acesso = models.PositiveIntegerField('Dias de Retenção de Logs de Acesso', default=90)
    
    # Notificações
    notificar_acessos_suspeitos = models.BooleanField('Notificar Acessos Suspeitos', default=True)
    notificar_alteracoes_criticas = models.BooleanField('Notificar Alterações Críticas', default=True)
    email_notificacao = models.EmailField('Email para Notificações', blank=True)
    
    # Módulos auditados
    modulos_auditados = models.JSONField('Módulos Auditados', default=list)
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Configuração de Auditoria'
        verbose_name_plural = 'Configurações de Auditoria'
    
    def __str__(self):
        return f"Configuração de Auditoria - {self.empresa.razao_social}"
