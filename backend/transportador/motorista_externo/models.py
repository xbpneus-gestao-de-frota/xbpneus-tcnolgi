from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

class MotoristaExterno(models.Model):
    """Modelo para motoristas parceiros com login próprio"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='motoristas_externos_empresa',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa à qual o motorista externo está vinculado"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='motoristas_externos_filial',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial à qual o motorista externo está associado"
    )
    nome_completo = models.CharField('Nome Completo', max_length=200)
    cpf = models.CharField("CPF", max_length=14, unique=True)
    cnpj = models.CharField("CNPJ", max_length=18, unique=True, blank=True, null=True)
    cnh = models.CharField("CNH", max_length=20, unique=True)
    telefone = models.CharField('Telefone', max_length=20, blank=True, null=True)
    email = models.EmailField('Email', unique=True)
    STATUS_CHOICES = [
        ('ATIVO', 'Ativo'),
        ('INATIVO', 'Inativo'),
        ('BLOQUEADO', 'Bloqueado'),
    ]
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='ATIVO')
    aprovado = models.BooleanField("Aprovado", default=False, help_text="Indica se o motorista externo foi aprovado por um administrador")
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='motorista_externo_perfil',
        verbose_name="Usuário do Sistema",
        null=True,
        blank=True,
        help_text="Vínculo com o usuário do Django para autenticação"
    )
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Motorista Externo'
        verbose_name_plural = 'Motoristas Externos'
        ordering = ['nome_completo']

    def __str__(self):
        return self.nome_completo


class AlocacaoMotorista(models.Model):
    """Registro de alocação de motoristas a veículos/composições"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='alocacoes_motorista_empresa',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa à qual a alocação pertence"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='alocacoes_motorista_filial',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial à qual a alocação está associada"
    )
    veiculo = models.ForeignKey(
        'frota.Vehicle',
        on_delete=models.PROTECT,
        related_name='alocacoes_motorista',
        verbose_name="Veículo Alocado",
        null=True,
        blank=True
    )
    # composicao = models.ForeignKey(
    #     'frota.ComposicaoVeiculo', # Assumindo que ComposicaoVeiculo será criado no módulo frota
    #     on_delete=models.PROTECT,
    #     related_name='alocacoes_motorista',
    #     verbose_name="Composição Alocada",
    #     null=True,
    #     blank=True
    # )
    motorista_interno = models.ForeignKey(
        'motorista_interno.MotoristaInterno',
        on_delete=models.PROTECT,
        related_name='alocacoes_veiculo',
        verbose_name="Motorista Interno",
        null=True,
        blank=True
    )
    motorista_externo = models.ForeignKey(
        MotoristaExterno,
        on_delete=models.PROTECT,
        related_name='alocacoes_veiculo',
        verbose_name="Motorista Externo",
        null=True,
        blank=True
    )
    data_inicio = models.DateTimeField('Data de Início', default=timezone.now)
    data_fim = models.DateTimeField('Data de Fim', null=True, blank=True)
    STATUS_CHOICES = [
        ('ATIVA', 'Ativa'),
        ('CONCLUIDA', 'Concluída'),
        ('CANCELADA', 'Cancelada'),
    ]
    status = models.CharField('Status da Alocação', max_length=20, choices=STATUS_CHOICES, default='ATIVA')
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Alocação de Motorista'
        verbose_name_plural = 'Alocações de Motoristas'
        ordering = ['-data_inicio']

    def __str__(self):
        motorista = self.motorista_interno or self.motorista_externo
        veiculo = self.veiculo # or self.composicao
        return f"Alocação de {motorista} para {veiculo} ({self.status})"

