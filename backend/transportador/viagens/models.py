from django.db import models
from django.utils import timezone
from backend.transportador.empresas.models import Empresa
from backend.transportador.frota.models import Vehicle


class Viagem(models.Model):
    """Viagens realizadas pelos veículos"""
    STATUS_CHOICES = [
        ('PLANEJADA', 'Planejada'),
        ('EM_ANDAMENTO', 'Em Andamento'),
        ('CONCLUIDA', 'Concluída'),
        ('CANCELADA', 'Cancelada'),
    ]
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='viagens')
    veiculo = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='viagens')
    
    numero_viagem = models.CharField(max_length=50, unique=True)
    
    origem = models.CharField(max_length=200)
    destino = models.CharField(max_length=200)
    
    data_saida_prevista = models.DateTimeField()
    data_chegada_prevista = models.DateTimeField()
    
    data_saida_real = models.DateTimeField(blank=True, null=True)
    data_chegada_real = models.DateTimeField(blank=True, null=True)
    
    km_inicial = models.IntegerField()
    km_final = models.IntegerField(blank=True, null=True)
    km_percorrido = models.IntegerField(blank=True, null=True)
    
    motorista_nome = models.CharField(max_length=200)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANEJADA')
    
    valor_frete = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    despesas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Viagem'
        verbose_name_plural = 'Viagens'
        ordering = ['-data_saida_prevista']
    
    def __str__(self):
        return f"{self.numero_viagem} - {self.origem} → {self.destino}"
    
    def calcular_km(self):
        """Calcula KM percorrido"""
        if self.km_final:
            self.km_percorrido = self.km_final - self.km_inicial
        return self.km_percorrido
    
    def lucro(self):
        """Calcula lucro da viagem"""
        return self.valor_frete - self.despesas


class Carga(models.Model):
    """Cargas transportadas nas viagens"""
    viagem = models.ForeignKey(Viagem, on_delete=models.CASCADE, related_name='cargas')
    
    descricao = models.CharField(max_length=200)
    peso = models.DecimalField(max_digits=10, decimal_places=2, help_text='Peso em kg')
    volume = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text='Volume em m³')
    
    numero_nota_fiscal = models.CharField(max_length=50, blank=True, null=True)
    valor_mercadoria = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    cliente_nome = models.CharField(max_length=200)
    cliente_cpf_cnpj = models.CharField(max_length=18, blank=True, null=True)
    
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Carga'
        verbose_name_plural = 'Cargas'
        ordering = ['viagem', 'id']
    
    def __str__(self):
        return f"{self.descricao} - {self.peso}kg"


class Parada(models.Model):
    """Paradas durante a viagem"""
    TIPO_CHOICES = [
        ('ABASTECIMENTO', 'Abastecimento'),
        ('DESCANSO', 'Descanso'),
        ('REFEICAO', 'Refeição'),
        ('MANUTENCAO', 'Manutenção'),
        ('CARGA', 'Carga'),
        ('DESCARGA', 'Descarga'),
        ('FISCALIZACAO', 'Fiscalização'),
        ('OUTRO', 'Outro'),
    ]
    
    viagem = models.ForeignKey(Viagem, on_delete=models.CASCADE, related_name='paradas')
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    local = models.CharField(max_length=200)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    
    data_hora_entrada = models.DateTimeField()
    data_hora_saida = models.DateTimeField(blank=True, null=True)
    
    duracao_minutos = models.IntegerField(blank=True, null=True)
    
    km_veiculo = models.IntegerField(blank=True, null=True)
    
    valor_gasto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Parada'
        verbose_name_plural = 'Paradas'
        ordering = ['viagem', 'data_hora_entrada']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.local}"
    
    def calcular_duracao(self):
        """Calcula duração da parada em minutos"""
        if self.data_hora_saida:
            delta = self.data_hora_saida - self.data_hora_entrada
            self.duracao_minutos = int(delta.total_seconds() / 60)
        return self.duracao_minutos
