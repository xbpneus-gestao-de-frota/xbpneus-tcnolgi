from django.db import models
from django.utils import timezone
from backend.transportador.empresas.models import Empresa
from backend.transportador.fornecedores.models import Fornecedor
from backend.transportador.clientes.models import Cliente


class ContaPagar(models.Model):
    """Contas a pagar"""
    TIPO_CHOICES = [
        ('FORNECEDOR', 'Fornecedor'),
        ('SALARIO', 'Salário'),
        ('IMPOSTO', 'Imposto'),
        ('ALUGUEL', 'Aluguel'),
        ('COMBUSTIVEL', 'Combustível'),
        ('MANUTENCAO', 'Manutenção'),
        ('SEGURO', 'Seguro'),
        ('OUTRO', 'Outro'),
    ]
    
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('PAGA', 'Paga'),
        ('VENCIDA', 'Vencida'),
        ('CANCELADA', 'Cancelada'),
    ]
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='contas_pagar')
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, null=True, blank=True, related_name='contas_pagar')
    
    numero_documento = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    
    descricao = models.CharField(max_length=200)
    
    data_emissao = models.DateField(default=timezone.now)
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(blank=True, null=True)
    
    valor_original = models.DecimalField(max_digits=12, decimal_places=2)
    valor_desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_juros = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_pago = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Conta a Pagar'
        verbose_name_plural = 'Contas a Pagar'
        ordering = ['data_vencimento']
    
    def __str__(self):
        return f"{self.numero_documento} - {self.descricao}"
    
    def valor_total(self):
        """Calcula valor total (original - desconto + juros)"""
        return self.valor_original - self.valor_desconto + self.valor_juros
    
    def dias_ate_vencimento(self):
        """Calcula dias até vencimento"""
        from datetime import date
        delta = self.data_vencimento - date.today()
        return delta.days
    
    def esta_vencida(self):
        """Verifica se está vencida"""
        return self.dias_ate_vencimento() < 0 and self.status == 'PENDENTE'


class ContaReceber(models.Model):
    """Contas a receber"""
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('RECEBIDA', 'Recebida'),
        ('VENCIDA', 'Vencida'),
        ('CANCELADA', 'Cancelada'),
    ]
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='contas_receber')
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='contas_receber')
    
    numero_documento = models.CharField(max_length=100)
    
    descricao = models.CharField(max_length=200)
    
    data_emissao = models.DateField(default=timezone.now)
    data_vencimento = models.DateField()
    data_recebimento = models.DateField(blank=True, null=True)
    
    valor_original = models.DecimalField(max_digits=12, decimal_places=2)
    valor_desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_juros = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_recebido = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Conta a Receber'
        verbose_name_plural = 'Contas a Receber'
        ordering = ['data_vencimento']
    
    def __str__(self):
        return f"{self.numero_documento} - {self.cliente.nome_razao_social}"
    
    def valor_total(self):
        """Calcula valor total (original - desconto + juros)"""
        return self.valor_original - self.valor_desconto + self.valor_juros
    
    def dias_ate_vencimento(self):
        """Calcula dias até vencimento"""
        from datetime import date
        delta = self.data_vencimento - date.today()
        return delta.days
    
    def esta_vencida(self):
        """Verifica se está vencida"""
        return self.dias_ate_vencimento() < 0 and self.status == 'PENDENTE'


class Pagamento(models.Model):
    """Pagamentos realizados"""
    FORMA_CHOICES = [
        ('DINHEIRO', 'Dinheiro'),
        ('PIX', 'PIX'),
        ('TED', 'TED'),
        ('BOLETO', 'Boleto'),
        ('CARTAO_CREDITO', 'Cartão de Crédito'),
        ('CARTAO_DEBITO', 'Cartão de Débito'),
        ('CHEQUE', 'Cheque'),
    ]
    
    conta_pagar = models.ForeignKey(ContaPagar, on_delete=models.CASCADE, null=True, blank=True, related_name='pagamentos')
    conta_receber = models.ForeignKey(ContaReceber, on_delete=models.CASCADE, null=True, blank=True, related_name='recebimentos')
    
    data_pagamento = models.DateField(default=timezone.now)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    
    forma_pagamento = models.CharField(max_length=20, choices=FORMA_CHOICES)
    
    comprovante = models.FileField(upload_to='pagamentos/', blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['-data_pagamento']
    
    def __str__(self):
        if self.conta_pagar:
            return f"Pagamento {self.conta_pagar.numero_documento}"
        return f"Recebimento {self.conta_receber.numero_documento}"
