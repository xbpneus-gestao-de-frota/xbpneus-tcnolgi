from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone


class UsuarioRevendaManager(BaseUserManager):
    """Manager customizado para UsuarioRevenda"""
    
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


class UsuarioRevenda(AbstractBaseUser, PermissionsMixin):
    """Modelo de usuário para Revendas"""
    
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
        related_name='revenda_users',
        related_query_name='revenda_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='revenda_users',
        related_query_name='revenda_user',
    )
    
    objects = UsuarioRevendaManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_razao_social', 'cnpj']
    
    class Meta:
        verbose_name = 'Usuário Revenda'
        verbose_name_plural = 'Usuários Revendas'
        db_table = 'revenda_usuario'
    
    def __str__(self):
        return f"{self.nome_razao_social} ({self.email})"

