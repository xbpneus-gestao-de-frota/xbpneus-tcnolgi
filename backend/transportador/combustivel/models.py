from django.db import models
from django.utils import timezone
from backend.transportador.frota.models import Vehicle


class PostoCombustivel(models.Model):
    """Postos de combustível cadastrados"""
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='postos_combustivel',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa à qual o posto de combustível pertence"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='postos_combustivel',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial à qual o posto de combustível está associado"
    )
    nome = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=18, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    ativo = models.BooleanField(default=True)
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Posto de Combustível'
        verbose_name_plural = 'Postos de Combustível'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class Abastecimento(models.Model):
    """Registro de abastecimentos"""
    TIPO_COMBUSTIVEL_CHOICES = [
        ('DIESEL_S10', 'Diesel S10'),
        ('DIESEL_S500', 'Diesel S500'),
        ('DIESEL_ADITIVADO', 'Diesel Aditivado'),
        ('ARLA32', 'Arla 32'),
        ('GASOLINA', 'Gasolina'),
        ('ETANOL', 'Etanol'),
    ]
    
    FORMA_PAGAMENTO_CHOICES = [
        ('DINHEIRO', 'Dinheiro'),
        ('CARTAO', 'Cartão'),
        ('VALE', 'Vale Combustível'),
        ('FATURADO', 'Faturado'),
    ]
    
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='abastecimentos',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa à qual o abastecimento pertence"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='abastecimentos',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial à qual o abastecimento está associado"
    )
    veiculo = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='abastecimentos')
    posto = models.ForeignKey(PostoCombustivel, on_delete=models.SET_NULL, null=True, blank=True, related_name='abastecimentos')
    data_abastecimento = models.DateTimeField(default=timezone.now)
    tipo_combustivel = models.CharField(max_length=30, choices=TIPO_COMBUSTIVEL_CHOICES)
    
    # Dados do abastecimento
    litros = models.DecimalField(max_digits=10, decimal_places=3)
    preco_litro = models.DecimalField(max_digits=10, decimal_places=3)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Dados do veículo
    km_veiculo = models.IntegerField()
    km_desde_ultimo = models.IntegerField(blank=True, null=True)
    
    # Consumo
    consumo_medio = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text='KM/L')
    
    # Pagamento
    forma_pagamento = models.CharField(max_length=20, choices=FORMA_PAGAMENTO_CHOICES)
    numero_nota = models.CharField(max_length=50, blank=True, null=True)
    
    # Localização
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    
    # Motorista
    motorista_nome = models.CharField(max_length=200, blank=True, null=True)
    
    tanque_cheio = models.BooleanField(default=True)
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Abastecimento'
        verbose_name_plural = 'Abastecimentos'
        ordering = ['-data_abastecimento']
    
    def __str__(self):
        return f"{self.veiculo.placa} - {self.litros}L - {self.data_abastecimento.strftime('%d/%m/%Y')}"
    
    def calcular_consumo(self):
        """Calcula consumo médio"""
        if self.km_desde_ultimo and self.litros > 0:
            self.consumo_medio = self.km_desde_ultimo / self.litros
        return self.consumo_medio
    
    def save(self, *args, **kwargs):
        # Calcular valor total
        self.valor_total = self.litros * self.preco_litro
        
        # Calcular KM desde último abastecimento
        ultimo = Abastecimento.objects.filter(
            veiculo=self.veiculo,
            data_abastecimento__lt=self.data_abastecimento
        ).order_by('-data_abastecimento').first()
        
        if ultimo:
            self.km_desde_ultimo = self.km_veiculo - ultimo.km_veiculo
            self.calcular_consumo()
        
        super().save(*args, **kwargs)


class ConsumoMensal(models.Model):
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='consumos_mensais',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa à qual o consumo mensal pertence"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='consumos_mensais',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial à qual o consumo mensal está associado"
    )
    """Análise de consumo mensal por veículo"""
    veiculo = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='consumo_mensal')
    
    mes_referencia = models.DateField()
    
    total_litros = models.DecimalField(max_digits=10, decimal_places=2)
    total_valor = models.DecimalField(max_digits=10, decimal_places=2)
    km_rodado = models.IntegerField()
    
    consumo_medio = models.DecimalField(max_digits=5, decimal_places=2, help_text='KM/L')
    custo_por_km = models.DecimalField(max_digits=10, decimal_places=4)
    
    numero_abastecimentos = models.IntegerField(default=0)
    
    criado_em = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Consumo Mensal'
        verbose_name_plural = 'Consumos Mensais'
        ordering = ['-mes_referencia']
        unique_together = ['veiculo', 'mes_referencia']
    
    def __str__(self):
        return f"{self.veiculo.placa} - {self.mes_referencia.strftime('%m/%Y')}"
