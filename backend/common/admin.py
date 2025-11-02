from django.contrib import admin
from django.http import HttpResponse
from .models import AuditLog
import csv

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("ts","user","action","model","object_id")
    search_fields = ("user__username","model","object_id","action","details")
    list_filter = ("action","model")
    actions = ["export_csv"]

    def export_csv(self, request, queryset):
        resp = HttpResponse(content_type="text/csv; charset=utf-8")
        resp["Content-Disposition"] = 'attachment; filename="audit_log.csv"'
        w = csv.writer(resp)
        w.writerow(["ts","user","action","model","object_id","details"])
        for a in queryset:
            w.writerow([a.ts, getattr(a.user,"username",None), a.action, a.model, a.object_id, a.details])
        return resp
    export_csv.short_description = "Exportar selecionados em CSV"
