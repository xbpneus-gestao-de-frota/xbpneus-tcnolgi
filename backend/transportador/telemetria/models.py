from django.db import models
from django.utils import timezone
from backend.transportador.empresas.models import Empresa
from backend.transportador.frota.models import Vehicle


class Dispositivo(models.Model):
    """Dispositivos de telemetria instalados"""
    TIPO_CHOICES = [
        ('GPS', 'GPS'),
        ('SENSOR_TEMPERATURA', 'Sensor de Temperatura'),
        ('SENSOR_PRESSAO', 'Sensor de Pressão'),
        ('TACOGRAFO', 'Tacógrafo'),
        ('CAMERA', 'Câmera'),
        ('SENSOR_COMBUSTIVEL', 'Sensor de Combustível'),
        ('OBD', 'OBD-II'),
        ('OUTRO', 'Outro'),
    ]
    
    STATUS_CHOICES = [
        ('ATIVO', 'Ativo'),
        ('INATIVO', 'Inativo'),
        ('MANUTENCAO', 'Manutenção'),
        ('DEFEITO', 'Defeito'),
    ]
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='dispositivos')
    veiculo = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='dispositivos')
    
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    fabricante = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    numero_serie = models.CharField(max_length=100, unique=True)
    
    data_instalacao = models.DateField(default=timezone.now)
    data_ultima_leitura = models.DateTimeField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ATIVO')
    
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Dispositivo'
        verbose_name_plural = 'Dispositivos'
        ordering = ['veiculo', 'tipo']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.veiculo.placa}"


class Leitura(models.Model):
    """Leituras dos dispositivos"""
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, related_name='leituras')
    
    data_hora = models.DateTimeField(default=timezone.now, db_index=True)
    
    # Dados gerais
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    velocidade = models.IntegerField(blank=True, null=True, help_text='Velocidade em km/h')
    
    # Sensores
    temperatura = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text='Temperatura em °C')
    pressao = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text='Pressão em PSI')
    nivel_combustivel = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text='Nível em %')
    
    # OBD
    rpm = models.IntegerField(blank=True, null=True)
    hodometro = models.IntegerField(blank=True, null=True, help_text='KM total')
    
    # JSON para dados adicionais
    dados_json = models.JSONField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Leitura'
        verbose_name_plural = 'Leituras'
        ordering = ['-data_hora']
        indexes = [
            models.Index(fields=['dispositivo', '-data_hora']),
        ]
    
    def __str__(self):
        return f"{self.dispositivo} - {self.data_hora}"


class Alerta(models.Model):
    """Alertas gerados pela telemetria"""
    TIPO_CHOICES = [
        ('EXCESSO_VELOCIDADE', 'Excesso de Velocidade'),
        ('TEMPERATURA_ALTA', 'Temperatura Alta'),
        ('PRESSAO_BAIXA', 'Pressão Baixa'),
        ('COMBUSTIVEL_BAIXO', 'Combustível Baixo'),
        ('MANUTENCAO', 'Manutenção Necessária'),
        ('CERCA_VIOLADA', 'Cerca Eletrônica Violada'),
        ('DISPOSITIVO_OFFLINE', 'Dispositivo Offline'),
        ('OUTRO', 'Outro'),
    ]
    
    SEVERIDADE_CHOICES = [
        ('BAIXA', 'Baixa'),
        ('MEDIA', 'Média'),
        ('ALTA', 'Alta'),
        ('CRITICA', 'Crítica'),
    ]
    
    STATUS_CHOICES = [
        ('ABERTO', 'Aberto'),
        ('RECONHECIDO', 'Reconhecido'),
        ('RESOLVIDO', 'Resolvido'),
        ('IGNORADO', 'Ignorado'),
    ]
    
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, related_name='alertas')
    leitura = models.ForeignKey(Leitura, on_delete=models.SET_NULL, null=True, blank=True, related_name='alertas')
    
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    severidade = models.CharField(max_length=10, choices=SEVERIDADE_CHOICES)
    
    mensagem = models.TextField()
    
    data_hora = models.DateTimeField(default=timezone.now)
    data_reconhecimento = models.DateTimeField(blank=True, null=True)
    data_resolucao = models.DateTimeField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ABERTO')
    
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Alerta'
        verbose_name_plural = 'Alertas'
        ordering = ['-data_hora']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.dispositivo.veiculo.placa}"
