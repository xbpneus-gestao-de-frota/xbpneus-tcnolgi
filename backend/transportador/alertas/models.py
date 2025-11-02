"""
Models para o módulo de Alertas
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class TipoAlerta(models.Model):
    """Model TipoAlerta"""
    
    # Relacionamentos
    # empresa = models.ForeignKey(
    #     on_delete=models.CASCADE,
    #     related_name='alertas_tipoalerta',
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
    #     related_name='alertas_tipoalerta_criado',
    #     verbose_name='Criado por'
    # )
    
    class Meta:
        verbose_name = 'TipoAlerta'
        verbose_name_plural = 'TipoAlertas'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class Alerta(models.Model):
    """Model Alerta"""
    
    # Relacionamentos
    # empresa = models.ForeignKey(
    #     on_delete=models.CASCADE,
    #     related_name='alertas_alerta',
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
    #     related_name='alertas_alerta_criado',
    #     verbose_name='Criado por'
    # )
    
    class Meta:
        verbose_name = 'Alerta'
        verbose_name_plural = 'Alertas'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class ConfiguracaoAlerta(models.Model):
    """Model ConfiguracaoAlerta"""
    
    # Relacionamentos
    # empresa = models.ForeignKey(
    #     on_delete=models.CASCADE,
    #     related_name='alertas_configuracaoalerta',
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
    #     related_name='alertas_configuracaoalerta_criado',
    #     verbose_name='Criado por'
    # )
    
    class Meta:
        verbose_name = 'ConfiguracaoAlerta'
        verbose_name_plural = 'ConfiguracaoAlertas'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class HistoricoAlerta(models.Model):
    """Model HistoricoAlerta"""
    
    # Relacionamentos
    # empresa = models.ForeignKey(
    #     on_delete=models.CASCADE,
    #     related_name='alertas_historicoalerta',
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
    #     related_name='alertas_historicoalerta_criado',
    #     verbose_name='Criado por'
    # )
    
    class Meta:
        verbose_name = 'HistoricoAlerta'
        verbose_name_plural = 'HistoricoAlertas'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


