from django.db import models


class Empresa(models.Model):
    """
    Modelo expandido de Empresa para suportar arquitetura Matriz-Filiais.
    Representa a empresa matriz que pode ter múltiplas filiais.
    """
    TIPOS = [
        ('transportador', 'Transportador'),
        ('revenda', 'Revenda'),
        ('borracharia', 'Borracharia'),
        ('recapagem', 'Recapagem'),
    ]
    
    # Campos básicos
    nome = models.CharField(max_length=255, verbose_name="Nome da Empresa")
    tipo = models.CharField(max_length=20, choices=TIPOS, verbose_name="Tipo de Empresa")
    cnpj = models.CharField(max_length=20, unique=True, verbose_name="CNPJ")
    
    # Campos adicionais para gestão completa
    razao_social = models.CharField(max_length=255, blank=True, verbose_name="Razão Social")
    nome_fantasia = models.CharField(max_length=255, blank=True, verbose_name="Nome Fantasia")
    inscricao_estadual = models.CharField(max_length=50, blank=True, verbose_name="Inscrição Estadual")
    inscricao_municipal = models.CharField(max_length=50, blank=True, verbose_name="Inscrição Municipal")
    
    # Endereço
    cep = models.CharField(max_length=10, blank=True, verbose_name="CEP")
    endereco = models.CharField(max_length=255, blank=True, verbose_name="Endereço")
    numero = models.CharField(max_length=20, blank=True, verbose_name="Número")
    complemento = models.CharField(max_length=100, blank=True, verbose_name="Complemento")
    bairro = models.CharField(max_length=100, blank=True, verbose_name="Bairro")
    cidade = models.CharField(max_length=100, blank=True, verbose_name="Cidade")
    estado = models.CharField(max_length=2, blank=True, verbose_name="Estado")
    
    # Contato
    telefone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    celular = models.CharField(max_length=20, blank=True, verbose_name="Celular")
    email = models.EmailField(blank=True, verbose_name="E-mail")
    site = models.URLField(blank=True, verbose_name="Site")
    
    # Configurações
    ativa = models.BooleanField(default=True, verbose_name="Empresa Ativa")
    
    # Metadados
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.nome} ({self.tipo})"


class Filial(models.Model):
    """
    Modelo de Filial vinculado a uma Empresa.
    Permite gestão multi-tenancy com separação de dados por filial.
    """
    # Relacionamento com Empresa
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='filiais',
        verbose_name="Empresa"
    )
    
    # Identificação
    codigo = models.CharField(max_length=50, verbose_name="Código da Filial")
    nome = models.CharField(max_length=255, verbose_name="Nome da Filial")
    cnpj = models.CharField(max_length=20, blank=True, verbose_name="CNPJ")
    inscricao_estadual = models.CharField(max_length=50, blank=True, verbose_name="Inscrição Estadual")
    inscricao_municipal = models.CharField(max_length=50, blank=True, verbose_name="Inscrição Municipal")
    
    # Endereço
    cep = models.CharField(max_length=10, blank=True, verbose_name="CEP")
    endereco = models.CharField(max_length=255, blank=True, verbose_name="Endereço")
    numero = models.CharField(max_length=20, blank=True, verbose_name="Número")
    complemento = models.CharField(max_length=100, blank=True, verbose_name="Complemento")
    bairro = models.CharField(max_length=100, blank=True, verbose_name="Bairro")
    cidade = models.CharField(max_length=100, blank=True, verbose_name="Cidade")
    estado = models.CharField(max_length=2, blank=True, verbose_name="Estado")
    
    # Contato
    telefone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    celular = models.CharField(max_length=20, blank=True, verbose_name="Celular")
    email = models.EmailField(blank=True, verbose_name="E-mail")
    
    # Configurações
    matriz = models.BooleanField(default=False, verbose_name="É Matriz")
    ativa = models.BooleanField(default=True, verbose_name="Filial Ativa")
    
    # Metadados
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    class Meta:
        verbose_name = "Filial"
        verbose_name_plural = "Filiais"
        ordering = ['empresa', 'codigo']
        unique_together = [['empresa', 'codigo']]
    
    def __str__(self):
        return f"{self.empresa.nome} - {self.nome} ({self.codigo})"



class Transportador(models.Model):
    """Cadastro de transportador aguardando aprovação"""
    cnpj = models.CharField(max_length=20, unique=True)
    razao = models.CharField(max_length=200)
    estado = models.CharField(max_length=2, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
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

