from django.conf import settings
"""
Models para o módulo de Configuracoes
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class ConfiguracaoSistema(models.Model):
    """Model ConfiguracaoSistema"""
    
    # Relacionamentos
    # empresa = models.ForeignKey(
    #     on_delete=models.CASCADE,
    #     related_name='configuracoes_configuracaosistema',
    #     verbose_name='Empresa'
    # )
    
    # Dados básicos
    nome = models.CharField('Nome', max_length=200)
    descricao = models.TextField('Descrição', blank=True)
    ativo = models.BooleanField('Ativo', default=True)
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='configuracoes_configuracaosistema_criado',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'ConfiguracaoSistema'
        verbose_name_plural = 'ConfiguracaoSistemas'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class ParametroEmpresa(models.Model):
    """Model ParametroEmpresa"""
    
    # Relacionamentos
    # empresa = models.ForeignKey(
    #     on_delete=models.CASCADE,
    #     related_name='configuracoes_parametroempresa',
    #     verbose_name='Empresa'
    # )
    
    # Dados básicos
    nome = models.CharField('Nome', max_length=200)
    descricao = models.TextField('Descrição', blank=True)
    ativo = models.BooleanField('Ativo', default=True)
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='configuracoes_parametroempresa_criado',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'ParametroEmpresa'
        verbose_name_plural = 'ParametroEmpresas'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class PerfilUsuario(models.Model):
    """Model PerfilUsuario"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='configuracoes_perfilusuario',
        verbose_name='Empresa'
    )
    
    # Dados básicos
    nome = models.CharField('Nome', max_length=200)
    descricao = models.TextField('Descrição', blank=True)
    ativo = models.BooleanField('Ativo', default=True)
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    # criado_por = models.ForeignKey(
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     related_name='configuracoes_perfilusuario_criado',
    #     verbose_name='Criado por'
    # )
    
    class Meta:
        verbose_name = 'PerfilUsuario'
        verbose_name_plural = 'PerfilUsuarios'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class PermissaoCustomizada(models.Model):
    """Model PermissaoCustomizada"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='configuracoes_permissaocustomizada',
        verbose_name='Empresa'
    )
    
    # Dados básicos
    nome = models.CharField('Nome', max_length=200)
    descricao = models.TextField('Descrição', blank=True)
    ativo = models.BooleanField('Ativo', default=True)
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    # criado_por = models.ForeignKey(
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     related_name='configuracoes_permissaocustomizada_criado',
    #     verbose_name='Criado por'
    # )
    
    class Meta:
        verbose_name = 'PermissaoCustomizada'
        verbose_name_plural = 'PermissaoCustomizadas'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome





# =============================================================================
# TABELAS AUXILIARES - CATÁLOGOS E CONFIGURAÇÕES
# =============================================================================


class CatalogoModeloVeiculo(models.Model):
    """
    Catálogo de modelos de veículos (caminhões, ônibus, vans)
    com configurações de eixos e períodos de fabricação.
    """
    
    CATEGORIA_CHOICES = [
        ('CAMINHAO_TRATOR', 'Caminhão/Trator'),
        ('CAMINHAO_RIGIDO', 'Caminhão Rígido'),
        ('ONIBUS_CHASSI', 'Ônibus (Chassi)'),
        ('VANS', 'Vans'),
    ]
    
    categoria = models.CharField('Categoria', max_length=50, choices=CATEGORIA_CHOICES)
    marca = models.CharField('Marca', max_length=100)
    familia_modelo = models.CharField('Família/Modelo', max_length=100)
    variante = models.CharField('Variante', max_length=200)
    ano_inicio = models.IntegerField('Ano Início', validators=[MinValueValidator(1900)])
    ano_fim = models.IntegerField('Ano Fim', validators=[MinValueValidator(1900)])
    configuracoes = models.TextField('Configurações', help_text='Configurações de eixos separadas por |')
    observacoes = models.TextField('Observações', blank=True)
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Catálogo de Modelo de Veículo'
        verbose_name_plural = 'Catálogo de Modelos de Veículos'
        ordering = ['marca', 'familia_modelo', 'ano_inicio']
        indexes = [
            models.Index(fields=['marca', 'familia_modelo']),
            models.Index(fields=['categoria']),
        ]
    
    def __str__(self):
        return f"{self.marca} {self.familia_modelo} ({self.variante})"


class MapaPosicaoPneu(models.Model):
    """
    Mapeamento de posições de pneus por configuração de eixos.
    Define cada posição específica onde um pneu pode ser instalado.
    """
    
    COMPONENTE_CHOICES = [
        ('T', 'Trator'),
        ('R', 'Rígido'),
        ('SR1', 'Semi-reboque 1'),
        ('SR2', 'Semi-reboque 2'),
        ('DOL', 'Dolly'),
    ]
    
    LADO_CHOICES = [
        ('L', 'Esquerdo'),
        ('R', 'Direito'),
    ]
    
    RODADO_CHOICES = [
        ('S', 'Singelo'),
        ('IN', 'Interno (Duplo)'),
        ('EX', 'Externo (Duplo)'),
    ]
    
    POSICAO_TIPO_CHOICES = [
        ('direcao', 'Direção'),
        ('tracao', 'Tração'),
        ('auxiliar', 'Auxiliar'),
        ('sr', 'Semi-reboque'),
        ('dolly', 'Dolly'),
    ]
    
    config_id = models.CharField('Config ID', max_length=50, db_index=True)
    componente = models.CharField('Componente', max_length=10, choices=COMPONENTE_CHOICES)
    eixo = models.IntegerField('Eixo', validators=[MinValueValidator(1)])
    lado = models.CharField('Lado', max_length=1, choices=LADO_CHOICES)
    rodado = models.CharField('Rodado', max_length=2, choices=RODADO_CHOICES)
    posicao_tipo = models.CharField('Tipo de Posição', max_length=20, choices=POSICAO_TIPO_CHOICES)
    position_id = models.CharField('Position ID', max_length=50, db_index=True)
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Mapa de Posição de Pneu'
        verbose_name_plural = 'Mapa de Posições de Pneus'
        ordering = ['config_id', 'componente', 'eixo', 'lado', 'rodado']
        unique_together = [['config_id', 'componente', 'eixo', 'lado', 'rodado']]
        indexes = [
            models.Index(fields=['config_id', 'posicao_tipo']),
            models.Index(fields=['position_id']),
        ]
    
    def __str__(self):
        return f"{self.config_id} - {self.position_id}"


class OperacaoConfiguracao(models.Model):
    """
    Tipos de operação (rodoviário, urbano, off-road) com 
    configurações de eixos e implementos recomendados.
    """
    
    op_code = models.CharField('Código da Operação', max_length=50, unique=True, db_index=True)
    config_ids_recomendados = models.TextField('Configs Recomendadas', help_text='IDs separados por |')
    implementos_recomendados = models.TextField('Implementos Recomendados')
    eixos_tipicos = models.CharField('Eixos Típicos', max_length=50)
    pbtc_faixa_aprox_t = models.CharField('PBTC Faixa Aprox (t)', max_length=50)
    observacoes = models.TextField('Observações', blank=True)
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Operação e Configuração'
        verbose_name_plural = 'Operações e Configurações'
        ordering = ['op_code']
        indexes = [
            models.Index(fields=['op_code']),
        ]
    
    def __str__(self):
        return f"{self.op_code} - {self.implementos_recomendados[:50]}"


class MedidaPorPosicao(models.Model):
    """
    Medidas de pneus típicas recomendadas para cada tipo de posição
    em diferentes configurações de veículos.
    """
    
    config_id = models.CharField('Config ID', max_length=50, db_index=True)
    posicao_tipo = models.CharField('Tipo de Posição', max_length=20)
    medidas_tipicas = models.TextField('Medidas Típicas', help_text='Medidas separadas por ;')
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Medida por Posição'
        verbose_name_plural = 'Medidas por Posição'
        ordering = ['config_id', 'posicao_tipo']
        unique_together = [['config_id', 'posicao_tipo']]
        indexes = [
            models.Index(fields=['config_id', 'posicao_tipo']),
        ]
    
    def __str__(self):
        return f"{self.config_id} - {self.posicao_tipo}"


class PressaoRecomendada(models.Model):
    """
    Faixas de pressão recomendadas (PSI) por categoria de veículo,
    configuração e tipo de posição.
    """
    
    CATEGORIA_CHOICES = [
        ('CAMINHAO_TRATOR', 'Caminhão/Trator'),
        ('CAMINHAO_RIGIDO', 'Caminhão Rígido'),
        ('IMPLEMENTO_SR', 'Implemento (SR)'),
        ('COMBINADO', 'Combinado'),
        ('ONIBUS', 'Ônibus'),
        ('VANS', 'Vans'),
    ]
    
    categoria = models.CharField('Categoria', max_length=50, choices=CATEGORIA_CHOICES)
    config_id = models.CharField('Config ID', max_length=50, blank=True)
    posicao_tipo = models.CharField('Tipo de Posição', max_length=20)
    medida_exemplo = models.CharField('Medida Exemplo', max_length=50)
    faixa_psi_min = models.IntegerField('PSI Mínimo', validators=[MinValueValidator(0)])
    faixa_psi_max = models.IntegerField('PSI Máximo', validators=[MinValueValidator(0)])
    observacoes = models.TextField('Observações', blank=True)
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Pressão Recomendada'
        verbose_name_plural = 'Pressões Recomendadas'
        ordering = ['categoria', 'config_id', 'posicao_tipo']
        indexes = [
            models.Index(fields=['categoria', 'config_id']),
            models.Index(fields=['posicao_tipo']),
        ]
    
    def __str__(self):
        return f"{self.categoria} - {self.posicao_tipo} ({self.faixa_psi_min}-{self.faixa_psi_max} PSI)"


class CatalogoPneuXBRI(models.Model):
    """
    Catálogo de pneus XBRI com especificações técnicas completas.
    """
    
    linha = models.CharField('Linha', max_length=50, db_index=True)
    modelo = models.CharField('Modelo', max_length=100)
    medida = models.CharField('Medida', max_length=50, db_index=True)
    ply_rating = models.CharField('Ply Rating', max_length=20)
    aro_recomendado = models.CharField('Aro Recomendado', max_length=20)
    indice_carga = models.CharField('Índice de Carga', max_length=50)
    indice_velocidade = models.CharField('Índice de Velocidade', max_length=10)
    largura_banda_mm = models.DecimalField('Largura Banda (mm)', max_digits=6, decimal_places=1, null=True, blank=True)
    largura_secao_mm = models.DecimalField('Largura Seção (mm)', max_digits=6, decimal_places=1, null=True, blank=True)
    profundidade_sulco_mm = models.DecimalField('Profundidade Sulco (mm)', max_digits=5, decimal_places=1, null=True, blank=True)
    diametro_externo_mm = models.IntegerField('Diâmetro Externo (mm)', null=True, blank=True)
    pressao_max_psi = models.DecimalField('Pressão Máx (PSI)', max_digits=6, decimal_places=2, null=True, blank=True)
    fonte = models.URLField('Fonte', max_length=500, blank=True)
    li_single_num = models.IntegerField('LI Single', null=True, blank=True)
    li_dual_num = models.IntegerField('LI Dual', null=True, blank=True)
    linha_canonica = models.CharField('Linha Canônica', max_length=100)
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Catálogo de Pneu XBRI'
        verbose_name_plural = 'Catálogo de Pneus XBRI'
        ordering = ['linha', 'modelo', 'medida']
        indexes = [
            models.Index(fields=['linha', 'modelo']),
            models.Index(fields=['medida']),
            models.Index(fields=['linha_canonica']),
        ]
    
    def __str__(self):
        return f"{self.linha} {self.modelo} - {self.medida}"

