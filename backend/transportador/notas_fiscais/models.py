from django.conf import settings
"""
Models para o módulo de Notas Fiscais
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class TipoNotaFiscal(models.TextChoices):
    """Tipos de nota fiscal"""
    ENTRADA = 'ENTRADA', 'Entrada'
    SAIDA = 'SAIDA', 'Saída'
    SERVICO = 'SERVICO', 'Serviço'
    DEVOLUCAO = 'DEVOLUCAO', 'Devolução'


class StatusNotaFiscal(models.TextChoices):
    """Status da nota fiscal"""
    RASCUNHO = 'RASCUNHO', 'Rascunho'
    EMITIDA = 'EMITIDA', 'Emitida'
    AUTORIZADA = 'AUTORIZADA', 'Autorizada'
    CANCELADA = 'CANCELADA', 'Cancelada'
    DENEGADA = 'DENEGADA', 'Denegada'
    REJEITADA = 'REJEITADA', 'Rejeitada'


class ModeloNotaFiscal(models.TextChoices):
    """Modelo da nota fiscal"""
    NFE = '55', 'NF-e (Modelo 55)'
    NFCE = '65', 'NFC-e (Modelo 65)'
    CTE = '57', 'CT-e (Modelo 57)'
    NFSE = 'NFSE', 'NFS-e'


class NotaFiscal(models.Model):
    """Nota Fiscal"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='notas_fiscais',
        verbose_name='Empresa'
    )
    
    # Dados básicos
    numero = models.CharField('Número', max_length=20)
    serie = models.CharField('Série', max_length=10)
    modelo = models.CharField(
        'Modelo',
        max_length=10,
        choices=ModeloNotaFiscal.choices,
        default=ModeloNotaFiscal.NFE
    )
    tipo = models.CharField(
        'Tipo',
        max_length=20,
        choices=TipoNotaFiscal.choices,
        default=TipoNotaFiscal.SAIDA
    )
    status = models.CharField(
        'Status',
        max_length=20,
        choices=StatusNotaFiscal.choices,
        default=StatusNotaFiscal.RASCUNHO
    )
    
    # Datas
    data_emissao = models.DateTimeField('Data de Emissão')
    data_autorizacao = models.DateTimeField('Data de Autorização', null=True, blank=True)
    data_cancelamento = models.DateTimeField('Data de Cancelamento', null=True, blank=True)
    
    # Emitente
    emitente_cnpj = models.CharField('CNPJ Emitente', max_length=18)
    emitente_nome = models.CharField('Nome Emitente', max_length=200)
    emitente_ie = models.CharField('IE Emitente', max_length=20, blank=True)
    
    # Destinatário
    destinatario_cpf_cnpj = models.CharField('CPF/CNPJ Destinatário', max_length=18)
    destinatario_nome = models.CharField('Nome Destinatário', max_length=200)
    destinatario_ie = models.CharField('IE Destinatário', max_length=20, blank=True)
    destinatario_endereco = models.TextField('Endereço Destinatário', blank=True)
    
    # Valores
    valor_produtos = models.DecimalField(
        'Valor Produtos',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    valor_servicos = models.DecimalField(
        'Valor Serviços',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    valor_desconto = models.DecimalField(
        'Valor Desconto',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    valor_frete = models.DecimalField(
        'Valor Frete',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    valor_seguro = models.DecimalField(
        'Valor Seguro',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    valor_outras_despesas = models.DecimalField(
        'Outras Despesas',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    valor_total = models.DecimalField(
        'Valor Total',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    # Impostos
    base_calculo_icms = models.DecimalField(
        'Base Cálculo ICMS',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    valor_icms = models.DecimalField(
        'Valor ICMS',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    valor_ipi = models.DecimalField(
        'Valor IPI',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    valor_pis = models.DecimalField(
        'Valor PIS',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    valor_cofins = models.DecimalField(
        'Valor COFINS',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    # SEFAZ
    chave_acesso = models.CharField('Chave de Acesso', max_length=44, blank=True, unique=True, null=True)
    protocolo_autorizacao = models.CharField('Protocolo de Autorização', max_length=50, blank=True)
    motivo_cancelamento = models.TextField('Motivo do Cancelamento', blank=True)
    
    # XML
    xml_enviado = models.TextField('XML Enviado', blank=True)
    xml_retorno = models.TextField('XML Retorno', blank=True)
    
    # Observações
    observacoes = models.TextField('Observações', blank=True)
    informacoes_complementares = models.TextField('Informações Complementares', blank=True)
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='notas_fiscais_criadas',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'Nota Fiscal'
        verbose_name_plural = 'Notas Fiscais'
        ordering = ['-data_emissao', '-numero']
        unique_together = [['empresa', 'numero', 'serie', 'modelo']]
        indexes = [
            models.Index(fields=['empresa', 'status']),
            models.Index(fields=['data_emissao']),
            models.Index(fields=['chave_acesso']),
            models.Index(fields=['destinatario_cpf_cnpj']),
        ]
    
    def __str__(self):
        return f"NF {self.numero}/{self.serie} - {self.destinatario_nome}"
    
    def save(self, *args, **kwargs):
        """Calcula o valor total antes de salvar"""
        self.valor_total = (
            self.valor_produtos +
            self.valor_servicos +
            self.valor_frete +
            self.valor_seguro +
            self.valor_outras_despesas -
            self.valor_desconto
        )
        super().save(*args, **kwargs)


class ItemNotaFiscal(models.Model):
    """Item da Nota Fiscal"""
    
    # Relacionamentos
    nota_fiscal = models.ForeignKey(
        NotaFiscal,
        on_delete=models.CASCADE,
        related_name='itens',
        verbose_name='Nota Fiscal'
    )
    
    # Dados do produto/serviço
    numero_item = models.PositiveIntegerField('Número do Item')
    codigo_produto = models.CharField('Código do Produto', max_length=60)
    descricao = models.CharField('Descrição', max_length=500)
    ncm = models.CharField('NCM', max_length=8, blank=True)
    cfop = models.CharField('CFOP', max_length=4)
    unidade = models.CharField('Unidade', max_length=10)
    
    # Quantidades
    quantidade = models.DecimalField(
        'Quantidade',
        max_digits=15,
        decimal_places=4,
        validators=[MinValueValidator(Decimal('0.0001'))]
    )
    valor_unitario = models.DecimalField(
        'Valor Unitário',
        max_digits=15,
        decimal_places=4,
        validators=[MinValueValidator(Decimal('0.0001'))]
    )
    valor_total = models.DecimalField(
        'Valor Total',
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    valor_desconto = models.DecimalField(
        'Valor Desconto',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    # Impostos
    aliquota_icms = models.DecimalField(
        'Alíquota ICMS (%)',
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00')
    )
    valor_icms = models.DecimalField(
        'Valor ICMS',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    aliquota_ipi = models.DecimalField(
        'Alíquota IPI (%)',
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00')
    )
    valor_ipi = models.DecimalField(
        'Valor IPI',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    # Informações adicionais
    informacoes_adicionais = models.TextField('Informações Adicionais', blank=True)
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Item de Nota Fiscal'
        verbose_name_plural = 'Itens de Nota Fiscal'
        ordering = ['nota_fiscal', 'numero_item']
        unique_together = [['nota_fiscal', 'numero_item']]
    
    def __str__(self):
        return f"Item {self.numero_item} - {self.descricao}"
    
    def save(self, *args, **kwargs):
        """Calcula valores antes de salvar"""
        self.valor_total = (self.quantidade * self.valor_unitario) - self.valor_desconto
        self.valor_icms = self.valor_total * (self.aliquota_icms / 100)
        self.valor_ipi = self.valor_total * (self.aliquota_ipi / 100)
        super().save(*args, **kwargs)


class ImpostoNotaFiscal(models.Model):
    """Detalhamento de Impostos da Nota Fiscal"""
    
    # Relacionamentos
    nota_fiscal = models.ForeignKey(
        NotaFiscal,
        on_delete=models.CASCADE,
        related_name='impostos',
        verbose_name='Nota Fiscal'
    )
    
    # Tipo de imposto
    tipo_imposto = models.CharField('Tipo de Imposto', max_length=20)
    
    # Valores
    base_calculo = models.DecimalField(
        'Base de Cálculo',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    aliquota = models.DecimalField(
        'Alíquota (%)',
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00')
    )
    valor_imposto = models.DecimalField(
        'Valor do Imposto',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    # Informações adicionais
    descricao = models.TextField('Descrição', blank=True)
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Imposto de Nota Fiscal'
        verbose_name_plural = 'Impostos de Nota Fiscal'
        ordering = ['nota_fiscal', 'tipo_imposto']
    
    def __str__(self):
        return f"{self.tipo_imposto} - R$ {self.valor_imposto}"


class AnexoNotaFiscal(models.Model):
    """Anexos da Nota Fiscal"""
    
    # Relacionamentos
    nota_fiscal = models.ForeignKey(
        NotaFiscal,
        on_delete=models.CASCADE,
        related_name='anexos',
        verbose_name='Nota Fiscal'
    )
    
    # Dados do anexo
    titulo = models.CharField('Título', max_length=200)
    descricao = models.TextField('Descrição', blank=True)
    arquivo = models.FileField('Arquivo', upload_to='notas_fiscais/anexos/%Y/%m/')
    tipo_arquivo = models.CharField('Tipo de Arquivo', max_length=50)
    tamanho_arquivo = models.PositiveIntegerField('Tamanho (bytes)', default=0)
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='anexos_nf_criados',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'Anexo de Nota Fiscal'
        verbose_name_plural = 'Anexos de Nota Fiscal'
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"{self.titulo} - {self.nota_fiscal}"
