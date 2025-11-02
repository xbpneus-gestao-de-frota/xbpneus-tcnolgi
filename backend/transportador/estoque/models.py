"""
Models expandidos para o módulo de Estoque
Sistema XBPneus - Gestão de Frotas de Transporte
Expandido de 20% para 60% de completude
"""

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class CategoriaProduto(models.Model):
    """Categoria de Produto"""
    
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='categorias_produto',
        verbose_name='Empresa'
    )
    
    codigo = models.CharField('Código', max_length=20)
    nome = models.CharField('Nome', max_length=200)
    descricao = models.TextField('Descrição', blank=True)
    ativo = models.BooleanField('Ativo', default=True)
    
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Categoria de Produto'
        verbose_name_plural = 'Categorias de Produto'
        ordering = ['nome']
        unique_together = [['empresa', 'codigo']]
    
    def __str__(self):
        return f"{self.codigo} - {self.nome}"


class Produto(models.Model):
    """Produto em Estoque"""
    
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='produtos',
        verbose_name='Empresa'
    )
    categoria = models.ForeignKey(
        CategoriaProduto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='produtos',
        verbose_name='Categoria'
    )
    
    codigo = models.CharField('Código', max_length=60, unique=True)
    codigo_barras = models.CharField('Código de Barras', max_length=50, blank=True)
    descricao = models.CharField('Descrição', max_length=500)
    unidade = models.CharField('Unidade', max_length=10)
    
    # Estoque
    estoque_minimo = models.DecimalField(
        'Estoque Mínimo',
        max_digits=15,
        decimal_places=4,
        default=Decimal('0.0000')
    )
    estoque_maximo = models.DecimalField(
        'Estoque Máximo',
        max_digits=15,
        decimal_places=4,
        default=Decimal('0.0000')
    )
    ponto_reposicao = models.DecimalField(
        'Ponto de Reposição',
        max_digits=15,
        decimal_places=4,
        default=Decimal('0.0000')
    )
    
    # Valores
    custo_medio = models.DecimalField(
        'Custo Médio',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    preco_venda = models.DecimalField(
        'Preço de Venda',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    # Informações adicionais
    ncm = models.CharField('NCM', max_length=8, blank=True)
    localizacao = models.CharField('Localização', max_length=100, blank=True)
    observacoes = models.TextField('Observações', blank=True)
    
    ativo = models.BooleanField('Ativo', default=True)
    
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['descricao']
    
    def __str__(self):
        return f"{self.codigo} - {self.descricao}"
    
    @property
    def estoque_atual(self):
        """Retorna o estoque atual do produto"""
        saldo = self.saldos.filter(ativo=True).aggregate(
            total=models.Sum('quantidade')
        )['total']
        return saldo or Decimal('0.0000')
    
    @property
    def necessita_reposicao(self):
        """Verifica se o produto necessita reposição"""
        return self.estoque_atual <= self.ponto_reposicao


class SaldoEstoque(models.Model):
    """Saldo de Estoque por Produto"""
    
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name='saldos',
        verbose_name='Produto'
    )
    
    quantidade = models.DecimalField(
        'Quantidade',
        max_digits=15,
        decimal_places=4,
        default=Decimal('0.0000')
    )
    valor_total = models.DecimalField(
        'Valor Total',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    data_ultima_movimentacao = models.DateTimeField('Última Movimentação', null=True, blank=True)
    ativo = models.BooleanField('Ativo', default=True)
    
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Saldo de Estoque'
        verbose_name_plural = 'Saldos de Estoque'
    
    def __str__(self):
        return f"{self.produto.codigo} - Qtd: {self.quantidade}"


class StockMove(models.Model):
    """Movimentação de Estoque (mantido para compatibilidade)"""
    
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='movimentacoes_antigas',
        verbose_name='Produto'
    )
    
    tipo = models.CharField('Tipo', max_length=20)  # Entrada/Saida/Transferencia
    qtd = models.IntegerField('Quantidade', default=0)
    data = models.CharField('Data', max_length=20, blank=True)  # simplificado
    obs = models.CharField('Observações', max_length=200, blank=True)
    
    class Meta:
        verbose_name = 'Movimentação de Estoque (Legado)'
        verbose_name_plural = 'Movimentações de Estoque (Legado)'



    def __str__(self):
        return str(self.name)
class MovimentacaoEstoque(models.Model):
    """Movimentação de Estoque (Nova versão expandida)"""
    
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name='movimentacoes',
        verbose_name='Produto'
    )
    
    tipo = models.CharField(
        'Tipo',
        max_length=20,
        choices=[
            ('ENTRADA', 'Entrada'),
            ('SAIDA', 'Saída'),
            ('TRANSFERENCIA', 'Transferência'),
            ('AJUSTE', 'Ajuste'),
            ('DEVOLUCAO', 'Devolução'),
        ]
    )
    
    data_movimentacao = models.DateTimeField('Data da Movimentação')
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
    
    documento_referencia = models.CharField('Documento de Referência', max_length=50, blank=True)
    observacoes = models.TextField('Observações', blank=True)
    
    # responsavel = models.ForeignKey(
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     related_name='movimentacoes_estoque',
    #     verbose_name='Responsável'
    # )
    
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Movimentação de Estoque'
        verbose_name_plural = 'Movimentações de Estoque'
        ordering = ['-data_movimentacao']
    
    def __str__(self):
        return f"{self.tipo} - {self.produto.codigo} - Qtd: {self.quantidade}"
    
    def save(self, *args, **kwargs):
        """Calcula o valor total e atualiza saldo"""
        self.valor_total = self.quantidade * self.valor_unitario
        super().save(*args, **kwargs)
        
        # Atualizar saldo do produto
        self.atualizar_saldo()
    
    def atualizar_saldo(self):
        """Atualiza o saldo do produto"""
        saldo, created = SaldoEstoque.objects.get_or_create(
            produto=self.produto,
            defaults={'quantidade': Decimal('0.0000'), 'valor_total': Decimal('0.00')}
        )
        
        if self.tipo in ['ENTRADA', 'DEVOLUCAO']:
            saldo.quantidade += self.quantidade
            saldo.valor_total += self.valor_total
        elif self.tipo in ['SAIDA', 'TRANSFERENCIA']:
            saldo.quantidade -= self.quantidade
            saldo.valor_total -= self.valor_total
        elif self.tipo == 'AJUSTE':
            # Ajuste pode ser positivo ou negativo
            saldo.quantidade = self.quantidade
        
        saldo.data_ultima_movimentacao = self.data_movimentacao
        saldo.save()


class PrevisaoDemanda(models.Model):
    """Previsão de Demanda de Produtos"""
    
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name='previsoes_demanda',
        verbose_name='Produto'
    )
    
    mes_referencia = models.DateField('Mês de Referência')
    quantidade_prevista = models.DecimalField(
        'Quantidade Prevista',
        max_digits=15,
        decimal_places=4,
        default=Decimal('0.0000')
    )
    quantidade_real = models.DecimalField(
        'Quantidade Real',
        max_digits=15,
        decimal_places=4,
        null=True,
        blank=True
    )
    
    metodo_previsao = models.CharField(
        'Método de Previsão',
        max_length=50,
        choices=[
            ('MEDIA_MOVEL', 'Média Móvel'),
            ('MEDIA_PONDERADA', 'Média Ponderada'),
            ('TENDENCIA', 'Tendência'),
            ('SAZONALIDADE', 'Sazonalidade'),
        ],
        default='MEDIA_MOVEL'
    )
    
    observacoes = models.TextField('Observações', blank=True)
    
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Previsão de Demanda'
        verbose_name_plural = 'Previsões de Demanda'
        ordering = ['-mes_referencia']
        unique_together = [['produto', 'mes_referencia']]
    
    def __str__(self):
        return f"{self.produto.codigo} - {self.mes_referencia.strftime('%m/%Y')}"
    
    @property
    def acuracia(self):
        """Calcula a acurácia da previsão"""
        if self.quantidade_real and self.quantidade_prevista > 0:
            erro = abs(self.quantidade_real - self.quantidade_prevista)
            return (1 - (erro / self.quantidade_prevista)) * 100
        return None


class CurvaABC(models.Model):
    """Curva ABC de Produtos"""
    
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name='curvas_abc',
        verbose_name='Produto'
    )
    
    periodo_inicio = models.DateField('Período Início')
    periodo_fim = models.DateField('Período Fim')
    
    valor_total_vendas = models.DecimalField(
        'Valor Total de Vendas',
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    percentual_acumulado = models.DecimalField(
        'Percentual Acumulado',
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    classificacao = models.CharField(
        'Classificação',
        max_length=1,
        choices=[
            ('A', 'Classe A (80% do valor)'),
            ('B', 'Classe B (15% do valor)'),
            ('C', 'Classe C (5% do valor)'),
        ]
    )
    
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Curva ABC'
        verbose_name_plural = 'Curvas ABC'
        ordering = ['classificacao', '-valor_total_vendas']
    
    def __str__(self):
        return f"{self.produto.codigo} - Classe {self.classificacao}"
