from decimal import Decimal

from django.db import models
from django.utils import timezone


class Tire(models.Model):
    # Arquitetura Matriz-Filiais
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='pneus',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa proprietária do pneu"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='pneus',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial responsável pelo pneu"
    )

    """Pneu do sistema"""
    STATUS_CHOICES = [
        ("ESTOQUE", "Em Estoque"),
        ("MONTADO", "Montado"),
        ("MANUTENCAO", "Em Manutenção"),
        ("SUCATA", "Sucata"),
        ("RECAPAGEM", "Em Recapagem"),
        ("VENDIDO", "Vendido"),
    ]
    
    TIPO_CHOICES = [
        ("NOVO", "Novo"),
        ("RECAPADO", "Recapado"),
        ("REFORMADO", "Reformado"),
    ]
    
    codigo = models.CharField(max_length=100, unique=True)

    numero_fogo = models.CharField(max_length=50, blank=True, null=True, help_text='Número de fogo gravado no pneu')
    
    # Especificações
    medida = models.CharField(max_length=50)
    marca = models.CharField(max_length=50, blank=True, null=True)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='NOVO')

    # DOT e fabricação
    dot = models.CharField(max_length=10, blank=True, help_text='Data de fabricação')
    ano_fabricacao = models.IntegerField(blank=True, null=True)
    semana_fabricacao = models.IntegerField(blank=True, null=True)

    # Status e localização
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="ESTOQUE")
    posicao_atual = models.CharField(max_length=50, blank=True, default="", help_text='Placa-Posição ex: ABC1234-1E')

    # Dados de uso
    km_total = models.IntegerField(default=0, help_text='KM total rodado')
    km_atual = models.IntegerField(default=0, help_text='KM desde última montagem')
    profundidade_sulco_novo = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Profundidade do sulco quando novo (mm)'
    )
    profundidade_sulco_minimo = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Profundidade mínima aceitável do sulco (mm)'
    )
    profundidade_sulco = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Profundidade atual do sulco em mm'
    )

    # Recapagens
    numero_recapagens = models.IntegerField(default=0)
    pode_recapar = models.BooleanField(default=True)

    # Valores
    valor_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_atual = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Datas
    data_compra = models.DateField(blank=True, null=True)
    data_aquisicao = models.DateField(blank=True, null=True)
    data_montagem = models.DateField(blank=True, null=True)
    data_desmontagem = models.DateField(blank=True, null=True)
    ultima_inspecao = models.DateField(blank=True, null=True)
    proxima_inspecao = models.DateField(blank=True, null=True)

    observacoes = models.TextField(blank=True, null=True)

    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Pneu'
        verbose_name_plural = 'Pneus'
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.medida}"
    
    def vida_util_percentual(self):
        """Calcula percentual de vida útil baseado no sulco"""
        if (
            self.profundidade_sulco is None
            or self.profundidade_sulco_novo is None
            or self.profundidade_sulco_minimo is None
        ):
            return None

        intervalo_total = self.profundidade_sulco_novo - self.profundidade_sulco_minimo
        if intervalo_total <= 0:
            return None

        valor_atual = self.profundidade_sulco - self.profundidade_sulco_minimo
        percentual = (valor_atual / intervalo_total) * Decimal("100")
        return float(max(Decimal("0"), min(Decimal("100"), percentual)))
        return None

    def precisa_inspecao(self):
        """Verifica se pneu precisa de inspeção"""
        if self.proxima_inspecao and self.proxima_inspecao <= timezone.now().date():
            return True

        if (
            self.profundidade_sulco is not None
            and self.profundidade_sulco_minimo is not None
            and self.profundidade_sulco <= self.profundidade_sulco_minimo
        ):
            return True

        return False


class Application(models.Model):
    # Arquitetura Matriz-Filiais
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='aplicacoes_pneu',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa proprietária da aplicação de pneu"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='aplicacoes_pneu',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial responsável pela aplicação de pneu"
    )

    """Aplicação de pneus - Regras de uso por medida e histórico."""
    pneu = models.ForeignKey(
        Tire,
        on_delete=models.CASCADE,
        related_name='aplicacoes',
        null=True,
        blank=True,
    )
    veiculo = models.ForeignKey(
        'frota.Vehicle',
        on_delete=models.SET_NULL,
        related_name='aplicacoes_pneu',
        null=True,
        blank=True,
    )

    medida = models.CharField(max_length=50, blank=True)
    
    # Aplicabilidade
    eixos_aplicaveis = models.CharField(max_length=100, blank=True, help_text='Ex: DIANTEIRO, TRACAO, LIVRE')
    operacao = models.CharField(max_length=100, blank=True, help_text='Tipo de operação recomendada')
    
    # Especificações técnicas
    carga_maxima = models.IntegerField(blank=True, null=True, help_text='Carga máxima em kg')
    pressao_recomendada = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, help_text='Pressão em PSI')
    
    # Limites
    km_recomendado = models.IntegerField(blank=True, null=True, help_text='KM recomendado até troca')
    sulco_minimo = models.DecimalField(max_digits=4, decimal_places=2, default=1.6, help_text='Sulco mínimo legal em mm')
    
    # Histórico de montagem
    km_montagem = models.IntegerField(blank=True, null=True)
    data_montagem = models.DateField(blank=True, null=True)
    posicao = models.CharField(max_length=20, blank=True)
    km_desmontagem = models.IntegerField(blank=True, null=True)
    data_desmontagem = models.DateField(blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)

    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Aplicação de Pneu'
        verbose_name_plural = 'Aplicações de Pneus'
        ordering = ['medida']
    
    def __str__(self):
        return f"{self.medida}"


class MovimentacaoPneu(models.Model):
    # Arquitetura Matriz-Filiais
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='movimentacoes_pneu',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa proprietária da movimentação de pneu"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='movimentacoes_pneu',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial responsável pela movimentação de pneu"
    )

    """Histórico de movimentações do pneu"""
    TIPO_CHOICES = [
        ('MONTAGEM', 'Montagem'),
        ('DESMONTAGEM', 'Desmontagem'),
        ('RODIZIO', 'Rodízio'),
        ('RECAPAGEM', 'Envio para Recapagem'),
        ('RETORNO_RECAPAGEM', 'Retorno de Recapagem'),
        ('SUCATA', 'Descarte/Sucata'),
        ('VENDA', 'Venda'),
    ]
    
    pneu = models.ForeignKey(Tire, on_delete=models.CASCADE, related_name='movimentacoes')
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    
    # Origem e destino
    origem = models.CharField(max_length=100, blank=True, null=True)
    destino = models.CharField(max_length=100, blank=True, null=True)
    
    # Dados da movimentação
    km_veiculo = models.IntegerField(blank=True, null=True)
    km_pneu = models.IntegerField(blank=True, null=True)
    sulco_medicao = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    
    motivo = models.CharField(max_length=200, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    
    data_movimentacao = models.DateTimeField(default=timezone.now)
    realizado_por = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Movimentação de Pneu'
        verbose_name_plural = 'Movimentações de Pneus'
        ordering = ['-data_movimentacao']
    
    def __str__(self):
        return f"{self.pneu.codigo} - {self.get_tipo_display()}"


class MedicaoPneu(models.Model):
    # Arquitetura Matriz-Filiais
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='medicoes_pneu',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa proprietária da medição de pneu"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='medicoes_pneu',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial responsável pela medição de pneu"
    )

    """Medições de sulco e pressão do pneu"""
    pneu = models.ForeignKey(Tire, on_delete=models.CASCADE, related_name='medicoes')
    
    # Medições
    sulco = models.DecimalField(max_digits=4, decimal_places=2, help_text='Sulco médio em mm')
    sulco_externo = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, help_text='Sulco externo em mm')
    sulco_central = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, help_text='Sulco central em mm')
    sulco_interno = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, help_text='Sulco interno em mm')
    pressao = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, help_text='Pressão em PSI')
    
    # Contexto
    km_veiculo = models.IntegerField(blank=True, null=True)
    km_pneu = models.IntegerField(blank=True, null=True)
    
    # Observações
    desgaste_irregular = models.BooleanField(default=False)
    observacoes = models.TextField(blank=True, null=True)
    
    data_medicao = models.DateTimeField(default=timezone.now)
    medido_por = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Medição de Pneu'
        verbose_name_plural = 'Medições de Pneus'
        ordering = ['-data_medicao']
    
    def __str__(self):
        return f"{self.pneu.codigo} - {self.data_medicao.strftime('%d/%m/%Y')}"
    
    def sulco_medio(self):
        """Calcula sulco médio"""
        if (
            self.sulco_externo is not None
            and self.sulco_central is not None
            and self.sulco_interno is not None
        ):
            return (self.sulco_externo + self.sulco_central + self.sulco_interno) / 3
        return self.sulco
