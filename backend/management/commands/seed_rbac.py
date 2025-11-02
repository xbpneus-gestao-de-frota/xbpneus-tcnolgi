from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from backend.transportador.frota.models import Vehicle, Position
from backend.transportador.pneus.models import Tire, Application
from backend.transportador.estoque.models import StockMove
from backend.transportador.manutencao.models import WorkOrder, Teste

MODELS = [Vehicle, Position, Tire, Application, StockMove, WorkOrder, Teste]

ROLE_MATRIX = {
    "transportador": {"view"},
    "ops": {"view","change"},
    "admin": {"view","add","change","delete"},
}

class Command(BaseCommand):
    help = "Cria grupos e vincula permissões por modelo"
    def handle(self, *args, **kwargs):
        for role, actions in ROLE_MATRIX.items():
            grp, _ = Group.objects.get_or_create(name=role)
            for model in MODELS:
                ct = ContentType.objects.get_for_model(model)
                for act in actions:
                    codename = f"{act}_{model._meta.model_name}"
                    try:
                        perm = Permission.objects.get(codename=codename, content_type=ct)
                        grp.permissions.add(perm)
                        self.stdout.write(f"Vinculado: {role} -> {codename}")
                    except Permission.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f"Permissão não encontrada: {codename}"))
        self.stdout.write(self.style.SUCCESS("RBAC configurado."))
