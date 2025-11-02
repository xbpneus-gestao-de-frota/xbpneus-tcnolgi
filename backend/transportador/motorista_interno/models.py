from django.db import models
from django.utils import timezone
from backend.transportador.empresas.models import Empresa
from backend.transportador.frota.models import Vehicle


class MotoristaInterno(models.Model):
    """Motorista vinculado ao transportador - Porta de comunicação com motorista externo"""
    STATUS_CHOICES = [
        ('ATIVO', 'Ativo'),
        ('INATIVO', 'Inativo'),
        ('FERIAS', 'Férias'),
        ('AFASTADO', 'Afastado'),
        ('DESLIGADO', 'Desligado'),
    ]
    
    TIPO_CONTRATO_CHOICES = [
        ('CLT', 'CLT'),
        ('AGREGADO', 'Agregado'),
        ('TERCEIRO', 'Terceiro'),
        ('TEMPORARIO', 'Temporário'),
    ]
    
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.PROTECT,
        related_name='motoristas_internos_empresa',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa à qual o motorista interno está vinculado"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='motoristas_internos_filial',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial à qual o motorista interno está associado"
    )
    
    # Dados pessoais
    nome_completo = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    
    # Contato
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)
    
    # Dados profissionais
    cnh = models.CharField(max_length=20, unique=True)
    categoria_cnh = models.CharField(max_length=5, default='D')  # A, B, C, D, E
    validade_cnh = models.DateField()
    numero_registro = models.CharField(max_length=50, blank=True, null=True)
    
    # Vínculo
    tipo_contrato = models.CharField(max_length=20, choices=TIPO_CONTRATO_CHOICES, default='CLT')
    data_admissao = models.DateField(default=timezone.now)
    data_desligamento = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ATIVO')
    
    # Conexão com motorista externo (app)
    motorista_externo_id = models.CharField(max_length=100, blank=True, null=True, help_text='ID do motorista no sistema externo')
    conectado_app = models.BooleanField(default=False, help_text='Motorista conectado ao app externo')
    ultimo_acesso_app = models.DateTimeField(blank=True, null=True)
    
    # Observações
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Motorista Interno'
        verbose_name_plural = 'Motoristas Internos'
        ordering = ['nome_completo']
    
    def __str__(self):
        return f"{self.nome_completo} - {self.cnh}"
    
    def cnh_valida(self):
        """Verifica se CNH está válida"""
        from datetime import date
        return self.validade_cnh >= date.today()


class VinculoMotoristaVeiculo(models.Model):
    """Vínculo entre motorista e veículo"""
    STATUS_CHOICES = [
        ('ATIVO', 'Ativo'),
        ('INATIVO', 'Inativo'),
    ]
    
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='vinculos_motorista_veiculo_empresa',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa à qual o vínculo pertence"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='vinculos_motorista_veiculo_filial',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial à qual o vínculo está associado"
    )
    motorista = models.ForeignKey(MotoristaInterno, on_delete=models.CASCADE, related_name='vinculos_veiculo')
    veiculo = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='vinculos_motorista')
    
    data_inicio = models.DateTimeField(default=timezone.now)
    data_fim = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ATIVO')
    
    observacoes = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Vínculo Motorista-Veículo'
        verbose_name_plural = 'Vínculos Motorista-Veículo'
        ordering = ['-data_inicio']
    
    def __str__(self):
        return f"{self.motorista.nome_completo} - {self.veiculo.placa}"


class RegistroJornada(models.Model):
    """Registro de jornada do motorista - Recebe dados do app externo"""
    TIPO_REGISTRO_CHOICES = [
        ('INICIO', 'Início de Jornada'),
        ('PAUSA', 'Pausa'),
        ('RETORNO', 'Retorno da Pausa'),
        ('FIM', 'Fim de Jornada'),
    ]
    
    ORIGEM_CHOICES = [
        ('APP', 'App Externo'),
        ('MANUAL', 'Manual'),
        ('SISTEMA', 'Sistema'),
    ]
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='registros_jornada_empresa',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa à qual o registro de jornada pertence"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='registros_jornada_filial',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial à qual o registro de jornada está associado"
    )
    motorista = models.ForeignKey(MotoristaInterno, on_delete=models.CASCADE, related_name='registros_jornada')
    veiculo = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name='registros_jornada')
    tipo_registro = models.CharField(max_length=20, choices=TIPO_REGISTRO_CHOICES)
    data_hora = models.DateTimeField(default=timezone.now)
    origem = models.CharField(max_length=20, choices=ORIGEM_CHOICES, default='APP')
    
    # Localização (recebida do app)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    localizacao_texto = models.CharField(max_length=200, blank=True, null=True)
    
    # Dados adicionais
    km_veiculo = models.IntegerField(blank=True, null=True, help_text='Quilometragem do veículo no momento do registro')
    observacoes = models.TextField(blank=True, null=True)
    
    # Metadados do app
    app_versao = models.CharField(max_length=20, blank=True, null=True)
    dispositivo_id = models.CharField(max_length=100, blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Registro de Jornada'
        verbose_name_plural = 'Registros de Jornada'
        ordering = ['-data_hora']
    
    def __str__(self):
        return f"{self.motorista.nome_completo} - {self.get_tipo_registro_display()} - {self.data_hora}"


class MensagemMotorista(models.Model):
    """Mensagens trocadas entre transportador e motorista via app"""
    TIPO_CHOICES = [
        ('ENVIADA', 'Enviada ao Motorista'),
        ('RECEBIDA', 'Recebida do Motorista'),
    ]
    
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('ENVIADA', 'Enviada'),
        ('ENTREGUE', 'Entregue'),
        ('LIDA', 'Lida'),
        ('ERRO', 'Erro'),
    ]
    
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='mensagens_motorista_empresa',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa à qual a mensagem pertence"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='mensagens_motorista_filial',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial à qual a mensagem está associada"
    )
    motorista = models.ForeignKey(MotoristaInterno, on_delete=models.CASCADE, related_name='mensagens')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    
    assunto = models.CharField(max_length=200, blank=True, null=True)
    mensagem = models.TextField()
    
    # Anexos (URLs ou referências)
    anexo_url = models.URLField(blank=True, null=True)
    anexo_tipo = models.CharField(max_length=50, blank=True, null=True)
    
    data_envio = models.DateTimeField(default=timezone.now)
    data_entrega = models.DateTimeField(blank=True, null=True)
    data_leitura = models.DateTimeField(blank=True, null=True)
    
    # Resposta (se for mensagem recebida)
    mensagem_resposta_de = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='respostas')
    
    criado_em = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Mensagem Motorista'
        verbose_name_plural = 'Mensagens Motoristas'
        ordering = ['-data_envio']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.motorista.nome_completo} - {self.assunto or 'Sem assunto'}"


class AlertaMotorista(models.Model):
    """Alertas relacionados ao motorista"""
    TIPO_CHOICES = [
        ('CNH_VENCENDO', 'CNH Vencendo'),
        ('CNH_VENCIDA', 'CNH Vencida'),
        ('JORNADA_EXCEDIDA', 'Jornada Excedida'),
        ('FALTA_REGISTRO', 'Falta Registro de Jornada'),
        ('MANUTENCAO_PENDENTE', 'Manutenção Pendente'),
        ('OUTRO', 'Outro'),
    ]
    
    PRIORIDADE_CHOICES = [
        ('BAIXA', 'Baixa'),
        ('MEDIA', 'Média'),
        ('ALTA', 'Alta'),
        ('URGENTE', 'Urgente'),
    ]
    
    STATUS_CHOICES = [
        ('ABERTO', 'Aberto'),
        ('EM_ANALISE', 'Em Análise'),
        ('RESOLVIDO', 'Resolvido'),
        ('IGNORADO', 'Ignorado'),
    ]
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='alertas_motorista_empresa',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa à qual o alerta pertence"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='alertas_motorista_filial',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial à qual o alerta está associado"
    )
    motorista = models.ForeignKey(MotoristaInterno, on_delete=models.CASCADE, related_name='alertas')
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    prioridade = models.CharField(max_length=20, choices=PRIORIDADE_CHOICES, default='MEDIA')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ABERTO')
    
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    
    data_alerta = models.DateTimeField(default=timezone.now)
    data_resolucao = models.DateTimeField(blank=True, null=True)
    
    resolvido_por = models.CharField(max_length=200, blank=True, null=True)
    observacoes_resolucao = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Alerta Motorista'
        verbose_name_plural = 'Alertas Motoristas'
        ordering = ['-data_alerta', '-prioridade']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.motorista.nome_completo} - {self.get_prioridade_display()}"
