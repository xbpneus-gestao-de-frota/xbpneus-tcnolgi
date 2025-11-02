from django.db import models
from django.utils import timezone
from backend.transportador.empresas.models import Empresa
from backend.transportador.clientes.models import Cliente
from backend.transportador.viagens.models import Viagem


class Fatura(models.Model):
    """Faturas emitidas"""
    STATUS_CHOICES = [
        ('RASCUNHO', 'Rascunho'),
        ('EMITIDA', 'Emitida'),
        ('ENVIADA', 'Enviada'),
        ('PAGA', 'Paga'),
        ('VENCIDA', 'Vencida'),
        ('CANCELADA', 'Cancelada'),
    ]
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='faturas')
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='faturas')
    viagem = models.ForeignKey(Viagem, on_delete=models.SET_NULL, null=True, blank=True, related_name='faturas')
    
    numero_fatura = models.CharField(max_length=100, unique=True)
    
    data_emissao = models.DateField(default=timezone.now)
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(blank=True, null=True)
    
    valor_bruto = models.DecimalField(max_digits=12, decimal_places=2)
    valor_desconto = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    valor_acrescimo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    valor_liquido = models.DecimalField(max_digits=12, decimal_places=2)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RASCUNHO')
    
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Fatura'
        verbose_name_plural = 'Faturas'
        ordering = ['-data_emissao']
    
    def __str__(self):
        return f"{self.numero_fatura} - {self.cliente.nome_razao_social}"
    
    def calcular_valor_liquido(self):
        """Calcula valor líquido"""
        self.valor_liquido = self.valor_bruto - self.valor_desconto + self.valor_acrescimo
        return self.valor_liquido
    
    def dias_ate_vencimento(self):
        """Calcula dias até vencimento"""
        from datetime import date
        delta = self.data_vencimento - date.today()
        return delta.days
    
    def esta_vencida(self):
        """Verifica se fatura está vencida"""
        return self.dias_ate_vencimento() < 0 and self.status not in ['PAGA', 'CANCELADA']


class ItemFatura(models.Model):
    """Itens da fatura"""
    fatura = models.ForeignKey(Fatura, on_delete=models.CASCADE, related_name='itens')
    
    descricao = models.CharField(max_length=200)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)
    
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Item da Fatura'
        verbose_name_plural = 'Itens da Fatura'
        ordering = ['fatura', 'id']
    
    def __str__(self):
        return f"{self.descricao} - {self.fatura.numero_fatura}"
    
    def calcular_valor_total(self):
        """Calcula valor total do item"""
        self.valor_total = self.quantidade * self.valor_unitario
        return self.valor_total


class NotaFiscal(models.Model):
    """Notas fiscais emitidas"""
    TIPO_CHOICES = [
        ('NFE', 'NF-e'),
        ('NFSE', 'NFS-e'),
        ('CTE', 'CT-e'),
    ]
    
    STATUS_CHOICES = [
        ('RASCUNHO', 'Rascunho'),
        ('AUTORIZADA', 'Autorizada'),
        ('CANCELADA', 'Cancelada'),
        ('DENEGADA', 'Denegada'),
    ]
    
    fatura = models.ForeignKey(Fatura, on_delete=models.PROTECT, related_name='notas_fiscais')
    
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    numero = models.CharField(max_length=50)
    serie = models.CharField(max_length=10)
    chave_acesso = models.CharField(max_length=44, unique=True, blank=True, null=True)
    
    data_emissao = models.DateTimeField(default=timezone.now)
    data_autorizacao = models.DateTimeField(blank=True, null=True)
    
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RASCUNHO')
    
    protocolo_autorizacao = models.CharField(max_length=50, blank=True, null=True)
    
    xml_nfe = models.TextField(blank=True, null=True)
    pdf_danfe = models.FileField(upload_to='notas_fiscais/', blank=True, null=True)
    
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Nota Fiscal'
        verbose_name_plural = 'Notas Fiscais'
        ordering = ['-data_emissao']
        unique_together = ['numero', 'serie']
    
    def __str__(self):
        return f"{self.get_tipo_display()} {self.numero}/{self.serie}"
