from django.db import models
from django.conf import settings


class AnaliseIA(models.Model):
    """Modelo para armazenar análises de IA realizadas"""
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='analises_ia')
    data_analise = models.DateTimeField(auto_now_add=True)
    tipo_analise = models.CharField(max_length=50, choices=[
        ('imagem', 'Análise de Imagem'),
        ('video', 'Análise de Vídeo'),
        ('audio', 'Análise de Áudio'),
    ])
    
    # Dados da análise
    arquivo = models.FileField(upload_to='ia_analises/')
    resultado = models.JSONField()
    precisao = models.FloatField(default=0.0)
    
    # Metadados
    tempo_processamento = models.FloatField(default=0.0)  # em segundos
    status = models.CharField(max_length=20, default='processando')
    
    class Meta:
        ordering = ['-data_analise']
        verbose_name = 'Análise de IA'
        verbose_name_plural = 'Análises de IA'
    
    def __str__(self):
        return f"Análise {self.id} - {self.tipo_analise} ({self.data_analise.strftime('%d/%m/%Y')})"


class Gamificacao(models.Model):
    """Modelo para pontuação e ranking de motoristas"""
    
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pontos = models.IntegerField(default=0)
    nivel = models.CharField(max_length=20, default='bronze', choices=[
        ('bronze', 'Bronze'),
        ('prata', 'Prata'),
        ('ouro', 'Ouro'),
        ('platina', 'Platina'),
    ])
    
    # Conquistas
    conquistas = models.JSONField(default=list)
    
    class Meta:
        verbose_name = 'Gamificação'
        verbose_name_plural = 'Gamificações'
        ordering = ['-pontos']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.pontos} pontos"


class Garantia(models.Model):
    """Modelo para gestão de garantias"""
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    analise = models.ForeignKey(AnaliseIA, on_delete=models.CASCADE, related_name='garantias')
    
    # Dados da garantia
    protocolo = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, default='aberta', choices=[
        ('aberta', 'Aberta'),
        ('em_analise', 'Em Análise'),
        ('aprovada', 'Aprovada'),
        ('negada', 'Negada'),
    ])
    
    # Blockchain
    hash_blockchain = models.CharField(max_length=64, blank=True)
    
    # Datas
    data_abertura = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-data_abertura']
        verbose_name = 'Garantia'
        verbose_name_plural = 'Garantias'
    
    def __str__(self):
        return f"Garantia {self.protocolo} - {self.status}"

