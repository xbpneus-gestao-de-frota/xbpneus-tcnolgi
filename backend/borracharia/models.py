from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from decimal import Decimal
from backend.transportador.empresas.models import Empresa


class UsuarioBorrachariaManager(BaseUserManager):
    """Manager customizado para UsuarioBorracharia"""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('aprovado', True)
        return self.create_user(email, password, **extra_fields)


class UsuarioBorracharia(AbstractBaseUser, PermissionsMixin):
    """Modelo de usuário para Borracharias"""
    
    email = models.EmailField('E-mail', unique=True)
    nome_razao_social = models.CharField('Nome/Razão Social', max_length=200)
    cnpj = models.CharField('CNPJ', max_length=18, unique=True)
    telefone = models.CharField('Telefone', max_length=20)
    endereco = models.TextField('Endereço', blank=True)
    
    # Status
    is_active = models.BooleanField('Ativo', default=False)
    is_staff = models.BooleanField('Staff', default=False)
    is_superuser = models.BooleanField('Superusuário', default=False)
    
    # Aprovação
    aprovado = models.BooleanField('Aprovado', default=False)
    aprovado_em = models.DateTimeField('Aprovado em', null=True, blank=True)
    aprovado_por = models.CharField('Aprovado por', max_length=200, blank=True)
    
    # Datas
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    
    # Fix para conflitos de related_name
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='borracharia_users',
        related_query_name='borracharia_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='borracharia_users',
        related_query_name='borracharia_user',
    )
    
    objects = UsuarioBorrachariaManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_razao_social', 'cnpj']
    
    class Meta:
        verbose_name = 'Usuário Borracharia'
        verbose_name_plural = 'Usuários Borracharias'
        db_table = 'borracharia_usuario'
    
    def __str__(self):
        return f"{self.nome_razao_social} ({self.email})"


# Model original mantido
class Borracharia(models.Model):
    """Cadastro básico de borracharia (mantido para compatibilidade)"""
    cnpjcpf = models.CharField(max_length=20)
    razao = models.CharField(max_length=200)
    estado = models.CharField(max_length=2)
    cidade = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)
    status = models.CharField(
        max_length=20,
        choices=[("PENDENTE", "Pendente"), ("APROVADO", "Aprovado"), ("RECUSADO", "Recusado")],
        default="PENDENTE",
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.razao


# Novos models completos para gestão de borracharia

class ClienteBorracharia(models.Model):
    """Cliente da borracharia (geralmente transportadoras)"""
    TIPO_CHOICES = [
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
    ]
    
    STATUS_CHOICES = [
        ('Ativo', 'Ativo'),
        ('Inativo', 'Inativo'),
        ('Bloqueado', 'Bloqueado'),
    ]
    
    borracharia = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='clientes_borracharia')
    
    # Dados básicos
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES, default='PJ')
    cpf_cnpj = models.CharField(max_length=18, unique=True)
    nome_razao_social = models.CharField(max_length=200)
    nome_fantasia = models.CharField(max_length=200, blank=True, null=True)
    
    # Contato
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    celular = models.CharField(max_length=20, blank=True, null=True)
    
    # Endereço
    cep = models.CharField(max_length=10, blank=True, null=True)
    logradouro = models.CharField(max_length=200, blank=True, null=True)
    numero = models.CharField(max_length=20, blank=True, null=True)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    
    # Financeiro
    limite_credito = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    saldo_devedor = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    prazo_pagamento = models.IntegerField(default=30, help_text='Prazo em dias')
    
    # Controle
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Ativo')
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'borracharia_cliente'
        verbose_name = 'Cliente Borracharia'
        verbose_name_plural = 'Clientes Borracharia'
        ordering = ['nome_razao_social']
    
    def __str__(self):
        return f"{self.nome_razao_social} - {self.cpf_cnpj}"


class TipoServicoBorracharia(models.Model):
    """Tipos de serviços oferecidos pela borracharia"""
    borracharia = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='tipos_servico_borracharia')
    
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    preco_padrao = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tempo_estimado = models.IntegerField(help_text='Tempo em minutos', default=30)
    ativo = models.BooleanField(default=True)
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'borracharia_tipo_servico'
        verbose_name = 'Tipo de Serviço'
        verbose_name_plural = 'Tipos de Serviço'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class OrcamentoBorracharia(models.Model):
    """Orçamento de serviços para clientes"""
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Enviado', 'Enviado'),
        ('Aprovado', 'Aprovado'),
        ('Recusado', 'Recusado'),
        ('Expirado', 'Expirado'),
    ]
    
    borracharia = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='orcamentos_borracharia')
    cliente = models.ForeignKey(ClienteBorracharia, on_delete=models.CASCADE, related_name='orcamentos')
    
    numero = models.CharField(max_length=20, unique=True)
    data_emissao = models.DateField(default=timezone.now)
    data_validade = models.DateField()
    
    # Dados do veículo (se aplicável)
    placa_veiculo = models.CharField(max_length=20, blank=True, null=True)
    modelo_veiculo = models.CharField(max_length=100, blank=True, null=True)
    
    # Valores
    valor_servicos = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    valor_pecas = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pendente')
    observacoes = models.TextField(blank=True, null=True)
    
    # Integração com transportador
    transportador_empresa_id = models.IntegerField(blank=True, null=True, help_text='ID da empresa transportadora')
    enviado_transportador = models.BooleanField(default=False)
    data_envio_transportador = models.DateTimeField(blank=True, null=True)
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'borracharia_orcamento'
        verbose_name = 'Orçamento'
        verbose_name_plural = 'Orçamentos'
        ordering = ['-data_emissao']
    
    def __str__(self):
        return f"Orçamento {self.numero} - {self.cliente.nome_razao_social}"
    
    def calcular_total(self):
        self.valor_total = self.valor_servicos + self.valor_pecas - self.desconto
        return self.valor_total


class ItemOrcamentoBorracharia(models.Model):
    """Itens do orçamento"""
    TIPO_CHOICES = [
        ('Servico', 'Serviço'),
        ('Peca', 'Peça'),
    ]
    
    orcamento = models.ForeignKey(OrcamentoBorracharia, on_delete=models.CASCADE, related_name='itens')
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='Servico')
    tipo_servico = models.ForeignKey(TipoServicoBorracharia, on_delete=models.SET_NULL, null=True, blank=True, related_name='itens_orcamento')
    
    descricao = models.CharField(max_length=200)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1.00'))
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'borracharia_item_orcamento'
        verbose_name = 'Item de Orçamento'
        verbose_name_plural = 'Itens de Orçamento'
    
    def __str__(self):
        return f"{self.descricao} - {self.quantidade}x R$ {self.valor_unitario}"
    
    def calcular_total(self):
        self.valor_total = self.quantidade * self.valor_unitario
        return self.valor_total


class OrdemServicoBorracharia(models.Model):
    """Ordem de serviço da borracharia"""
    STATUS_CHOICES = [
        ('Aberta', 'Aberta'),
        ('Em Andamento', 'Em Andamento'),
        ('Aguardando Peças', 'Aguardando Peças'),
        ('Concluída', 'Concluída'),
        ('Cancelada', 'Cancelada'),
    ]
    
    borracharia = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='ordens_servico_borracharia')
    cliente = models.ForeignKey(ClienteBorracharia, on_delete=models.CASCADE, related_name='ordens_servico')
    orcamento = models.ForeignKey(OrcamentoBorracharia, on_delete=models.SET_NULL, null=True, blank=True, related_name='ordens_servico')
    
    numero = models.CharField(max_length=20, unique=True)
    data_abertura = models.DateTimeField(default=timezone.now)
    data_prevista = models.DateField(blank=True, null=True)
    data_conclusao = models.DateTimeField(blank=True, null=True)
    
    # Dados do veículo
    placa_veiculo = models.CharField(max_length=20)
    modelo_veiculo = models.CharField(max_length=100, blank=True, null=True)
    km_veiculo = models.IntegerField(blank=True, null=True)
    
    # Valores
    valor_servicos = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    valor_pecas = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Aberta')
    observacoes = models.TextField(blank=True, null=True)
    
    # Integração com transportador
    transportador_empresa_id = models.IntegerField(blank=True, null=True)
    transportador_os_id = models.IntegerField(blank=True, null=True, help_text='ID da OS no sistema do transportador')
    enviado_transportador = models.BooleanField(default=False)
    data_envio_transportador = models.DateTimeField(blank=True, null=True)
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'borracharia_ordem_servico'
        verbose_name = 'Ordem de Serviço'
        verbose_name_plural = 'Ordens de Serviço'
        ordering = ['-data_abertura']
    
    def __str__(self):
        return f"OS {self.numero} - {self.placa_veiculo}"
    
    def calcular_total(self):
        self.valor_total = self.valor_servicos + self.valor_pecas - self.desconto
        return self.valor_total


class ItemOrdemServicoBorracharia(models.Model):
    """Itens da ordem de serviço"""
    TIPO_CHOICES = [
        ('Servico', 'Serviço'),
        ('Peca', 'Peça'),
    ]
    
    ordem_servico = models.ForeignKey(OrdemServicoBorracharia, on_delete=models.CASCADE, related_name='itens')
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='Servico')
    tipo_servico = models.ForeignKey(TipoServicoBorracharia, on_delete=models.SET_NULL, null=True, blank=True, related_name='itens_os')
    
    descricao = models.CharField(max_length=200)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1.00'))
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    concluido = models.BooleanField(default=False)
    data_conclusao = models.DateTimeField(blank=True, null=True)
    
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'borracharia_item_os'
        verbose_name = 'Item de OS'
        verbose_name_plural = 'Itens de OS'
    
    def __str__(self):
        return f"{self.descricao} - {self.quantidade}x R$ {self.valor_unitario}"
    
    def calcular_total(self):
        self.valor_total = self.quantidade * self.valor_unitario
        return self.valor_total


class EstoquePneuBorracharia(models.Model):
    """Estoque de pneus da borracharia"""
    STATUS_CHOICES = [
        ('Disponivel', 'Disponível'),
        ('Reservado', 'Reservado'),
        ('Vendido', 'Vendido'),
        ('Descartado', 'Descartado'),
    ]
    
    borracharia = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='estoque_pneus_borracharia')
    
    numero_fogo = models.CharField(max_length=50, unique=True)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    medida = models.CharField(max_length=50)
    dot = models.CharField(max_length=10, blank=True, null=True)
    
    tipo = models.CharField(max_length=50, choices=[
        ('Novo', 'Novo'),
        ('Recapado', 'Recapado'),
        ('Usado', 'Usado'),
    ], default='Novo')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Disponivel')
    
    # Valores
    valor_compra = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    valor_venda = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    # Localização
    localizacao = models.CharField(max_length=100, blank=True, null=True)
    
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'borracharia_estoque_pneu'
        verbose_name = 'Estoque de Pneu'
        verbose_name_plural = 'Estoque de Pneus'
        ordering = ['numero_fogo']
    
    def __str__(self):
        return f"{self.numero_fogo} - {self.marca} {self.modelo} {self.medida}"


class NotaFiscalBorracharia(models.Model):
    """Notas fiscais emitidas pela borracharia"""
    TIPO_CHOICES = [
        ('Servico', 'Serviço'),
        ('Produto', 'Produto'),
        ('Mista', 'Mista'),
    ]
    
    STATUS_CHOICES = [
        ('Emitida', 'Emitida'),
        ('Cancelada', 'Cancelada'),
        ('Denegada', 'Denegada'),
    ]
    
    borracharia = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='notas_fiscais_borracharia')
    cliente = models.ForeignKey(ClienteBorracharia, on_delete=models.CASCADE, related_name='notas_fiscais')
    ordem_servico = models.ForeignKey(OrdemServicoBorracharia, on_delete=models.SET_NULL, null=True, blank=True, related_name='notas_fiscais')
    
    numero = models.CharField(max_length=20, unique=True)
    serie = models.CharField(max_length=10, default='1')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='Servico')
    
    data_emissao = models.DateTimeField(default=timezone.now)
    chave_acesso = models.CharField(max_length=44, blank=True, null=True)
    
    # Valores
    valor_servicos = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    valor_produtos = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    valor_desconto = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    # Impostos
    valor_iss = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    valor_icms = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Emitida')
    
    # Integração com transportador
    enviado_transportador = models.BooleanField(default=False)
    data_envio_transportador = models.DateTimeField(blank=True, null=True)
    
    # Arquivo XML
    xml_nfe = models.TextField(blank=True, null=True)
    
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'borracharia_nota_fiscal'
        verbose_name = 'Nota Fiscal'
        verbose_name_plural = 'Notas Fiscais'
        ordering = ['-data_emissao']
    
    def __str__(self):
        return f"NF {self.numero}/{self.serie} - {self.cliente.nome_razao_social}"


class ContaReceberBorracharia(models.Model):
    """Contas a receber da borracharia"""
    STATUS_CHOICES = [
        ('Aberta', 'Aberta'),
        ('Paga', 'Paga'),
        ('Vencida', 'Vencida'),
        ('Cancelada', 'Cancelada'),
    ]
    
    borracharia = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='contas_receber_borracharia')
    cliente = models.ForeignKey(ClienteBorracharia, on_delete=models.CASCADE, related_name='contas_receber')
    ordem_servico = models.ForeignKey(OrdemServicoBorracharia, on_delete=models.SET_NULL, null=True, blank=True, related_name='contas_receber')
    nota_fiscal = models.ForeignKey(NotaFiscalBorracharia, on_delete=models.SET_NULL, null=True, blank=True, related_name='contas_receber')
    
    numero = models.CharField(max_length=20, unique=True)
    descricao = models.CharField(max_length=200)
    
    data_emissao = models.DateField(default=timezone.now)
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(blank=True, null=True)
    
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    juros = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Aberta')
    
    forma_pagamento = models.CharField(max_length=50, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'borracharia_conta_receber'
        verbose_name = 'Conta a Receber'
        verbose_name_plural = 'Contas a Receber'
        ordering = ['data_vencimento']
    
    def __str__(self):
        return f"Conta {self.numero} - {self.cliente.nome_razao_social} - R$ {self.valor}"
