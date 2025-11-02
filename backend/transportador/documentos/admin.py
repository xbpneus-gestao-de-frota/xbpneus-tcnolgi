from django.contrib import admin
from .models import Documento

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'numero', 'veiculo', 'data_validade', 'status']
    list_filter = ['tipo', 'status', 'data_validade']
    search_fields = ['numero', 'veiculo__placa']
    readonly_fields = ['criado_em', 'atualizado_em']
