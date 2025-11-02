"""
Models para o módulo de Ferramentas
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Ferramenta(models.Model):
    """Model Ferramenta"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='ferramentas_ferramenta',
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
    #     related_name='ferramentas_ferramenta_criado',
    #     verbose_name='Criado por'
    # )
    
    class Meta:
        verbose_name = 'Ferramenta'
        verbose_name_plural = 'Ferramentas'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class EmprestimoFerramenta(models.Model):
    """Model EmprestimoFerramenta"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='ferramentas_emprestimoferramenta',
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
    #     related_name='ferramentas_emprestimoferramenta_criado',
    #     verbose_name='Criado por'
    # )
    
    class Meta:
        verbose_name = 'EmprestimoFerramenta'
        verbose_name_plural = 'EmprestimoFerramentas'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class ManutencaoFerramenta(models.Model):
    """Model ManutencaoFerramenta"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='ferramentas_manutencaoferramenta',
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
    #     related_name='ferramentas_manutencaoferramenta_criado',
    #     verbose_name='Criado por'
    # )
    
    class Meta:
        verbose_name = 'ManutencaoFerramenta'
        verbose_name_plural = 'ManutencaoFerramentas'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class CalibracaoFerramenta(models.Model):
    """Model CalibracaoFerramenta"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='ferramentas_calibracaoferramenta',
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
    #     related_name='ferramentas_calibracaoferramenta_criado',
    #     verbose_name='Criado por'
    # )
    
    class Meta:
        verbose_name = 'CalibracaoFerramenta'
        verbose_name_plural = 'CalibracaoFerramentas'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


