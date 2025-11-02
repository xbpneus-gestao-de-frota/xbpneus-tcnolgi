from django.db import models
from django.utils import timezone
from backend.transportador.frota.models import Vehicle


class CategoriaCusto(models.Model):
    """Categorias de custos operacionais"""
    TIPO_CHOICES = [
        ("FIXO", "Custo Fixo"),
        ("VARIAVEL", "Custo Variável"),
        ("OPERACIONAL", "Operacional"),
        ("ADMINISTRATIVO", "Administrativo"),
    ]
    
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descricao = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Categoria de Custo"
        verbose_name_plural = "Categorias de Custos"
        ordering = ["nome"]
    
    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"


class Custo(models.Model):
    """Registro de custos"""
    STATUS_CHOICES = [
        ("PENDENTE", "Pendente"),
        ("APROVADO", "Aprovado"),
        ("PAGO", "Pago"),
        ("CANCELADO", "Cancelado"),
    ]
    # empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='custos')
    categoria = models.ForeignKey(CategoriaCusto, on_delete=models.PROTECT, related_name='custos')
    veiculo = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name='custos')
    
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_custo = models.DateField(default=timezone.now)
    data_vencimento = models.DateField(blank=True, null=True)
    data_pagamento = models.DateField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    
    fornecedor = models.CharField(max_length=200, blank=True, null=True)
    numero_documento = models.CharField(max_length=50, blank=True, null=True)
    
    km_veiculo = models.IntegerField(blank=True, null=True, help_text='KM do veículo no momento do custo')
    
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    # criado_por = models.ForeignKey(
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     related_name='custos_criado',
    #     verbose_name='Criado por'
    # )
    
    class Meta:
        verbose_name = 'Custo'
        verbose_name_plural = 'Custos'
        ordering = ['-data_custo']
    
    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"
    
    def esta_vencido(self):
        """Verifica se custo está vencido"""
        from datetime import date
        if self.data_vencimento and self.status in ['PENDENTE', 'APROVADO']:
            return self.data_vencimento < date.today()
        return False


class CustoPorKm(models.Model):
    """Análise de custo por KM rodado"""
    veiculo = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='custos_km')
    
    mes_referencia = models.DateField()
    km_inicial = models.IntegerField()
    km_final = models.IntegerField()
    km_rodado = models.IntegerField()
    
    custo_total = models.DecimalField(max_digits=10, decimal_places=2)
    custo_por_km = models.DecimalField(max_digits=10, decimal_places=4)
    
    custo_combustivel = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    custo_manutencao = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    custo_pneus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    custo_outros = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    criado_em = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Custo por KM'
        verbose_name_plural = 'Custos por KM'
        ordering = ['-mes_referencia']
        unique_together = ['veiculo', 'mes_referencia']
    
    def __str__(self):
        return f"{self.veiculo.placa} - {self.mes_referencia.strftime('%m/%Y')} - R$ {self.custo_por_km}/km"
    
    def calcular(self):
        """Calcula custo por KM"""
        if self.km_rodado > 0:
            self.custo_por_km = self.custo_total / self.km_rodado
        return self.custo_por_km
