from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from backend.transportador.models import UsuarioTransportador


class Command(BaseCommand):
    help = "Garante um superadmin aprovado e ativo."

    def handle(self, *args, **options):
        email = getattr(settings, "ADMIN_EMAIL", None) or "catanharacing@gmail.com"
        password = getattr(settings, "ADMIN_PASSWORD", None) or "fer69@HOTMAIL"

        defaults = {
            "nome_razao_social": "XBP Admin",
            "cnpj": "00000000000000",
            "telefone": "0000000000",
            "is_staff": True,
            "is_superuser": True,
            "aprovado": True,
            "is_active": True,
        }

        user, created = UsuarioTransportador.objects.get_or_create(email=email, defaults=defaults)
        changed = False

        for field, value in defaults.items():
            if getattr(user, field) != value:
                setattr(user, field, value)
                changed = True

        if not user.check_password(password):
            user.set_password(password)
            changed = True

        if user.aprovado and not user.aprovado_em:
            user.aprovado_em = timezone.now()
            changed = True

        if changed or created:
            user.save()

        status = "ADMIN_CREATED" if created else "ADMIN_OK"
        self.stdout.write(self.style.SUCCESS(status))
