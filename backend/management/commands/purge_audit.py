from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from backend.common.models import AuditLog

class Command(BaseCommand):
    help = "Remove registros antigos de AuditLog (padrão: 90 dias)"
    def add_arguments(self, parser):
        parser.add_argument("--days", type=int, default=90)
    def handle(self, *args, **opts):
        cutoff = timezone.now() - timedelta(days=opts["days"])
        n, _ = AuditLog.objects.filter(ts__lt=cutoff).delete()
        self.stdout.write(self.style.SUCCESS(f"Removidos {n} registros antigos (>{opts['days']} dias)."))
