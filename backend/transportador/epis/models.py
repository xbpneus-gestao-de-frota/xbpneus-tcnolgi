"""
Models para o módulo de Epis
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class TipoEPI(models.Model):
    """Model TipoEPI"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='epis_tipoepi',
        verbose_name='Empresa'
    )
    
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
    #     related_name='epis_tipoepi_criado',
    #     verbose_name='Criado por'
    # )
    
    class Meta:
        verbose_name = 'TipoEPI'
        verbose_name_plural = 'TipoEPIs'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class EPI(models.Model):
    """Model EPI"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='epis_epi',
        verbose_name='Empresa'
    )
    
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
    #     related_name='epis_epi_criado',
    #     verbose_name='Criado por'
    # )
    
    class Meta:
        verbose_name = 'EPI'
        verbose_name_plural = 'EPIs'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class EntregaEPI(models.Model):
    """Model EntregaEPI"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='epis_entregaepi',
        verbose_name='Empresa'
    )
    
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
    #     related_name='epis_entregaepi_criado',
    #     verbose_name='Criado por'
    # )
    
    class Meta:
        verbose_name = 'EntregaEPI'
        verbose_name_plural = 'EntregaEPIs'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class FichaEPI(models.Model):
    """Model FichaEPI"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='epis_fichaepi',
        verbose_name='Empresa'
    )
    
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
    #     related_name='epis_fichaepi_criado',
    #     verbose_name='Criado por'
    # )
    
    class Meta:
        verbose_name = 'FichaEPI'
        verbose_name_plural = 'FichaEPIs'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


