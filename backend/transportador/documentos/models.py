from django.db import models
from django.utils import timezone
from backend.transportador.frota.models import Vehicle


class Documento(models.Model):
    """Documentos de veículos e motoristas"""
    TIPO_CHOICES = [
        ("CRLV", "CRLV"),
        ("CNH", "CNH"),
        ("ANTT", "ANTT"),
        ("SEGURO", "Seguro"),
        ("LICENCA_AMBIENTAL", "Licença Ambiental"),
        ("CERTIFICADO_TACOGRAFO", "Certificado Tacógrafo"),
        ("ALVARA", "Alvará"),
        ("OUTRO", "Outro"),
    ]
    
    STATUS_CHOICES = [
        ("ATIVO", "Ativo"),
        ("VENCIDO", "Vencido"),
        ("VENCENDO", "Vencendo"),
        ("RENOVADO", "Renovado"),
        ("CANCELADO", "Cancelado"),
    ]
       # empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='documentos')
    veiculo = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True, blank=True, related_name='documentos')
    
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    numero = models.CharField(max_length=100)
    orgao_emissor = models.CharField(max_length=100, blank=True, null=True)
    
    data_emissao = models.DateField()
    data_validade = models.DateField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ATIVO')
    
    arquivo = models.FileField(upload_to='documentos/', blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    # criado_por = models.ForeignKey(
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     related_name='documentos_criado',
    #     verbose_name='Criado por'
    # )
    
    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        ordering = ['data_validade']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.numero}"
    
    def dias_para_vencer(self):
        """Calcula dias até vencimento"""
        from datetime import date
        delta = self.data_validade - date.today()
        return delta.days
    
    def esta_vencido(self):
        """Verifica se documento está vencido"""
        return self.dias_para_vencer() < 0
    
    def esta_vencendo(self):
        """Verifica se documento está vencendo em 30 dias"""
        dias = self.dias_para_vencer()
        return 0 <= dias <= 30
    
    def save(self, *args, **kwargs):
        # Atualizar status baseado na validade
        if self.esta_vencido():
            self.status = 'VENCIDO'
        elif self.esta_vencendo():
            self.status = 'VENCENDO'
        else:
            self.status = 'ATIVO'
        super().save(*args, **kwargs)
