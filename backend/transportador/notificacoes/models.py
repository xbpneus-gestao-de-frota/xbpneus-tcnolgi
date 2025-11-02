from django.db import models
from django.utils import timezone
from django.conf import settings
from backend.transportador.empresas.models import Empresa


class CanalNotificacao(models.Model):
    """Canais de notificação disponíveis"""
    TIPO_CHOICES = [
        ('EMAIL', 'E-mail'),
        ('SMS', 'SMS'),
        ('PUSH', 'Push Notification'),
        ('WHATSAPP', 'WhatsApp'),
        ('IN_APP', 'In-App'),
    ]
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='canais_notificacao')
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    nome = models.CharField(max_length=100)
    
    ativo = models.BooleanField(default=True)
    
    # Configurações específicas do canal (JSON)
    configuracao_json = models.JSONField(blank=True, null=True, help_text='Configurações como API keys, endpoints, etc')
    
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Canal de Notificação'
        verbose_name_plural = 'Canais de Notificação'
        ordering = ['tipo', 'nome']
        unique_together = ['empresa', 'tipo', 'nome']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.nome}"


class Notificacao(models.Model):
    """Notificações enviadas"""
    PRIORIDADE_CHOICES = [
        ('BAIXA', 'Baixa'),
        ('NORMAL', 'Normal'),
        ('ALTA', 'Alta'),
        ('URGENTE', 'Urgente'),
    ]
    
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('ENVIANDO', 'Enviando'),
        ('ENVIADA', 'Enviada'),
        ('ENTREGUE', 'Entregue'),
        ('LIDA', 'Lida'),
        ('FALHA', 'Falha'),
    ]
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='notificacoes')
    canal = models.ForeignKey(CanalNotificacao, on_delete=models.PROTECT, related_name='notificacoes')
    
    destinatario_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='notificacoes_recebidas')
    destinatario_email = models.EmailField(blank=True, null=True)
    destinatario_telefone = models.CharField(max_length=20, blank=True, null=True)
    
    titulo = models.CharField(max_length=200)
    mensagem = models.TextField()
    
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES, default='NORMAL')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    
    # Metadados
    categoria = models.CharField(max_length=50, blank=True, null=True, help_text='Ex: manutencao, viagem, financeiro')
    referencia_tipo = models.CharField(max_length=50, blank=True, null=True, help_text='Tipo do objeto relacionado')
    referencia_id = models.IntegerField(blank=True, null=True, help_text='ID do objeto relacionado')
    
    # Datas
    agendada_para = models.DateTimeField(blank=True, null=True)
    enviada_em = models.DateTimeField(blank=True, null=True)
    entregue_em = models.DateTimeField(blank=True, null=True)
    lida_em = models.DateTimeField(blank=True, null=True)
    
    # Controle de tentativas
    tentativas = models.IntegerField(default=0)
    max_tentativas = models.IntegerField(default=3)
    erro_mensagem = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        ordering = ['-criado_em']
        indexes = [
            models.Index(fields=['destinatario_usuario', 'status']),
            models.Index(fields=['status', 'agendada_para']),
        ]
    
    def __str__(self):
        return f"{self.titulo} - {self.get_status_display()}"
    
    def marcar_como_lida(self):
        """Marca notificação como lida"""
        self.status = 'LIDA'
        self.lida_em = timezone.now()
        self.save()
    
    def pode_reenviar(self):
        """Verifica se pode tentar reenviar"""
        return self.tentativas < self.max_tentativas and self.status == 'FALHA'


class TemplateNotificacao(models.Model):
    """Templates de notificações"""
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='templates_notificacao')
    
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    
    categoria = models.CharField(max_length=50)
    
    # Templates por canal
    template_email_assunto = models.CharField(max_length=200, blank=True, null=True)
    template_email_corpo = models.TextField(blank=True, null=True)
    template_sms = models.CharField(max_length=160, blank=True, null=True)
    template_push_titulo = models.CharField(max_length=100, blank=True, null=True)
    template_push_corpo = models.CharField(max_length=200, blank=True, null=True)
    
    # Variáveis disponíveis (JSON)
    variaveis_json = models.JSONField(blank=True, null=True, help_text='Lista de variáveis disponíveis no template')
    
    ativo = models.BooleanField(default=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Template de Notificação'
        verbose_name_plural = 'Templates de Notificação'
        ordering = ['categoria', 'nome']
    
    def __str__(self):
        return f"{self.categoria} - {self.nome}"


class PreferenciaNotificacao(models.Model):
    """Preferências de notificação por usuário"""
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='preferencias_notificacao')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='preferencias_notificacao')
    
    # Canais habilitados
    email_habilitado = models.BooleanField(default=True)
    sms_habilitado = models.BooleanField(default=False)
    push_habilitado = models.BooleanField(default=True)
    whatsapp_habilitado = models.BooleanField(default=False)
    
    # Categorias de interesse (JSON)
    categorias_json = models.JSONField(blank=True, null=True, help_text='Categorias que o usuário deseja receber')
    
    # Horário de silêncio
    silencio_inicio = models.TimeField(blank=True, null=True)
    silencio_fim = models.TimeField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Preferência de Notificação'
        verbose_name_plural = 'Preferências de Notificação'
    
    def __str__(self):
        return f"Preferências de {self.usuario.username}"
    
    def esta_em_silencio(self):
        """Verifica se está no horário de silêncio"""
        if not self.silencio_inicio or not self.silencio_fim:
            return False
        agora = timezone.now().time()
        return self.silencio_inicio <= agora <= self.silencio_fim
