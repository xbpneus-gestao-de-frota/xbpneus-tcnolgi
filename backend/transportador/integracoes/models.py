from django.conf import settings
"""
Models para o módulo de Integracoes
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class IntegracaoExterna(models.Model):
    """Model IntegracaoExterna"""
    
    # Relacionamentos
    # empresa = models.ForeignKey(
    #     on_delete=models.CASCADE,
    #     related_name='integracoes_integracaoexterna',
    #     verbose_name='Empresa'
    # )
    
    # Dados básicos
    nome = models.CharField('Nome', max_length=200)
    descricao = models.TextField('Descrição', blank=True)
    ativo = models.BooleanField('Ativo', default=True)
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    # criado_por = models.ForeignKey(
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     related_name='integracoes_integracaoexterna_criado',
    #     verbose_name='Criado por'
    # )
    
    class Meta:
        verbose_name = 'IntegracaoExterna'
        verbose_name_plural = 'IntegracaoExternas'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class LogIntegracao(models.Model):
    """Model LogIntegracao"""
    
    # Relacionamentos
    # empresa = models.ForeignKey(
    #     on_delete=models.CASCADE,
    #     related_name='integracoes_logintegracao',
    #     verbose_name='Empresa'
    # )
    
    # Dados básicos
    nome = models.CharField('Nome', max_length=200)
    descricao = models.TextField('Descrição', blank=True)
    ativo = models.BooleanField('Ativo', default=True)
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    # criado_por = models.ForeignKey(
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     related_name='integracoes_logintegracao_criado',
    #     verbose_name='Criado por'
    # )
    
    class Meta:
        verbose_name = 'LogIntegracao'
        verbose_name_plural = 'LogIntegracaos'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class WebhookConfig(models.Model):
    """Model WebhookConfig"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='integracoes_webhookconfig',
        verbose_name='Empresa'
    )
    
    # Dados básicos
    nome = models.CharField('Nome', max_length=200)
    descricao = models.TextField('Descrição', blank=True)
    ativo = models.BooleanField('Ativo', default=True)
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='integracoes_webhookconfig_criado',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'WebhookConfig'
        verbose_name_plural = 'WebhookConfigs'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class APICredential(models.Model):
    """Model APICredential"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='integracoes_apicredential',
        verbose_name='Empresa'
    )
    
    # Dados básicos
    nome = models.CharField('Nome', max_length=200)
    descricao = models.TextField('Descrição', blank=True)
    ativo = models.BooleanField('Ativo', default=True)
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='integracoes_apicredential_criado',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'APICredential'
        verbose_name_plural = 'APICredentials'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


