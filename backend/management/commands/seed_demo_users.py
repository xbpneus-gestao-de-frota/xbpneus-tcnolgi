from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Cria usuários demo (admin/ops/transportador) e associa grupos."
    def handle(self, *args, **kwargs):
        User = get_user_model()
        # Ensure groups exist
        for g in ["admin","ops","transportador"]:
            Group.objects.get_or_create(name=g)
        users = [
            ("admin_demo", "xbp12345", ["admin"], True, True),
            ("ops_demo", "xbp12345", ["ops"], False, False),
            ("transp_demo", "xbp12345", ["transportador"], False, False),
        ]
        for username, password, groups, is_staff, is_superuser in users:
            u, created = User.objects.get_or_create(username=username, defaults={"is_staff": is_staff, "is_superuser": is_superuser})
            if created:
                u.set_password(password); u.save()
                self.stdout.write(self.style.SUCCESS(f"Usuário criado: {username} / {password}"))
            else:
                self.stdout.write(f"Usuário já existe: {username}")
            for g in groups:
                grp = Group.objects.get(name=g)
                u.groups.add(grp)
        self.stdout.write(self.style.SUCCESS("Usuários demo prontos."))
