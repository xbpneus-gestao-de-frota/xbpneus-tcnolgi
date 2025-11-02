from django.db import models
from django.utils import timezone


class Fornecedor(models.Model):
    """Fornecedores da transportadora"""
    TIPO_CHOICES = [
        ("PF", "Pessoa Física"),
        ("PJ", "Pessoa Jurídica"),
    ]
    
    CATEGORIA_CHOICES = [
        ("PNEUS", "Pneus"),
        ("PECAS", "Peças"),
        ("COMBUSTIVEL", "Combustível"),
        ("MANUTENCAO", "Manutenção"),
        ("RECAPAGEM", "Recapagem"),
        ("SEGURO", "Seguro"),
        ("PEDAGIO", "Pedágio"),
        ("OUTRO", "Outro"),
    ]
    
    STATUS_CHOICES = [
        ("ATIVO", "Ativo"),
        ("INATIVO", "Inativo"),
        ("BLOQUEADO", "Bloqueado"),
    ]
    
    # empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='fornecedores')
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES)

    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    cpf_cnpj = models.CharField(max_length=18, unique=True)
    
    nome_razao_social = models.CharField(max_length=200)
    nome_fantasia = models.CharField(max_length=200, blank=True, null=True)
    
    inscricao_estadual = models.CharField(max_length=20, blank=True, null=True)
    inscricao_municipal = models.CharField(max_length=20, blank=True, null=True)
    
    # Endereço
    cep = models.CharField(max_length=10, blank=True, null=True)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    numero = models.CharField(max_length=20, blank=True, null=True)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    
    # Contato
    telefone = models.CharField(max_length=20, blank=True, null=True)
    celular = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    site = models.URLField(blank=True, null=True)
    
    # Dados comerciais
    prazo_pagamento = models.IntegerField(default=30, help_text='Prazo em dias')
    
    # Avaliação
    avaliacao = models.IntegerField(default=5, help_text='Avaliação de 1 a 5')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ATIVO')
    
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'
        ordering = ['nome_razao_social']
    
    def __str__(self):
        return f"{self.nome_razao_social} ({self.get_categoria_display()})"


class ContatoFornecedor(models.Model):
    """Contatos do fornecedor"""
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, related_name='contatos')
    
    nome = models.CharField(max_length=200)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    
    telefone = models.CharField(max_length=20, blank=True, null=True)
    celular = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    principal = models.BooleanField(default=False)
    
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Contato do Fornecedor'
        verbose_name_plural = 'Contatos dos Fornecedores'
        ordering = ['-principal', 'nome']
    
    def __str__(self):
        return f"{self.nome} - {self.fornecedor.nome_razao_social}"
