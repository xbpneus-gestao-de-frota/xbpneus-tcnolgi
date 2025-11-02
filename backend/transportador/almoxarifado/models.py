from django.conf import settings
"""
Models para o módulo de Almoxarifado
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class TipoAlmoxarifado(models.TextChoices):
    """Tipos de almoxarifado"""
    CENTRAL = 'CENTRAL', 'Central'
    FILIAL = 'FILIAL', 'Filial'
    MOVEL = 'MOVEL', 'Móvel'
    TERCEIRIZADO = 'TERCEIRIZADO', 'Terceirizado'


class Almoxarifado(models.Model):
    """Almoxarifado"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='almoxarifados',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa à qual o almoxarifado pertence"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='almoxarifados',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial à qual o almoxarifado está associado"
    )
    # empresa = models.ForeignKey(
    #     on_delete=models.CASCADE,
    #     related_name='almoxarifados',
    #     verbose_name='Empresa'
    # )
    
    # Dados básicos
    codigo = models.CharField('Código', max_length=20, unique=True)
    nome = models.CharField('Nome', max_length=200)
    tipo = models.CharField(
        'Tipo',
        max_length=20,
        choices=TipoAlmoxarifado.choices,
        default=TipoAlmoxarifado.CENTRAL
    )
    
    # Localização
    endereco = models.TextField('Endereço')
    cidade = models.CharField('Cidade', max_length=100)
    estado = models.CharField('Estado', max_length=2)
    cep = models.CharField('CEP', max_length=10)
    
    # Responsável
    # responsavel = models.ForeignKey(
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     related_name='almoxarifados_responsavel',
    #     verbose_name='Responsável'
    # )
    telefone = models.CharField('Telefone', max_length=20, blank=True)
    email = models.EmailField('Email', blank=True)
    
    # Status
    ativo = models.BooleanField('Ativo', default=True)
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Almoxarifado'
        verbose_name_plural = 'Almoxarifados'
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.codigo} - {self.nome}"


class LocalEstoque(models.Model):
    """Local de Estoque dentro do Almoxarifado"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='locais_estoque',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa à qual o local de estoque pertence"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='locais_estoque',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial à qual o local de estoque está associado"
    )
    almoxarifado = models.ForeignKey(
        Almoxarifado,
        on_delete=models.CASCADE,
        related_name='locais',
        verbose_name='Almoxarifado'
    )
    
    # Dados básicos
    codigo = models.CharField('Código', max_length=20)
    descricao = models.CharField('Descrição', max_length=200)
    
    # Localização física
    corredor = models.CharField('Corredor', max_length=10, blank=True)
    prateleira = models.CharField('Prateleira', max_length=10, blank=True)
    nivel = models.CharField('Nível', max_length=10, blank=True)
    posicao = models.CharField('Posição', max_length=10, blank=True)
    
    # Capacidade
    capacidade_maxima = models.DecimalField(
        'Capacidade Máxima',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    unidade_capacidade = models.CharField('Unidade', max_length=10, blank=True)
    
    # Status
    ativo = models.BooleanField('Ativo', default=True)
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Local de Estoque'
        verbose_name_plural = 'Locais de Estoque'
        ordering = ['almoxarifado', 'codigo']
        unique_together = [['almoxarifado', 'codigo']]
    
    def __str__(self):
        return f"{self.almoxarifado.codigo} - {self.codigo} - {self.descricao}"


class TipoMovimentacao(models.TextChoices):
    """Tipos de movimentação"""
    ENTRADA = 'ENTRADA', 'Entrada'
    SAIDA = 'SAIDA', 'Saída'
    TRANSFERENCIA = 'TRANSFERENCIA', 'Transferência'
    AJUSTE = 'AJUSTE', 'Ajuste'
    DEVOLUCAO = 'DEVOLUCAO', 'Devolução'


class MovimentacaoAlmoxarifado(models.Model):
    """Movimentação de Almoxarifado"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='movimentacoes_almoxarifado_empresa',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa à qual a movimentação pertence"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='movimentacoes_almoxarifado_filial',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial à qual a movimentação está associada"
    )
    almoxarifado = models.ForeignKey(
        Almoxarifado,
        on_delete=models.CASCADE,
        related_name='movimentacoes',
        verbose_name='Almoxarifado'
    )
    local_estoque = models.ForeignKey(
        LocalEstoque,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='movimentacoes',
        verbose_name='Local de Estoque'
    )
    
    # Dados básicos
    numero = models.CharField('Número', max_length=20, unique=True)
    tipo = models.CharField(
        'Tipo',
        max_length=20,
        choices=TipoMovimentacao.choices
    )
    data_movimentacao = models.DateTimeField('Data da Movimentação')
    
    # Produto/Material
    codigo_produto = models.CharField('Código do Produto', max_length=60)
    descricao_produto = models.CharField('Descrição do Produto', max_length=200)
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
        decimal_places=2,
        default=Decimal('0.00')
    )
    valor_total = models.DecimalField(
        'Valor Total',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    # Origem/Destino (para transferências)
    almoxarifado_destino = models.ForeignKey(
        Almoxarifado,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='movimentacoes_destino',
        verbose_name='Almoxarifado Destino'
    )
    
    # Documento relacionado
    documento_referencia = models.CharField('Documento de Referência', max_length=50, blank=True)
    
    # Observações
    observacoes = models.TextField('Observações', blank=True)
    
    # Responsável
    # responsavel = models.ForeignKey(
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     related_name='movimentacoes_almoxarifado',
    #     verbose_name='Responsável'
    # )
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Movimentação de Almoxarifado'
        verbose_name_plural = 'Movimentações de Almoxarifado'
        ordering = ['-data_movimentacao']
    
    def __str__(self):
        return f"{self.numero} - {self.tipo} - {self.descricao_produto}"
    
    def save(self, *args, **kwargs):
        """Calcula o valor total"""
        self.valor_total = self.quantidade * self.valor_unitario
        super().save(*args, **kwargs)


class InventarioAlmoxarifado(models.Model):
    """Inventário de Almoxarifado"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='inventarios_almoxarifado_empresa',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa à qual o inventário pertence"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='inventarios_almoxarifado_filial',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial à qual o inventário está associado"
    )
    almoxarifado = models.ForeignKey(
        Almoxarifado,
        on_delete=models.CASCADE,
        related_name='inventarios',
        verbose_name='Almoxarifado'
    )
    
    # Dados básicos
    numero = models.CharField('Número', max_length=20, unique=True)
    data_inventario = models.DateField('Data do Inventário')
    data_inicio = models.DateTimeField('Data de Início')
    data_conclusao = models.DateTimeField('Data de Conclusão', null=True, blank=True)
    
    # Status
    status = models.CharField(
        'Status',
        max_length=20,
        choices=[
            ('PLANEJADO', 'Planejado'),
            ('EM_ANDAMENTO', 'Em Andamento'),
            ('CONCLUIDO', 'Concluído'),
            ('CANCELADO', 'Cancelado'),
        ],
        default='PLANEJADO'
    )
    
    # Responsável
    # responsavel = models.ForeignKey(
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     related_name='inventarios_responsavel',
    #     verbose_name='Responsável'
    # )
    
    # Observações
    observacoes = models.TextField('Observações', blank=True)
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Inventário de Almoxarifado'
        verbose_name_plural = 'Inventários de Almoxarifado'
        ordering = ['-data_inventario']
    
    def __str__(self):
        return f"{self.numero} - {self.almoxarifado.nome} - {self.data_inventario}"


class ItemInventario(models.Model):
    """Item do Inventário"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='itens_inventario_empresa',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa à qual o item de inventário pertence"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='itens_inventario_filial',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial à qual o item de inventário está associado"
    )
    inventario = models.ForeignKey(
        InventarioAlmoxarifado,
        on_delete=models.CASCADE,
        related_name='itens',
        verbose_name='Inventário'
    )
    local_estoque = models.ForeignKey(
        LocalEstoque,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='itens_inventario',
        verbose_name='Local de Estoque'
    )
    
    # Produto
    codigo_produto = models.CharField('Código do Produto', max_length=60)
    descricao_produto = models.CharField('Descrição do Produto', max_length=200)
    unidade = models.CharField('Unidade', max_length=10)
    
    # Quantidades
    quantidade_sistema = models.DecimalField(
        'Quantidade no Sistema',
        max_digits=15,
        decimal_places=4,
        default=Decimal('0.0000')
    )
    quantidade_contada = models.DecimalField(
        'Quantidade Contada',
        max_digits=15,
        decimal_places=4,
        null=True,
        blank=True
    )
    diferenca = models.DecimalField(
        'Diferença',
        max_digits=15,
        decimal_places=4,
        default=Decimal('0.0000')
    )
    
    # Valores
    valor_unitario = models.DecimalField(
        'Valor Unitário',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    valor_diferenca = models.DecimalField(
        'Valor da Diferença',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    # Observações
    observacoes = models.TextField('Observações', blank=True)
    
    # Auditoria
    contado_em = models.DateTimeField('Contado em', null=True, blank=True)
    contado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='itens_inventario_contados',
        verbose_name='Contado por'
    )
    
    class Meta:
        verbose_name = 'Item de Inventário'
        verbose_name_plural = 'Itens de Inventário'
        ordering = ['inventario', 'codigo_produto']
    
    def __str__(self):
        return f"{self.codigo_produto} - {self.descricao_produto}"
    
    def save(self, *args, **kwargs):
        """Calcula diferenças"""
        if self.quantidade_contada is not None:
            self.diferenca = self.quantidade_contada - self.quantidade_sistema
            self.valor_diferenca = self.diferenca * self.valor_unitario
        super().save(*args, **kwargs)


class RequisicaoMaterial(models.Model):
    """Requisição de Material"""
    
    # Relacionamentos
    almoxarifado = models.ForeignKey(
        Almoxarifado,
        on_delete=models.CASCADE,
        related_name='requisicoes',
        verbose_name='Almoxarifado'
    )
    
    # Dados básicos
    numero = models.CharField('Número', max_length=20, unique=True)
    data_requisicao = models.DateTimeField('Data da Requisição')
    data_necessidade = models.DateField('Data de Necessidade')
    
    # Solicitante
    solicitante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='requisicoes_solicitadas',
        verbose_name='Solicitante'
    )
    departamento = models.CharField('Departamento', max_length=100, blank=True)
    centro_custo = models.CharField('Centro de Custo', max_length=50, blank=True)
    
    # Status
    status = models.CharField(
        'Status',
        max_length=20,
        choices=[
            ('PENDENTE', 'Pendente'),
            ('APROVADA', 'Aprovada'),
            ('EM_SEPARACAO', 'Em Separação'),
            ('ATENDIDA', 'Atendida'),
            ('CANCELADA', 'Cancelada'),
        ],
        default='PENDENTE'
    )
    
    # Aprovação
    aprovada_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='requisicoes_aprovadas',
        verbose_name='Aprovada por'
    )
    data_aprovacao = models.DateTimeField('Data de Aprovação', null=True, blank=True)
    
    # Atendimento
    atendida_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='requisicoes_atendidas',
        verbose_name='Atendida por'
    )
    data_atendimento = models.DateTimeField('Data de Atendimento', null=True, blank=True)
    
    # Observações
    observacoes = models.TextField('Observações', blank=True)
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Requisição de Material'
        verbose_name_plural = 'Requisições de Material'
        ordering = ['-data_requisicao']
    
    def __str__(self):
        return f"{self.numero} - {self.solicitante} - {self.status}"


class ItemRequisicao(models.Model):
    """Item da Requisição de Material"""
    
    # Relacionamentos
    requisicao = models.ForeignKey(
        RequisicaoMaterial,
        on_delete=models.CASCADE,
        related_name='itens',
        verbose_name='Requisição'
    )
    
    # Produto
    codigo_produto = models.CharField('Código do Produto', max_length=60)
    descricao_produto = models.CharField('Descrição do Produto', max_length=200)
    unidade = models.CharField('Unidade', max_length=10)
    
    # Quantidades
    quantidade_solicitada = models.DecimalField(
        'Quantidade Solicitada',
        max_digits=15,
        decimal_places=4,
        validators=[MinValueValidator(Decimal('0.0001'))]
    )
    quantidade_atendida = models.DecimalField(
        'Quantidade Atendida',
        max_digits=15,
        decimal_places=4,
        default=Decimal('0.0000')
    )
    
    # Observações
    observacoes = models.TextField('Observações', blank=True)
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Item de Requisição'
        verbose_name_plural = 'Itens de Requisição'
        ordering = ['requisicao', 'codigo_produto']
    
    def __str__(self):
        return f"{self.codigo_produto} - {self.descricao_produto}"
