from django.db import models
from django.utils import timezone
class Dashboard(models.Model):
    """Dashboards configuráveis"""
    # empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='dashboards')   
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    
    padrao = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)
    
    # JSON com configuração de layout
    layout_json = models.JSONField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Dashboard'
        verbose_name_plural = 'Dashboards'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class Widget(models.Model):
    """Widgets do dashboard"""
    TIPO_CHOICES = [
        ('KPI', 'KPI'),
        ('GRAFICO_LINHA', 'Gráfico de Linha'),
        ('GRAFICO_BARRA', 'Gráfico de Barra'),
        ('GRAFICO_PIZZA', 'Gráfico de Pizza'),
        ('TABELA', 'Tabela'),
        ('MAPA', 'Mapa'),
        ('LISTA', 'Lista'),
    ]
    
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='widgets')
    
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    
    # Query ou endpoint para buscar dados
    fonte_dados = models.CharField(max_length=200)
    
    # Posição no grid
    posicao_x = models.IntegerField(default=0)
    posicao_y = models.IntegerField(default=0)
    largura = models.IntegerField(default=4)
    altura = models.IntegerField(default=4)
    
    # Configurações específicas do widget (JSON)
    configuracao_json = models.JSONField(blank=True, null=True)
    
    ativo = models.BooleanField(default=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Widget'
        verbose_name_plural = 'Widgets'
        ordering = ['dashboard', 'posicao_y', 'posicao_x']
    
    def __str__(self):
        return f"{self.dashboard.nome} - {self.titulo}"


class KPI(models.Model):
    """KPIs (Key Performance Indicators)"""
    CATEGORIA_CHOICES = [
        ('FROTA', 'Frota'),
        ('FINANCEIRO', 'Financeiro'),
        ('OPERACIONAL', 'Operacional'),
        ('MANUTENCAO', 'Manutenção'),
        ('ENTREGAS', 'Entregas'),
        ('CUSTOS', 'Custos'),
    ]
    
    # empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='kpis')
    
    nome = models.CharField(max_length=200)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    
    valor_atual = models.DecimalField(max_digits=15, decimal_places=2)
    valor_anterior = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    
    meta = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    
    unidade = models.CharField(max_length=20, help_text='Ex: R$, %, km, un')
    
    data_referencia = models.DateField(default=timezone.now)
    
    # Cálculo automático
    formula_sql = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'KPI'
        verbose_name_plural = 'KPIs'
        ordering = ['categoria', 'nome']
    
    def __str__(self):
        return f"{self.nome}: {self.valor_atual} {self.unidade}"
    
    def variacao_percentual(self):
        """Calcula variação percentual em relação ao valor anterior"""
        if not self.valor_anterior or self.valor_anterior == 0:
            return None
        return ((self.valor_atual - self.valor_anterior) / self.valor_anterior) * 100
    
    def atingiu_meta(self):
        """Verifica se atingiu a meta"""
        if not self.meta:
            return None
        return self.valor_atual >= self.meta
