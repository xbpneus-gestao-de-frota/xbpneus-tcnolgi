from django.conf import settings
"""
Models para o módulo de Compliance
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class NormaCompliance(models.Model):
    """Model NormaCompliance"""
    
    # Relacionamentos
    # empresa = models.ForeignKey(
    #     on_delete=models.CASCADE,
    #     related_name='compliance_normacompliance',
    #     verbose_name='Empresa'
    # )
    
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
        related_name='compliance_normacompliance_criado',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'NormaCompliance'
        verbose_name_plural = 'NormaCompliances'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class AuditoriaCompliance(models.Model):
    """Model AuditoriaCompliance"""
    
    # Relacionamentos
    # empresa = models.ForeignKey(
    #     on_delete=models.CASCADE,
    #     related_name='compliance_auditoriacompliance',
    #     verbose_name='Empresa'
    # )
    
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
        related_name='compliance_auditoriacompliance_criado',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'AuditoriaCompliance'
        verbose_name_plural = 'AuditoriaCompliances'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class NaoConformidade(models.Model):
    """Model NaoConformidade"""
    
    # Relacionamentos
    # empresa = models.ForeignKey(
    #     on_delete=models.CASCADE,
    #     related_name='compliance_naoconformidade',
    #     verbose_name='Empresa'
    # )
    
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
        related_name='compliance_naoconformidade_criado',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'NaoConformidade'
        verbose_name_plural = 'NaoConformidades'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class PlanoAcaoCompliance(models.Model):
    """Model PlanoAcaoCompliance"""
    
    # Relacionamentos
    # empresa = models.ForeignKey(
    #     on_delete=models.CASCADE,
    #     related_name='compliance_planoacaocompliance',
    #     verbose_name='Empresa'
    # )
    
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
        related_name='compliance_planoacaocompliance_criado',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'PlanoAcaoCompliance'
        verbose_name_plural = 'PlanoAcaoCompliances'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


