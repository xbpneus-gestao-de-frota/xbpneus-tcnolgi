from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone


class UsuarioTransportadorManager(BaseUserManager):
    """Manager customizado para UsuarioTransportador"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email é obrigatório")
        email = self.normalize_email(email)
        cnpj = extra_fields.pop("cnpj", None)
        aprovado = extra_fields.pop("aprovado", False)
        is_active = extra_fields.pop("is_active", True)
        user = self.model(email=email, cnpj=cnpj, aprovado=aprovado, is_active=is_active, **extra_fields)
        user.set_password(password)
        if user.aprovado and not user.aprovado_em:
            user.aprovado_em = timezone.now()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("aprovado", True)

        user = self.create_user(email, password, **extra_fields)
        if user.aprovado and not user.aprovado_em:
            user.aprovado_em = timezone.now()
            user.save(update_fields=["aprovado_em"])
        return user


class UsuarioTransportador(AbstractBaseUser, PermissionsMixin):
    """Modelo de usuário para Transportadores"""

    email = models.EmailField("E-mail", unique=True)
    nome_razao_social = models.CharField("Nome/Razão Social", max_length=200)
    cnpj = models.CharField("CNPJ", max_length=18, unique=False, null=True, blank=True)
    telefone = models.CharField("Telefone", max_length=20)
    
    # Relacionamento com Empresa
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios_transportadores',
        verbose_name='Empresa'
    )

    # Status
    is_active = models.BooleanField("Ativo", default=False)
    is_staff = models.BooleanField("Staff", default=False)
    is_superuser = models.BooleanField("Superusuário", default=False)

    # Aprovação
    aprovado = models.BooleanField("Aprovado", default=False)
    aprovado_em = models.DateTimeField("Aprovado em", null=True, blank=True)
    aprovado_por = models.CharField("Aprovado por", max_length=200, blank=True)

    # Datas
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    objects = UsuarioTransportadorManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nome_razao_social", "cnpj"]

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=('groups'),
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="usuario_transportador_set",
        related_query_name="usuario_transportador",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=('user permissions'),
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="usuario_transportador_permissions",
        related_query_name="usuario_transportador_permission",
    )


    class Meta:
        verbose_name = "Usuário Transportador"
        verbose_name_plural = "Usuários Transportadores"
        db_table = "transportador_usuario"

    def __str__(self):
        return f"{self.nome_razao_social} ({self.email})"
