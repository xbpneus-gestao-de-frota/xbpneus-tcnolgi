from django.db import models
from django.utils import timezone
from backend.transportador.clientes.models import Cliente
from backend.transportador.fornecedores.models import Fornecedor


class Contrato(models.Model):
    """Contratos comerciais"""
    TIPO_CHOICES = [
        ("PRESTACAO_SERVICO", "Prestação de Serviço"),
        ("FORNECIMENTO", "Fornecimento"),
        ("LOCACAO", "Locação"),
        ("PARCERIA", "Parceria"),
        ("OUTRO", "Outro"),
    ]
    
    STATUS_CHOICES = [
        ("RASCUNHO", "Rascunho"),
        ("ATIVO", "Ativo"),
        ("SUSPENSO", "Suspenso"),
        ("VENCIDO", "Vencido"),
        ("CANCELADO", "Cancelado"),
        ("RENOVADO", "Renovado"),
    ]
    
    # empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='contratos')
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, related_name='contratos')
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, blank=True, related_name='contratos')
    
    numero_contrato = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    
    data_inicio = models.DateField()
    data_fim = models.DateField()
    
    valor_mensal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)
    
    renovacao_automatica = models.BooleanField(default=False)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RASCUNHO')
    
    arquivo = models.FileField(upload_to='contratos/', blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    # criado_por = models.ForeignKey(
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     related_name='contratos_criado',
    #     verbose_name='Criado por'
    # )
    
    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'
        ordering = ['-data_inicio']
    
    def __str__(self):
        return f"{self.numero_contrato} - {self.titulo}"
    
    def dias_para_vencer(self):
        """Calcula dias até vencimento"""
        from datetime import date
        delta = self.data_fim - date.today()
        return delta.days
    
    def esta_vencido(self):
        """Verifica se contrato está vencido"""
        return self.dias_para_vencer() < 0
    
    def esta_vencendo(self):
        """Verifica se contrato está vencendo em 60 dias"""
        dias = self.dias_para_vencer()
        return 0 <= dias <= 60


class Aditivo(models.Model):
    """Aditivos contratuais"""
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name='aditivos')
    
    numero_aditivo = models.CharField(max_length=50)
    data_aditivo = models.DateField(default=timezone.now)
    
    descricao = models.TextField()
    
    alteracao_valor = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    alteracao_prazo_dias = models.IntegerField(default=0)
    
    arquivo = models.FileField(upload_to='contratos/aditivos/', blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Aditivo Contratual'
        verbose_name_plural = 'Aditivos Contratuais'
        ordering = ['-data_aditivo']
    
    def __str__(self):
        return f"Aditivo {self.numero_aditivo} - {self.contrato.numero_contrato}"
