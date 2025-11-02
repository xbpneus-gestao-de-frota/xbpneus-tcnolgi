from django.db import models
from django.utils import timezone
from backend.transportador.empresas.models import Empresa
from backend.transportador.frota.models import Vehicle


class Rota(models.Model):
    """Rotas planejadas"""
    STATUS_CHOICES = [
        ('PLANEJADA', 'Planejada'),
        ('EM_ANDAMENTO', 'Em Andamento'),
        ('CONCLUIDA', 'Concluída'),
        ('CANCELADA', 'Cancelada'),
    ]
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='rotas')
    veiculo = models.ForeignKey(Vehicle, on_delete=models.PROTECT, null=True, blank=True, related_name='rotas')
    
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    
    origem = models.CharField(max_length=200)
    destino = models.CharField(max_length=200)
    
    distancia_km = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tempo_estimado_minutos = models.IntegerField(blank=True, null=True)
    
    data_inicio_prevista = models.DateTimeField()
    data_fim_prevista = models.DateTimeField()
    
    data_inicio_real = models.DateTimeField(blank=True, null=True)
    data_fim_real = models.DateTimeField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANEJADA')
    
    # Custos
    custo_combustivel_estimado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    custo_pedagio_estimado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    custo_total_estimado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Rota'
        verbose_name_plural = 'Rotas'
        ordering = ['-data_inicio_prevista']
    
    def __str__(self):
        return f"{self.nome} - {self.origem} → {self.destino}"
    
    def calcular_custo_total(self):
        """Calcula custo total estimado"""
        self.custo_total_estimado = self.custo_combustivel_estimado + self.custo_pedagio_estimado
        return self.custo_total_estimado


class PontoRota(models.Model):
    """Pontos de parada na rota"""
    TIPO_CHOICES = [
        ('ORIGEM', 'Origem'),
        ('PARADA', 'Parada'),
        ('DESTINO', 'Destino'),
        ('PEDAGIO', 'Pedágio'),
        ('POSTO', 'Posto de Combustível'),
        ('DESCANSO', 'Ponto de Descanso'),
    ]
    
    rota = models.ForeignKey(Rota, on_delete=models.CASCADE, related_name='pontos')
    
    ordem = models.IntegerField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    
    nome = models.CharField(max_length=200)
    endereco = models.CharField(max_length=300)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    
    tempo_parada_minutos = models.IntegerField(default=0)
    
    chegada_prevista = models.DateTimeField(blank=True, null=True)
    chegada_real = models.DateTimeField(blank=True, null=True)
    
    saida_prevista = models.DateTimeField(blank=True, null=True)
    saida_real = models.DateTimeField(blank=True, null=True)
    
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Ponto da Rota'
        verbose_name_plural = 'Pontos da Rota'
        ordering = ['rota', 'ordem']
        unique_together = ['rota', 'ordem']
    
    def __str__(self):
        return f"{self.rota.nome} - {self.ordem}. {self.nome}"


class RotaOtimizada(models.Model):
    """Rotas otimizadas por algoritmo"""
    rota_original = models.ForeignKey(Rota, on_delete=models.CASCADE, related_name='otimizacoes')
    
    algoritmo = models.CharField(max_length=50, help_text='Algoritmo utilizado (ex: Dijkstra, A*)')
    
    distancia_km = models.DecimalField(max_digits=10, decimal_places=2)
    tempo_estimado_minutos = models.IntegerField()
    custo_estimado = models.DecimalField(max_digits=10, decimal_places=2)
    
    economia_distancia_km = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    economia_tempo_minutos = models.IntegerField(default=0)
    economia_custo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # JSON com sequência otimizada de pontos
    sequencia_pontos_json = models.JSONField()
    
    # JSON com dados do algoritmo
    detalhes_json = models.JSONField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Rota Otimizada'
        verbose_name_plural = 'Rotas Otimizadas'
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"Otimização {self.algoritmo} - {self.rota_original.nome}"
