from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone


class UsuarioMotoristaManager(BaseUserManager):
    """Manager customizado para UsuarioMotorista"""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email é obrigatório')

        email = self.normalize_email(email)
        aprovado = extra_fields.pop('aprovado', False)
        is_active = extra_fields.pop('is_active', False)

        user = self.model(email=email, aprovado=aprovado, is_active=is_active, **extra_fields)
        user.set_password(password)

        if user.aprovado and not user.aprovado_em:
            user.aprovado_em = timezone.now()

        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('aprovado', True)

        user = self.create_user(email, password, **extra_fields)

        if user.aprovado and not user.aprovado_em:
            user.aprovado_em = timezone.now()
            user.save(update_fields=['aprovado_em'])

        return user


class UsuarioMotorista(AbstractBaseUser, PermissionsMixin):
    """Modelo de usuário para Motoristas"""
    
    email = models.EmailField('E-mail', unique=True)
    nome_completo = models.CharField('Nome Completo', max_length=200)
    cpf = models.CharField('CPF', max_length=14, unique=True)
    cnh = models.CharField('CNH', max_length=20, unique=True)
    categoria_cnh = models.CharField('Categoria CNH', max_length=5)
    telefone = models.CharField('Telefone', max_length=20)
    
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
        related_name='motorista_users',
        related_query_name='motorista_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='motorista_users',
        related_query_name='motorista_user',
    )
    
    objects = UsuarioMotoristaManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_completo', 'cpf', 'cnh']
    
    class Meta:
        verbose_name = 'Usuário Motorista'
        verbose_name_plural = 'Usuários Motoristas'
        db_table = 'motorista_usuario'
    
    def __str__(self):
        return f"{self.nome_completo} ({self.email})"

