from django.db import models
from django.utils import timezone
from backend.transportador.empresas.models import Empresa
from backend.transportador.viagens.models import Viagem
from backend.transportador.clientes.models import Cliente


class Entrega(models.Model):
    """Entregas realizadas"""
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('EM_TRANSITO', 'Em Trânsito'),
        ('ENTREGUE', 'Entregue'),
        ('NAO_ENTREGUE', 'Não Entregue'),
        ('DEVOLVIDA', 'Devolvida'),
    ]
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='entregas')
    viagem = models.ForeignKey(Viagem, on_delete=models.PROTECT, related_name='entregas')
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='entregas')
    
    numero_entrega = models.CharField(max_length=100, unique=True)
    numero_nota_fiscal = models.CharField(max_length=50)
    
    destinatario_nome = models.CharField(max_length=200)
    destinatario_cpf_cnpj = models.CharField(max_length=18, blank=True, null=True)
    
    endereco_entrega = models.CharField(max_length=300)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=10)
    
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    
    data_prevista = models.DateTimeField()
    data_entrega = models.DateTimeField(blank=True, null=True)
    
    valor_mercadoria = models.DecimalField(max_digits=12, decimal_places=2)
    peso_kg = models.DecimalField(max_digits=10, decimal_places=2)
    volumes = models.IntegerField(default=1)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Entrega'
        verbose_name_plural = 'Entregas'
        ordering = ['-data_prevista']
    
    def __str__(self):
        return f"{self.numero_entrega} - {self.destinatario_nome}"
    
    def esta_atrasada(self):
        """Verifica se entrega está atrasada"""
        if self.status in ['ENTREGUE', 'NAO_ENTREGUE', 'DEVOLVIDA']:
            return False
        return timezone.now() > self.data_prevista


class POD(models.Model):
    """Proof of Delivery - Comprovante de Entrega"""
    entrega = models.OneToOneField(Entrega, on_delete=models.CASCADE, related_name='pod')
    
    recebedor_nome = models.CharField(max_length=200)
    recebedor_cpf = models.CharField(max_length=14, blank=True, null=True)
    recebedor_rg = models.CharField(max_length=20, blank=True, null=True)
    
    data_hora_recebimento = models.DateTimeField(default=timezone.now)
    
    assinatura_digital = models.ImageField(upload_to='pods/assinaturas/', blank=True, null=True)
    foto_comprovante = models.ImageField(upload_to='pods/fotos/', blank=True, null=True)
    
    latitude_entrega = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude_entrega = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'POD (Proof of Delivery)'
        verbose_name_plural = 'PODs (Proofs of Delivery)'
        ordering = ['-data_hora_recebimento']
    
    def __str__(self):
        return f"POD {self.entrega.numero_entrega} - {self.recebedor_nome}"


class Ocorrencia(models.Model):
    """Ocorrências durante a entrega"""
    TIPO_CHOICES = [
        ('ATRASO', 'Atraso'),
        ('RECUSA', 'Recusa'),
        ('ENDERECO_INCORRETO', 'Endereço Incorreto'),
        ('AUSENTE', 'Destinatário Ausente'),
        ('AVARIA', 'Avaria na Mercadoria'),
        ('EXTRAVIO', 'Extravio'),
        ('ROUBO', 'Roubo/Furto'),
        ('ACIDENTE', 'Acidente'),
        ('OUTRO', 'Outro'),
    ]
    
    entrega = models.ForeignKey(Entrega, on_delete=models.CASCADE, related_name='ocorrencias')
    
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    descricao = models.TextField()
    
    data_hora = models.DateTimeField(default=timezone.now)
    
    foto_ocorrencia = models.ImageField(upload_to='ocorrencias/', blank=True, null=True)
    
    responsavel = models.CharField(max_length=200, blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Ocorrência'
        verbose_name_plural = 'Ocorrências'
        ordering = ['-data_hora']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.entrega.numero_entrega}"


class Tentativa(models.Model):
    """Tentativas de entrega"""
    entrega = models.ForeignKey(Entrega, on_delete=models.CASCADE, related_name='tentativas')
    
    numero_tentativa = models.IntegerField()
    data_hora = models.DateTimeField(default=timezone.now)
    
    sucesso = models.BooleanField(default=False)
    motivo_falha = models.TextField(blank=True, null=True)
    
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Tentativa de Entrega'
        verbose_name_plural = 'Tentativas de Entrega'
        ordering = ['entrega', 'numero_tentativa']
        unique_together = ['entrega', 'numero_tentativa']
    
    def __str__(self):
        return f"Tentativa {self.numero_tentativa} - {self.entrega.numero_entrega}"
