from django.db import models
from django.utils import timezone
from backend.transportador.empresas.models import Empresa


class CategoriaProduto(models.Model):
    """Categorias de produtos na loja"""
    TIPO_CHOICES = [
        ('PNEU', 'Pneu'),
        ('SERVICO', 'Serviço'),
        ('PECA', 'Peça'),
        ('ACESSORIO', 'Acessório'),
        ('OUTRO', 'Outro'),
    ]
    
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='OUTRO')
    descricao = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Categoria de Produto'
        verbose_name_plural = 'Categorias de Produtos'
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"


class Produto(models.Model):
    """Produtos disponíveis na loja do transportador"""
    STATUS_CHOICES = [
        ('DISPONIVEL', 'Disponível'),
        ('INDISPONIVEL', 'Indisponível'),
        ('DESCONTINUADO', 'Descontinuado'),
    ]
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='produtos_loja')
    categoria = models.ForeignKey(CategoriaProduto, on_delete=models.SET_NULL, null=True, related_name='produtos')
    
    codigo = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    
    # Preços
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    margem_lucro = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Percentual
    
    # Estoque
    quantidade_estoque = models.IntegerField(default=0)
    estoque_minimo = models.IntegerField(default=0)
    
    # Informações adicionais
    unidade_medida = models.CharField(max_length=20, default='UN')  # UN, KG, L, etc
    fabricante = models.CharField(max_length=100, blank=True, null=True)
    codigo_fabricante = models.CharField(max_length=50, blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DISPONIVEL')
    ativo = models.BooleanField(default=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.codigo} - {self.nome}"
    
    def calcular_margem(self):
        """Calcula margem de lucro baseada nos preços"""
        if self.preco_custo > 0:
            self.margem_lucro = ((self.preco_venda - self.preco_custo) / self.preco_custo) * 100
        return self.margem_lucro
    
    def estoque_baixo(self):
        """Verifica se estoque está abaixo do mínimo"""
        return self.quantidade_estoque <= self.estoque_minimo


class Pedido(models.Model):
    """Pedidos realizados na loja"""
    STATUS_CHOICES = [
        ('ORCAMENTO', 'Orçamento'),
        ('PENDENTE', 'Pendente'),
        ('CONFIRMADO', 'Confirmado'),
        ('EM_SEPARACAO', 'Em Separação'),
        ('PRONTO', 'Pronto para Retirada'),
        ('ENTREGUE', 'Entregue'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    TIPO_CHOICES = [
        ('VENDA', 'Venda'),
        ('ORCAMENTO', 'Orçamento'),
        ('TROCA', 'Troca'),
        ('GARANTIA', 'Garantia'),
    ]
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='pedidos_loja')
    numero_pedido = models.CharField(max_length=50, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='VENDA')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    
    # Cliente (pode ser interno ou externo)
    cliente_nome = models.CharField(max_length=200)
    cliente_documento = models.CharField(max_length=20, blank=True, null=True)
    cliente_telefone = models.CharField(max_length=20, blank=True, null=True)
    cliente_email = models.EmailField(blank=True, null=True)
    
    # Valores
    valor_produtos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Observações
    observacoes = models.TextField(blank=True, null=True)
    observacoes_internas = models.TextField(blank=True, null=True)
    
    # Datas
    data_pedido = models.DateTimeField(default=timezone.now)
    data_confirmacao = models.DateTimeField(blank=True, null=True)
    data_entrega = models.DateTimeField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-data_pedido']
    
    def __str__(self):
        return f"Pedido {self.numero_pedido} - {self.cliente_nome}"
    
    def calcular_total(self):
        """Calcula o valor total do pedido"""
        self.valor_produtos = sum(item.valor_total for item in self.itens.all())
        self.valor_total = self.valor_produtos - self.valor_desconto
        return self.valor_total


class ItemPedido(models.Model):
    """Itens de um pedido"""
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='itens_pedido')
    
    quantidade = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    observacoes = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Item de Pedido'
        verbose_name_plural = 'Itens de Pedido'
    
    def __str__(self):
        return f"{self.produto.nome} x {self.quantidade}"
    
    def calcular_valor_total(self):
        """Calcula o valor total do item"""
        self.valor_total = (self.preco_unitario * self.quantidade) - self.desconto
        return self.valor_total
    
    def save(self, *args, **kwargs):
        self.calcular_valor_total()
        super().save(*args, **kwargs)


class MovimentacaoEstoqueLoja(models.Model):
    """Movimentações de estoque da loja"""
    TIPO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SAIDA', 'Saída'),
        ('AJUSTE', 'Ajuste'),
        ('TRANSFERENCIA', 'Transferência'),
        ('DEVOLUCAO', 'Devolução'),
    ]
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='movimentacoes_loja')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='movimentacoes')
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True, blank=True, related_name='movimentacoes')
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_anterior = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_nova = models.DecimalField(max_digits=10, decimal_places=2)
    
    motivo = models.CharField(max_length=200, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    
    data_movimentacao = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Movimentação de Estoque'
        verbose_name_plural = 'Movimentações de Estoque'
        ordering = ['-data_movimentacao']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.produto.nome} - {self.quantidade}"
