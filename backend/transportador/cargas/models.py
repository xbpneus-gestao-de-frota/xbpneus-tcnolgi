from django.conf import settings
"""
Models para o módulo de Cargas
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class TipoCarga(models.Model):
    """Model TipoCarga"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='tipos_carga',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa à qual o tipo de carga pertence"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='tipos_carga',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial à qual o tipo de carga está associado"
    )
    # empresa = models.ForeignKey(
    #     on_delete=models.CASCADE,
    #     related_name='cargas_tipocarga',
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
        related_name='cargas_tipocarga_criado',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'TipoCarga'
        verbose_name_plural = 'TipoCargas'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class Carga(models.Model):
    """Model Carga"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='cargas',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa à qual a carga pertence"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='cargas',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial à qual a carga está associada"
    )
    # empresa = models.ForeignKey(
    #     on_delete=models.CASCADE,
    #     related_name='cargas_carga',
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
        related_name='cargas_carga_criado',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'Carga'
        verbose_name_plural = 'Cargas'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class ItemCarga(models.Model):
    """Model ItemCarga"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='itens_carga',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa à qual o item de carga pertence"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='itens_carga',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial à qual o item de carga está associado"
    )
    # empresa = models.ForeignKey(
    #     on_delete=models.CASCADE,
    #     related_name='cargas_itemcarga',
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
        related_name='cargas_itemcarga_criado',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'ItemCarga'
        verbose_name_plural = 'ItemCargas'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class ManifestoCarga(models.Model):
    """Model ManifestoCarga"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='manifestos_carga',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa à qual o manifesto de carga pertence"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='manifestos_carga',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial à qual o manifesto de carga está associado"
    )
    # empresa = models.ForeignKey(
    #     on_delete=models.CASCADE,
    #     related_name='cargas_manifestocarga',
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
        related_name='cargas_manifestocarga_criado',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'ManifestoCarga'
        verbose_name_plural = 'ManifestoCargas'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class RastreamentoCarga(models.Model):
    """Model RastreamentoCarga"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='rastreamentos_carga',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa à qual o rastreamento de carga pertence"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='rastreamentos_carga',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial à qual o rastreamento de carga está associado"
    )
    # empresa = models.ForeignKey(
    #     on_delete=models.CASCADE,
    #     related_name='cargas_rastreamentocarga',
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
        related_name='cargas_rastreamentocarga_criado',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'RastreamentoCarga'
        verbose_name_plural = 'RastreamentoCargas'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


