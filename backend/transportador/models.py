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
            """
            Cria e retorna um superusuário.  O Django exige que todos os
            campos definidos em ``REQUIRED_FIELDS`` sejam fornecidos ao
            utilizar ``createsuperuser --noinput``.  Como ``UsuarioTransportador``
            inclui ``nome_razao_social`` e ``cnpj`` em ``REQUIRED_FIELDS``,
            chamá‑lo sem esses parâmetros resultaria em ``CommandError``.  Para
            permitir a criação automática durante o provisionamento (por exemplo,
            em serviços como Render), fornecemos valores padrão caso não
            estejam presentes em ``extra_fields``.  Esses valores podem ser
            configurados via variáveis de ambiente:

            - ``DJANGO_SUPERUSER_NOME_RAZAO_SOCIAL``: nome ou razão social do
              superusuário.  Padrão: "Administrador".
            - ``DJANGO_SUPERUSER_CNPJ``: CNPJ associado ao superusuário.  Padrão:
              "00000000000000".

            Outros campos como ``is_staff``, ``is_superuser``, ``is_active``
            e ``aprovado`` são definidos como ``True`` por padrão.
            """
            import os  # importação local para evitar dependência global ao configurar

            # Definir campos obrigatórios padrão caso não fornecidos.
            extra_fields.setdefault(
                "nome_razao_social",
                os.environ.get("DJANGO_SUPERUSER_NOME_RAZAO_SOCIAL", "Administrador"),
            )
            extra_fields.setdefault(
                "cnpj",
                os.environ.get("DJANGO_SUPERUSER_CNPJ", "00000000000000"),
            )

            extra_fields.setdefault("is_staff", True)
            extra_fields.setdefault("is_superuser", True)
            extra_fields.setdefault("is_active", True)
            extra_fields.setdefault("aprovado", True)

            user = self.create_user(email, password, **extra_fields)
            # Registrar data de aprovação se ainda não definida
            if user.aprovado and not user.aprovado_em:
                user.aprovado_em = timezone.now()
                user.save(update_fields=["aprovado_em"])
            
                return user"
                ""Modelo de usuário para Transportadores"""

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
