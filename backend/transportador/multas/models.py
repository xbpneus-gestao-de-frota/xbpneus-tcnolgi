from django.db import models
from django.utils import timezone
from backend.transportador.empresas.models import Empresa
from backend.transportador.frota.models import Vehicle


class Multa(models.Model):
    """Multas de trânsito"""
    GRAVIDADE_CHOICES = [
        ('LEVE', 'Leve'),
        ('MEDIA', 'Média'),
        ('GRAVE', 'Grave'),
        ('GRAVISSIMA', 'Gravíssima'),
    ]
    
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('EM_RECURSO', 'Em Recurso'),
        ('DEFERIDA', 'Deferida'),
        ('INDEFERIDA', 'Indeferida'),
        ('PAGA', 'Paga'),
        ('CANCELADA', 'Cancelada'),
    ]
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='multas')
    veiculo = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='multas')
    
    numero_auto = models.CharField(max_length=50, unique=True)
    data_infracao = models.DateField()
    data_vencimento = models.DateField()
    
    codigo_infracao = models.CharField(max_length=20)
    descricao = models.TextField()
    gravidade = models.CharField(max_length=20, choices=GRAVIDADE_CHOICES)
    
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    valor_desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    pontos_cnh = models.IntegerField(default=0)
    
    local_infracao = models.CharField(max_length=200, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    
    motorista_nome = models.CharField(max_length=200, blank=True, null=True)
    motorista_cnh = models.CharField(max_length=20, blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    data_pagamento = models.DateField(blank=True, null=True)
    
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Multa'
        verbose_name_plural = 'Multas'
        ordering = ['-data_infracao']
    
    def __str__(self):
        return f"{self.numero_auto} - {self.veiculo.placa}"
    
    def esta_vencida(self):
        """Verifica se multa está vencida"""
        from datetime import date
        return self.data_vencimento < date.today() and self.status == 'PENDENTE'
    
    def valor_com_desconto(self):
        """Calcula valor com desconto"""
        return self.valor - self.valor_desconto


class RecursoMulta(models.Model):
    """Recursos de multas"""
    STATUS_CHOICES = [
        ('EM_ANALISE', 'Em Análise'),
        ('DEFERIDO', 'Deferido'),
        ('INDEFERIDO', 'Indeferido'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    multa = models.ForeignKey(Multa, on_delete=models.CASCADE, related_name='recursos')
    
    data_recurso = models.DateField(default=timezone.now)
    protocolo = models.CharField(max_length=50, blank=True, null=True)
    
    motivo = models.TextField()
    argumentacao = models.TextField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='EM_ANALISE')
    data_resposta = models.DateField(blank=True, null=True)
    resposta = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Recurso de Multa'
        verbose_name_plural = 'Recursos de Multas'
        ordering = ['-data_recurso']
    
    def __str__(self):
        return f"Recurso {self.protocolo} - {self.multa.numero_auto}"


class PontuacaoCNH(models.Model):
    """Controle de pontuação de CNH dos motoristas"""
    motorista_nome = models.CharField(max_length=200)
    motorista_cnh = models.CharField(max_length=20, unique=True)
    
    pontos_atuais = models.IntegerField(default=0)
    pontos_limite = models.IntegerField(default=20)
    
    data_ultima_atualizacao = models.DateField(auto_now=True)
    
    suspenso = models.BooleanField(default=False)
    data_suspensao = models.DateField(blank=True, null=True)
    
    observacoes = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Pontuação CNH'
        verbose_name_plural = 'Pontuações CNH'
        ordering = ['-pontos_atuais']
    
    def __str__(self):
        return f"{self.motorista_nome} - {self.pontos_atuais} pontos"
    
    def em_risco(self):
        """Verifica se está próximo do limite"""
        return self.pontos_atuais >= (self.pontos_limite * 0.8)
