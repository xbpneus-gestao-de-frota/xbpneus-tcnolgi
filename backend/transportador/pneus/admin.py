from django.contrib import admin
from .models import Tire, Application
@admin.register(Tire)
class TireAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Tire._meta.fields]

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Application._meta.fields]

