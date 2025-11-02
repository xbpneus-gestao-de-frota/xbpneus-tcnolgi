from django.db import models
from django.utils import timezone
from backend.transportador.empresas.models import Empresa
from backend.transportador.frota.models import Vehicle


class Posicao(models.Model):
    """Posições GPS dos veículos"""
    veiculo = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='posicoes')
    
    data_hora = models.DateTimeField(default=timezone.now, db_index=True)
    
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    
    velocidade = models.IntegerField(default=0, help_text='Velocidade em km/h')
    direcao = models.IntegerField(blank=True, null=True, help_text='Direção em graus (0-360)')
    
    altitude = models.IntegerField(blank=True, null=True, help_text='Altitude em metros')
    precisao = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text='Precisão em metros')
    
    ignicao_ligada = models.BooleanField(default=False)
    
    endereco = models.CharField(max_length=300, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Posição GPS'
        verbose_name_plural = 'Posições GPS'
        ordering = ['-data_hora']
        indexes = [
            models.Index(fields=['veiculo', '-data_hora']),
        ]
    
    def __str__(self):
        return f"{self.veiculo.placa} - {self.data_hora}"


class CercaEletronica(models.Model):
    """Cercas eletrônicas (geofencing)"""
    TIPO_CHOICES = [
        ('CIRCULAR', 'Circular'),
        ('POLIGONAL', 'Poligonal'),
        ('ROTA', 'Rota'),
    ]
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='cercas')
    
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    
    # Para cercas circulares
    latitude_centro = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude_centro = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    raio = models.IntegerField(blank=True, null=True, help_text='Raio em metros')
    
    # Para cercas poligonais (JSON com array de coordenadas)
    coordenadas_json = models.JSONField(blank=True, null=True)
    
    ativa = models.BooleanField(default=True)
    
    # Alertas
    alertar_entrada = models.BooleanField(default=False)
    alertar_saida = models.BooleanField(default=False)
    
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Cerca Eletrônica'
        verbose_name_plural = 'Cercas Eletrônicas'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class ViolacaoCerca(models.Model):
    """Violações de cerca eletrônica"""
    TIPO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SAIDA', 'Saída'),
    ]
    
    STATUS_CHOICES = [
        ('ABERTO', 'Aberto'),
        ('RECONHECIDO', 'Reconhecido'),
        ('RESOLVIDO', 'Resolvido'),
        ('IGNORADO', 'Ignorado'),
    ]
    
    cerca = models.ForeignKey(CercaEletronica, on_delete=models.CASCADE, related_name='violacoes')
    veiculo = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='violacoes_cerca')
    posicao = models.ForeignKey(Posicao, on_delete=models.SET_NULL, null=True, blank=True, related_name='violacoes')
    
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    
    data_hora = models.DateTimeField(default=timezone.now)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ABERTO')
    
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Violação de Cerca'
        verbose_name_plural = 'Violações de Cercas'
        ordering = ['-data_hora']
    
    def __str__(self):
        return f"{self.veiculo.placa} - {self.get_tipo_display()} {self.cerca.nome}"


class HistoricoRastreamento(models.Model):
    """Histórico consolidado de rastreamento"""
    veiculo = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='historico_rastreamento')
    
    data = models.DateField(db_index=True)
    
    km_percorrido = models.IntegerField(default=0)
    tempo_movimento = models.IntegerField(default=0, help_text='Tempo em movimento (minutos)')
    tempo_parado = models.IntegerField(default=0, help_text='Tempo parado (minutos)')
    
    velocidade_maxima = models.IntegerField(default=0)
    velocidade_media = models.IntegerField(default=0)
    
    numero_paradas = models.IntegerField(default=0)
    
    criado_em = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Histórico de Rastreamento'
        verbose_name_plural = 'Históricos de Rastreamento'
        ordering = ['-data']
        unique_together = ['veiculo', 'data']
    
    def __str__(self):
        return f"{self.veiculo.placa} - {self.data}"
