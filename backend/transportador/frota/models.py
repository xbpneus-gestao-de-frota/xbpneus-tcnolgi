from django.db import models
from django.utils import timezone


class Vehicle(models.Model):
    """Veículo da frota"""
    TIPO_CHOICES = [
        ("CAMINHAO", "Caminhão"),
        ("CARRETA", "Carreta"),
        ("BITREM", "Bitrem"),
        ("RODOTREM", "Rodotrem"),
        ("VUC", "VUC"),
        ("OUTRO", "Outro"),
    ]
    
    STATUS_CHOICES = [
        ("ATIVO", "Ativo"),
        ("MANUTENCAO", "Em Manutenção"),
        ("INATIVO", "Inativo"),
        ("VENDIDO", "Vendido"),
    ]
    
    # Arquitetura Matriz-Filiais
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='veiculos',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa proprietária do veículo"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='veiculos',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial responsável pelo veículo"
    )
    
    placa = models.CharField(max_length=20, unique=True)

    modelo_veiculo = models.ForeignKey(
        'configuracoes.CatalogoModeloVeiculo',
        on_delete=models.PROTECT,
        related_name='veiculos_por_modelo',
        verbose_name="Modelo de Veículo",
        null=True,
        blank=True,
        help_text="Modelo de veículo do catálogo"
    )
    
    ano_fabricacao = models.IntegerField(blank=True, null=True)
    ano_modelo = models.IntegerField(blank=True, null=True)
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='CAMINHAO')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ATIVO')
    
    # Dados operacionais
    km = models.IntegerField(default=0, help_text='Quilometragem atual')
    km_ultima_manutencao = models.IntegerField(default=0)
    km_proxima_manutencao = models.IntegerField(blank=True, null=True)
    
    # Motorista atual (temporário, será substituído por vínculo)
    motorista = models.CharField(max_length=100, blank=True, null=True)
    
    # Dados técnicos
    chassi = models.CharField(max_length=50, blank=True, null=True)
    renavam = models.CharField(max_length=20, blank=True, null=True)
    capacidade_carga = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text='Capacidade em toneladas')
    
    # Eixos e pneus
    configuracao_operacional = models.ForeignKey(
        'configuracoes.OperacaoConfiguracao',
        on_delete=models.PROTECT,
        related_name='veiculos_por_operacao',
        verbose_name="Configuração Operacional",
        null=True,
        blank=True,
        help_text="Configuração de eixos e operação do veículo"
    )
    
    # Datas
    data_aquisicao = models.DateField(blank=True, null=True)
    data_venda = models.DateField(blank=True, null=True)
    
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
        ordering = ['placa']

    def __str__(self):
        return f"{self.placa} - {self.modelo_veiculo}"
    
    def precisa_manutencao(self):
        """Verifica se veículo precisa de manutenção"""
        if self.km_proxima_manutencao:
            return self.km >= self.km_proxima_manutencao
        return False
    
    def km_ate_manutencao(self):
        """Calcula KM restante até próxima manutenção"""
        if self.km_proxima_manutencao:
            return max(0, self.km_proxima_manutencao - self.km)
        return None


class Position(models.Model):
    # Arquitetura Matriz-Filiais
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='posicoes',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa proprietária da posição de pneu"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='posicoes',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial responsável pela posição de pneu"
    )

    """Posição de pneu em um veículo"""
    
    veiculo = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='posicoes_pneu')
    
    # Identificação da posição
    mapa_posicao = models.ForeignKey(
        'configuracoes.MapaPosicaoPneu',
        on_delete=models.PROTECT,
        related_name='posicoes_veiculos_mapa',
        verbose_name="Mapa de Posição",
        null=True,
        blank=True,
        help_text="Mapeamento da posição do pneu no veículo"
    )
    
    # Medida recomendada
    medida_recomendada = models.ForeignKey(
        'configuracoes.MedidaPorPosicao',
        on_delete=models.PROTECT,
        related_name='posicoes_veiculos_medida',
        verbose_name="Medida Recomendada",
        null=True,
        blank=True,
        help_text="Medida de pneu recomendada para esta posição"
    )
    
    # Pneu atual (será vinculado ao pilar de pneus)
    pneu_atual_codigo = models.CharField(max_length=50, blank=True, null=True)
    
    ordem = models.IntegerField(default=0, help_text='Ordem de exibição')
    
    class Meta:
        verbose_name = 'Posição de Pneu'
        verbose_name_plural = 'Posições de Pneus'
        ordering = ['veiculo', 'ordem']
        unique_together = ['veiculo', 'mapa_posicao']

    def __str__(self):
        return f"{self.veiculo.placa} - {self.mapa_posicao}"


class HistoricoKm(models.Model):
    # Arquitetura Matriz-Filiais
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='historicos_km',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa proprietária do histórico de KM"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='historicos_km',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial responsável pelo histórico de KM"
    )

    """Histórico de quilometragem do veículo"""
    veiculo = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='historico_km')
    
    km_anterior = models.IntegerField()
    km_atual = models.IntegerField()
    km_rodado = models.IntegerField()
    
    data_leitura = models.DateTimeField(default=timezone.now)
    origem = models.CharField(max_length=50, default='MANUAL', help_text='MANUAL, APP, TELEMETRIA')
    
    observacoes = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Histórico de KM'
        verbose_name_plural = 'Históricos de KM'
        ordering = ['-data_leitura']
    
    def __str__(self):
        return f"{self.veiculo.placa} - {self.km_atual} km"
