from django.db import models
from django.utils import timezone
from backend.transportador.empresas.models import Empresa
from backend.transportador.frota.models import Vehicle


class Seguradora(models.Model):
    """Seguradoras cadastradas"""
    nome = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=18, unique=True)
    
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    site = models.URLField(blank=True, null=True)
    
    ativo = models.BooleanField(default=True)
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Seguradora'
        verbose_name_plural = 'Seguradoras'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class Apolice(models.Model):
    """Apólices de seguro"""
    TIPO_CHOICES = [
        ('FROTA', 'Seguro de Frota'),
        ('CARGA', 'Seguro de Carga'),
        ('RCFDC', 'RCFDC'),
        ('RCF', 'RCF'),
        ('VIDA', 'Seguro de Vida'),
        ('OUTRO', 'Outro'),
    ]
    
    STATUS_CHOICES = [
        ('ATIVA', 'Ativa'),
        ('VENCIDA', 'Vencida'),
        ('CANCELADA', 'Cancelada'),
        ('RENOVADA', 'Renovada'),
    ]
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='apolices')
    seguradora = models.ForeignKey(Seguradora, on_delete=models.PROTECT, related_name='apolices')
    veiculo = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name='apolices')
    
    numero_apolice = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    
    data_inicio = models.DateField()
    data_fim = models.DateField()
    
    valor_premio = models.DecimalField(max_digits=12, decimal_places=2)
    valor_cobertura = models.DecimalField(max_digits=12, decimal_places=2)
    franquia = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ATIVA')
    
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Apólice'
        verbose_name_plural = 'Apólices'
        ordering = ['-data_inicio']
    
    def __str__(self):
        return f"{self.numero_apolice} - {self.get_tipo_display()}"
    
    def dias_para_vencer(self):
        """Calcula dias até vencimento"""
        from datetime import date
        delta = self.data_fim - date.today()
        return delta.days
    
    def esta_vencida(self):
        """Verifica se apólice está vencida"""
        return self.dias_para_vencer() < 0
    
    def esta_vencendo(self):
        """Verifica se apólice está vencendo em 30 dias"""
        dias = self.dias_para_vencer()
        return 0 <= dias <= 30


class Sinistro(models.Model):
    """Sinistros ocorridos"""
    TIPO_CHOICES = [
        ('COLISAO', 'Colisão'),
        ('ROUBO', 'Roubo/Furto'),
        ('INCENDIO', 'Incêndio'),
        ('DANOS_CARGA', 'Danos à Carga'),
        ('TERCEIROS', 'Danos a Terceiros'),
        ('OUTRO', 'Outro'),
    ]
    
    STATUS_CHOICES = [
        ('ABERTO', 'Aberto'),
        ('EM_ANALISE', 'Em Análise'),
        ('APROVADO', 'Aprovado'),
        ('NEGADO', 'Negado'),
        ('PAGO', 'Pago'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    apolice = models.ForeignKey(Apolice, on_delete=models.PROTECT, related_name='sinistros')
    
    numero_sinistro = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    
    data_ocorrencia = models.DateTimeField()
    data_abertura = models.DateField(default=timezone.now)
    
    local_ocorrencia = models.CharField(max_length=200)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    
    descricao = models.TextField()
    
    valor_estimado = models.DecimalField(max_digits=12, decimal_places=2)
    valor_aprovado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    valor_franquia = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ABERTO')
    
    boletim_ocorrencia = models.CharField(max_length=50, blank=True, null=True)
    
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Sinistro'
        verbose_name_plural = 'Sinistros'
        ordering = ['-data_ocorrencia']
    
    def __str__(self):
        return f"{self.numero_sinistro} - {self.get_tipo_display()}"
    
    def valor_liquido(self):
        """Calcula valor líquido (aprovado - franquia)"""
        return self.valor_aprovado - self.valor_franquia
