from django.conf import settings
"""
Models completos para o módulo de Manutenção
Sistema XBPneus - Gestão de Frotas de Transporte
Expandido de 60% para 100% de completude
"""

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class TipoManutencao(models.TextChoices):
    """Tipos de manutenção"""
    PREVENTIVA = 'PREVENTIVA', 'Preventiva'
    CORRETIVA = 'CORRETIVA', 'Corretiva'
    PREDITIVA = 'PREDITIVA', 'Preditiva'
    EMERGENCIAL = 'EMERGENCIAL', 'Emergencial'



    def __str__(self):
        return f"TipoManutencao {self.pk}"

    def __str__(self):
        return f"TipoManutencao {self.pk}"
class StatusOS(models.TextChoices):
    """Status da Ordem de Serviço"""
    ABERTA = 'ABERTA', 'Aberta'
    AGENDADA = 'AGENDADA', 'Agendada'
    EM_ANDAMENTO = 'EM_ANDAMENTO', 'Em Andamento'
    AGUARDANDO_PECA = 'AGUARDANDO_PECA', 'Aguardando Peça'
    CONCLUIDA = 'CONCLUIDA', 'Concluída'
    CANCELADA = 'CANCELADA', 'Cancelada'


class PrioridadeOS(models.TextChoices):
    """Prioridade da OS"""
    BAIXA = 'BAIXA', 'Baixa'
    MEDIA = 'MEDIA', 'Média'
    ALTA = 'ALTA', 'Alta'
    CRITICA = 'CRITICA', 'Crítica'


# Model legado mantido para compatibilidade
class WorkOrder(models.Model):
    """Ordem de Serviço (modelo legado)"""
    tipo = models.CharField(max_length=30)  # Corretiva/Preventiva
    status = models.CharField(max_length=50, blank=True)
    veiculo = models.CharField(max_length=20)  # placa
    agendamento = models.CharField(max_length=20, blank=True)  # simplificado data
    
    class Meta:
        verbose_name = 'Work Order (Legado)'
        verbose_name_plural = 'Work Orders (Legado)'


class Teste(models.Model):
    """Teste (modelo legado)"""
    os_id = models.IntegerField()
    torque_ok = models.BooleanField(default=False)
    pressao_ok = models.BooleanField(default=False)
    rodagem_ok = models.BooleanField(default=False)
    data = models.CharField(max_length=30, blank=True)
    
    class Meta:
        verbose_name = 'Teste (Legado)'
        verbose_name_plural = 'Testes (Legado)'



    def __str__(self):
        return f"Teste {self.pk}"
class OrdemServico(models.Model):
    """Ordem de Serviço Completa"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='ordens_servico',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa à qual a OS pertence"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='ordens_servico',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial à qual a OS está associada"
    )
    # empresa = models.ForeignKey(
    #     on_delete=models.CASCADE,
    #     related_name='ordens_servico',
    #     verbose_name='Empresa'
    # )
    veiculo = models.ForeignKey(
        'frota.Vehicle',
        on_delete=models.CASCADE,
        related_name='ordens_servico',
        verbose_name='Veículo'
    )
    
    # Dados básicos
    numero = models.CharField('Número da OS', max_length=20, unique=True)
    tipo = models.CharField(
        'Tipo de Manutenção',
        max_length=20,
        choices=TipoManutencao.choices
    )
    status = models.CharField(
        'Status',
        max_length=20,
        choices=StatusOS.choices,
        default=StatusOS.ABERTA
    )
    prioridade = models.CharField(
        'Prioridade',
        max_length=10,
        choices=PrioridadeOS.choices,
        default=PrioridadeOS.MEDIA
    )
    
    # Datas
    data_abertura = models.DateTimeField('Data de Abertura', auto_now_add=True)
    data_agendamento = models.DateTimeField('Data de Agendamento', null=True, blank=True)
    data_inicio = models.DateTimeField('Data de Início', null=True, blank=True)
    data_conclusao = models.DateTimeField('Data de Conclusão', null=True, blank=True)
    data_cancelamento = models.DateTimeField('Data de Cancelamento', null=True, blank=True)
    
    # Descrição
    descricao_problema = models.TextField('Descrição do Problema')
    descricao_servico = models.TextField('Descrição do Serviço Realizado', blank=True)
    observacoes = models.TextField('Observações', blank=True)
    
    # Quilometragem
    km_abertura = models.IntegerField('KM na Abertura', null=True, blank=True)
    km_conclusao = models.IntegerField('KM na Conclusão', null=True, blank=True)
    
    # Custos
    custo_pecas = models.DecimalField(
        'Custo de Peças',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    custo_mao_obra = models.DecimalField(
        'Custo de Mão de Obra',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    custo_total = models.DecimalField(
        'Custo Total',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    # Responsáveis
    aberta_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='os_abertas',
        verbose_name='Aberta por'
    )
    mecanico = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='os_executadas',
        verbose_name='Mecânico'
    )
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Ordem de Serviço'
        verbose_name_plural = 'Ordens de Serviço'
        ordering = ['-data_abertura']
        indexes = [
            models.Index(fields=['numero']),
            models.Index(fields=['veiculo', 'status']),
            models.Index(fields=['status', 'prioridade']),
            models.Index(fields=['data_abertura']),
        ]
    
    def __str__(self):
        return f"OS {self.numero} - {self.veiculo.placa} - {self.status}"
    
    def save(self, *args, **kwargs):
        """Calcula custo total"""
        self.custo_total = self.custo_pecas + self.custo_mao_obra
        super().save(*args, **kwargs)
    
    @property
    def tempo_execucao(self):
        """Retorna o tempo de execução em horas"""
        if self.data_inicio and self.data_conclusao:
            delta = self.data_conclusao - self.data_inicio
            return delta.total_seconds() / 3600
        return None
    
    @property
    def esta_atrasada(self):
        """Verifica se a OS está atrasada"""
        if self.data_agendamento and self.status not in [StatusOS.CONCLUIDA, StatusOS.CANCELADA]:
            from django.utils import timezone
            return timezone.now() > self.data_agendamento
        return False


class ItemOS(models.Model):
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='itens_os',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa à qual o item da OS pertence"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='itens_os',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial à qual o item da OS está associado"
    )
    """Itens (peças/serviços) da Ordem de Serviço"""
    
    os = models.ForeignKey(
        OrdemServico,
        on_delete=models.CASCADE,
        related_name='itens',
        verbose_name='Ordem de Serviço'
    )
    
    tipo = models.CharField(
        'Tipo',
        max_length=10,
        choices=[
            ('PECA', 'Peça'),
            ('SERVICO', 'Serviço'),
        ]
    )
    
    codigo = models.CharField('Código', max_length=60)
    descricao = models.CharField('Descrição', max_length=200)
    quantidade = models.DecimalField(
        'Quantidade',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    unidade = models.CharField('Unidade', max_length=10, default='UN')
    
    valor_unitario = models.DecimalField(
        'Valor Unitário',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    valor_total = models.DecimalField(
        'Valor Total',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    aplicado = models.BooleanField('Aplicado', default=False)
    
    observacoes = models.TextField('Observações', blank=True)
    
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Item da OS'
        verbose_name_plural = 'Itens da OS'
        ordering = ['os', 'tipo', 'descricao']
    
    def __str__(self):
        return f"{self.codigo} - {self.descricao}"
    
    def save(self, *args, **kwargs):
        """Calcula valor total"""
        self.valor_total = self.quantidade * self.valor_unitario
        super().save(*args, **kwargs)


class ChecklistManutencao(models.Model):
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='checklists_manutencao',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa à qual o checklist pertence"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='checklists_manutencao',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial à qual o checklist está associado"
    )
    """Checklist de Manutenção"""
    
    os = models.ForeignKey(
        OrdemServico,
        on_delete=models.CASCADE,
        related_name='checklists',
        verbose_name='Ordem de Serviço'
    )
    
    # Itens do checklist
    nivel_oleo_motor = models.BooleanField('Nível de Óleo do Motor', default=False)
    nivel_fluido_freio = models.BooleanField('Nível de Fluido de Freio', default=False)
    nivel_agua_radiador = models.BooleanField('Nível de Água do Radiador', default=False)
    pressao_pneus = models.BooleanField('Pressão dos Pneus', default=False)
    estado_pneus = models.BooleanField('Estado dos Pneus', default=False)
    funcionamento_farois = models.BooleanField('Funcionamento dos Faróis', default=False)
    funcionamento_setas = models.BooleanField('Funcionamento das Setas', default=False)
    funcionamento_freios = models.BooleanField('Funcionamento dos Freios', default=False)
    funcionamento_buzina = models.BooleanField('Funcionamento da Buzina', default=False)
    limpeza_filtro_ar = models.BooleanField('Limpeza do Filtro de Ar', default=False)
    estado_correia = models.BooleanField('Estado da Correia', default=False)
    vazamentos = models.BooleanField('Verificação de Vazamentos', default=False)
    
    # Testes (mantido para compatibilidade)
    torque_ok = models.BooleanField('Torque OK', default=False)
    pressao_ok = models.BooleanField('Pressão OK', default=False)
    rodagem_ok = models.BooleanField('Rodagem OK', default=False)
    
    observacoes = models.TextField('Observações', blank=True)
    
    realizado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='checklists_realizados',
        verbose_name='Realizado por'
    )
    realizado_em = models.DateTimeField('Realizado em', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Checklist de Manutenção'
        verbose_name_plural = 'Checklists de Manutenção'
        ordering = ['-realizado_em']
    
    def __str__(self):
        return f"Checklist OS {self.os.numero}"
    
    @property
    def percentual_conclusao(self):
        """Calcula o percentual de itens concluídos"""
        campos_checklist = [
            self.nivel_oleo_motor, self.nivel_fluido_freio, self.nivel_agua_radiador,
            self.pressao_pneus, self.estado_pneus, self.funcionamento_farois,
            self.funcionamento_setas, self.funcionamento_freios, self.funcionamento_buzina,
            self.limpeza_filtro_ar, self.estado_correia, self.vazamentos,
            self.torque_ok, self.pressao_ok, self.rodagem_ok
        ]
        total = len(campos_checklist)
        concluidos = sum(1 for campo in campos_checklist if campo)
        return (concluidos / total) * 100 if total > 0 else 0


class PlanoManutencaoPreventiva(models.Model):
    """Plano de Manutenção Preventiva"""
    
    # empresa = models.ForeignKey(
    #     on_delete=models.CASCADE,
    #     related_name='planos_manutencao',
    #     verbose_name='Empresa'
    # )
    veiculo = models.ForeignKey(
        'frota.Vehicle',
        on_delete=models.CASCADE,
        related_name='planos_manutencao',
        verbose_name='Veículo',
        null=True,
        blank=True
    )
    
    nome = models.CharField('Nome do Plano', max_length=200)
    descricao = models.TextField('Descrição')
    
    # Periodicidade
    periodicidade_km = models.IntegerField(
        'Periodicidade em KM',
        null=True,
        blank=True,
        help_text='Ex: 10000 para manutenção a cada 10.000 km'
    )
    periodicidade_dias = models.IntegerField(
        'Periodicidade em Dias',
        null=True,
        blank=True,
        help_text='Ex: 90 para manutenção a cada 90 dias'
    )
    
    # Próxima manutenção
    proxima_manutencao_km = models.IntegerField('Próxima Manutenção (KM)', null=True, blank=True)
    proxima_manutencao_data = models.DateField('Próxima Manutenção (Data)', null=True, blank=True)
    
    # Status
    ativo = models.BooleanField('Ativo', default=True)
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='planos_manutencao_criados',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'Plano de Manutenção Preventiva'
        verbose_name_plural = 'Planos de Manutenção Preventiva'
        ordering = ['nome']
    
    def __str__(self):
        veiculo_str = f" - {self.veiculo.placa}" if self.veiculo else ""
        return f"{self.nome}{veiculo_str}"


class HistoricoManutencao(models.Model):
    """Histórico de Manutenções do Veículo"""
    
    veiculo = models.ForeignKey(
        'frota.Vehicle',
        on_delete=models.CASCADE,
        related_name='historico_manutencao',
        verbose_name='Veículo'
    )
    os = models.ForeignKey(
        OrdemServico,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='historicos',
        verbose_name='Ordem de Serviço'
    )
    
    data = models.DateTimeField('Data')
    tipo = models.CharField('Tipo', max_length=20, choices=TipoManutencao.choices)
    descricao = models.TextField('Descrição')
    km = models.IntegerField('Quilometragem', null=True, blank=True)
    custo = models.DecimalField(
        'Custo',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Histórico de Manutenção'
        verbose_name_plural = 'Históricos de Manutenção'
        ordering = ['-data']
    
    def __str__(self):
        return f"{self.veiculo.placa} - {self.tipo} - {self.data.strftime('%d/%m/%Y')}"
