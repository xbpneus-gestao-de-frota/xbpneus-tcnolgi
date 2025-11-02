from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = "Carrega seeds de apps do Transportador"
    def handle(self, *args, **kwargs):
        # apps: frota, pneus, estoque, manutencao
        self.stdout.write(self.style.NOTICE("Carregando seeds..."))
        call_command("loaddata", "initial_data.json", app_label="frota")
        call_command("loaddata", "initial_data.json", app_label="pneus")
        call_command("loaddata", "initial_data.json", app_label="estoque")
        call_command("loaddata", "initial_data.json", app_label="manutencao")
        self.stdout.write(self.style.SUCCESS("Seeds carregados."))
