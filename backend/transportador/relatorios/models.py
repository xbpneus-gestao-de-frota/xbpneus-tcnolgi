from django.conf import settings
"""
Models para o módulo de Relatorios
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class RelatorioTemplate(models.Model):
    """Model RelatorioTemplate"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='relatorios_relatoriotemplate',
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
        related_name='relatorios_relatoriotemplate_criado',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'RelatorioTemplate'
        verbose_name_plural = 'RelatorioTemplates'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class RelatorioAgendado(models.Model):
    """Model RelatorioAgendado"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='relatorios_relatorioagendado',
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
        related_name='relatorios_relatorioagendado_criado',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'RelatorioAgendado'
        verbose_name_plural = 'RelatorioAgendados'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class RelatorioGerado(models.Model):
    """Model RelatorioGerado"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='relatorios_relatoriogerado',
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
        related_name='relatorios_relatoriogerado_criado',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'RelatorioGerado'
        verbose_name_plural = 'RelatorioGerados'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class DashboardPersonalizado(models.Model):
    """Model DashboardPersonalizado"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='relatorios_dashboardpersonalizado',
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
        related_name='relatorios_dashboardpersonalizado_criado',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'DashboardPersonalizado'
        verbose_name_plural = 'DashboardPersonalizados'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


