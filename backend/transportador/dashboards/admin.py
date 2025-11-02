from django.contrib import admin
from .models import Dashboard, Widget, KPI

@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ['nome', 'padrao', 'ativo']
    list_filter = ['padrao', 'ativo']
    search_fields = ['nome']

@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'dashboard', 'tipo', 'ativo']
    list_filter = ['tipo', 'ativo']
    search_fields = ['titulo']

@admin.register(KPI)
class KPIAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'valor_atual', 'meta', 'unidade', 'data_referencia']
    list_filter = ['categoria', 'data_referencia']
    search_fields = ['nome']
