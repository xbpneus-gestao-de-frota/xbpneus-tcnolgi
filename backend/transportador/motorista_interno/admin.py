from django.contrib import admin
from .models import (
    MotoristaInterno, VinculoMotoristaVeiculo, RegistroJornada,
    MensagemMotorista, AlertaMotorista
)


@admin.register(MotoristaInterno)
class MotoristaInternoAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'cpf', 'cnh', 'status', 'tipo_contrato', 'conectado_app']
    list_filter = ['status', 'tipo_contrato', 'conectado_app']
    search_fields = ['nome_completo', 'cpf', 'cnh']
    readonly_fields = ['criado_em', 'atualizado_em', 'ultimo_acesso_app']


@admin.register(VinculoMotoristaVeiculo)
class VinculoMotoristaVeiculoAdmin(admin.ModelAdmin):
    list_display = ['motorista', 'veiculo', 'data_inicio', 'data_fim', 'status']
    list_filter = ['status', 'data_inicio']
    search_fields = ['motorista__nome_completo', 'veiculo__placa']


@admin.register(RegistroJornada)
class RegistroJornadaAdmin(admin.ModelAdmin):
    list_display = ['motorista', 'veiculo', 'tipo_registro', 'data_hora', 'origem']
    list_filter = ['tipo_registro', 'origem', 'data_hora']
    search_fields = ['motorista__nome_completo', 'veiculo__placa']
    readonly_fields = ['criado_em']


@admin.register(MensagemMotorista)
class MensagemMotoristaAdmin(admin.ModelAdmin):
    list_display = ['motorista', 'tipo', 'assunto', 'status', 'data_envio']
    list_filter = ['tipo', 'status', 'data_envio']
    search_fields = ['motorista__nome_completo', 'assunto', 'mensagem']
    readonly_fields = ['criado_em', 'data_entrega', 'data_leitura']


@admin.register(AlertaMotorista)
class AlertaMotoristaAdmin(admin.ModelAdmin):
    list_display = ['motorista', 'tipo', 'prioridade', 'status', 'data_alerta']
    list_filter = ['tipo', 'prioridade', 'status', 'data_alerta']
    search_fields = ['motorista__nome_completo', 'titulo', 'descricao']
    readonly_fields = ['criado_em', 'data_alerta']
