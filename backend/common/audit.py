import json
from django.conf import settings
from rest_framework import viewsets
from .models import AuditLog

def _mask_payload(obj):
    try:
        mask = getattr(settings, "AUDIT_MASK_FIELDS", set())
        if isinstance(obj, dict):
            return {k: ("***" if k.lower() in mask else _mask_payload(v)) for k,v in obj.items()}
        if isinstance(obj, list):
            return [_mask_payload(x) for x in obj]
        return obj
    except Exception:
        return obj

def _safe_json(data):
    try:
        return json.dumps(data, ensure_ascii=False)
    except Exception:
        return ""

class AuditedModelViewSet(viewsets.ModelViewSet):
    def log(self, instance, action):
        AuditLog.objects.create(
            user=getattr(self.request, "user", None) if hasattr(self, "request") else None,
            action=action,
            model=instance.__class__.__name__,
            object_id=str(getattr(instance, "pk", "")),
            details=_safe_json(_mask_payload(getattr(self.request, "data", {}))),
        )

    def perform_create(self, serializer):
        instance = serializer.save()
        self.log(instance, "create")

    def perform_update(self, serializer):
        instance = serializer.save()
        self.log(instance, "update")

    def perform_destroy(self, instance):
        self.log(instance, "delete")
        instance.delete()
