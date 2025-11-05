import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone


class Command(BaseCommand):
    help = "Garante que um superusuário aprovado exista com dados vindos do ambiente."

    def handle(self, *args, **options):
        user_model = get_user_model()

        email = os.getenv("ADMIN_EMAIL") or os.getenv("DJANGO_SUPERUSER_EMAIL")
        password = os.getenv("ADMIN_PASSWORD") or os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not email:
            raise CommandError(
                "Defina ADMIN_EMAIL ou DJANGO_SUPERUSER_EMAIL para criar o superusuário."
            )

        if not password:
            raise CommandError(
                "Defina ADMIN_PASSWORD ou DJANGO_SUPERUSER_PASSWORD para criar o superusuário."
            )

        nome = (
            os.getenv("ADMIN_NAME")
            or os.getenv("DJANGO_SUPERUSER_NOME_RAZAO_SOCIAL")
            or "Administrador"
        )
        cnpj = os.getenv("ADMIN_CNPJ") or os.getenv("DJANGO_SUPERUSER_CNPJ") or "00000000000000"
        telefone = (
            os.getenv("ADMIN_PHONE")
            or os.getenv("DJANGO_SUPERUSER_TELEFONE")
            or "0000000000"
        )

        defaults = {
            "nome_razao_social": nome,
            "cnpj": cnpj,
            "telefone": telefone,
            "is_staff": True,
            "is_superuser": True,
            "is_active": True,
            "aprovado": True,
        }

        user, created = user_model.objects.get_or_create(email=email, defaults=defaults)

        if not created:
            updated = False
            for field, value in defaults.items():
                if getattr(user, field) != value:
                    setattr(user, field, value)
                    updated = True

            if updated:
                self.stdout.write(
                    self.style.WARNING(
                        "Atualizando campos obrigatórios do superusuário existente."
                    )
                )

        user.set_password(password)

        if user.aprovado and not user.aprovado_em:
            user.aprovado_em = timezone.now()

        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS("Superusuário criado."))
        else:
            self.stdout.write(self.style.SUCCESS("Superusuário atualizado."))
