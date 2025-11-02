from django.conf import settings
"""
Models para o módulo de Treinamentos
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class CursoTreinamento(models.Model):
    """Model CursoTreinamento"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='treinamentos_cursotreinamento',
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
        related_name='treinamentos_cursotreinamento_criado',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'CursoTreinamento'
        verbose_name_plural = 'CursoTreinamentos'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class TreinamentoRealizado(models.Model):
    """Model TreinamentoRealizado"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='treinamentos_treinamentorealizado',
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
        related_name='treinamentos_treinamentorealizado_criado',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'TreinamentoRealizado'
        verbose_name_plural = 'TreinamentoRealizados'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class CertificadoTreinamento(models.Model):
    """Model CertificadoTreinamento"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='treinamentos_certificadotreinamento',
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
        related_name='treinamentos_certificadotreinamento_criado',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'CertificadoTreinamento'
        verbose_name_plural = 'CertificadoTreinamentos'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class InstrutorTreinamento(models.Model):
    """Model InstrutorTreinamento"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='treinamentos_instrutortreinamento',
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
        related_name='treinamentos_instrutortreinamento_criado',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'InstrutorTreinamento'
        verbose_name_plural = 'InstrutorTreinamentos'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


