from django.contrib import admin
from .models import Vehicle, Position
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Vehicle._meta.fields]

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Position._meta.fields]

