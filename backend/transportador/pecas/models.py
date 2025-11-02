from django.conf import settings
"""
Models para o módulo de Pecas
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class CategoriaPeca(models.Model):
    """Model CategoriaPeca"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='pecas_categoriapeca',
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
        related_name='pecas_categoriapeca_criado',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'CategoriaPeca'
        verbose_name_plural = 'CategoriaPecas'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class Peca(models.Model):
    """Model Peca"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='pecas_peca',
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
        related_name='pecas_peca_criado',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'Peca'
        verbose_name_plural = 'Pecas'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class EstoquePeca(models.Model):
    """Model EstoquePeca"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='pecas_estoquepeca',
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
        related_name='pecas_estoquepeca_criado',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'EstoquePeca'
        verbose_name_plural = 'EstoquePecas'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class MovimentacaoPeca(models.Model):
    """Model MovimentacaoPeca"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='pecas_movimentacaopeca',
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
        related_name='pecas_movimentacaopeca_criado',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'MovimentacaoPeca'
        verbose_name_plural = 'MovimentacaoPecas'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class FornecedorPeca(models.Model):
    """Model FornecedorPeca"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='pecas_fornecedorpeca',
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
        related_name='pecas_fornecedorpeca_criado',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'FornecedorPeca'
        verbose_name_plural = 'FornecedorPecas'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


