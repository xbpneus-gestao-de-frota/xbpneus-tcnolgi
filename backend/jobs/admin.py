from django.contrib import admin
from .models import AsyncJob
@admin.register(AsyncJob)
class AsyncJobAdmin(admin.ModelAdmin):
    list_display = ("id","kind","resource","fmt","status","created_at","user")
    search_fields = ("resource","status","user__username")
    list_filter = ("kind","status","fmt")
