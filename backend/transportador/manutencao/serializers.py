"""
Serializers completos para o módulo de Manutenção
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework import serializers
from .models import (
    OrdemServico, ItemOS, ChecklistManutencao,
    PlanoManutencaoPreventiva, HistoricoManutencao,
    WorkOrder, Teste
)


class ItemOSSerializer(serializers.ModelSerializer):
    """Serializer para Item da OS"""
    
    class Meta:
        model = ItemOS
        fields = '__all__'
        read_only_fields = ['id', 'valor_total', 'criado_em']


class ChecklistManutencaoSerializer(serializers.ModelSerializer):
    """Serializer para Checklist de Manutenção"""
    
    realizado_por_nome = serializers.CharField(source='realizado_por.get_full_name', read_only=True)
    percentual_conclusao = serializers.ReadOnlyField()
    
    class Meta:
        model = ChecklistManutencao
        fields = '__all__'
        read_only_fields = ['id', 'realizado_em']


class OrdemServicoSerializer(serializers.ModelSerializer):
    """Serializer para Ordem de Serviço"""
    
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    veiculo_placa = serializers.CharField(source='veiculo.placa', read_only=True)
    aberta_por_nome = serializers.CharField(source='aberta_por.get_full_name', read_only=True)
    mecanico_nome = serializers.CharField(source='mecanico.get_full_name', read_only=True)
    
    itens = ItemOSSerializer(many=True, read_only=True)
    checklists = ChecklistManutencaoSerializer(many=True, read_only=True)
    
    tempo_execucao = serializers.ReadOnlyField()
    esta_atrasada = serializers.ReadOnlyField()
    
    total_itens = serializers.IntegerField(source='itens.count', read_only=True)
    
    class Meta:
        model = OrdemServico
        fields = '__all__'
        read_only_fields = ['id', 'custo_total', 'criado_em', 'atualizado_em']


class PlanoManutencaoPreventivaSerializer(serializers.ModelSerializer):
    """Serializer para Plano de Manutenção Preventiva"""
    
    empresa_nome = serializers.CharField(source='empresa.razao_social', read_only=True)
    veiculo_placa = serializers.CharField(source='veiculo.placa', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = PlanoManutencaoPreventiva
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em']


class HistoricoManutencaoSerializer(serializers.ModelSerializer):
    """Serializer para Histórico de Manutenção"""
    
    veiculo_placa = serializers.CharField(source='veiculo.placa', read_only=True)
    os_numero = serializers.CharField(source='os.numero', read_only=True)
    
    class Meta:
        model = HistoricoManutencao
        fields = '__all__'
        read_only_fields = ['id', 'criado_em']


# Serializers legados (para compatibilidade)
class WorkOrderSerializer(serializers.ModelSerializer):
    """Serializer para Work Order (legado)"""
    
    class Meta:
        model = WorkOrder
        fields = ["id","tipo","status","veiculo","agendamento"]


class TesteSerializer(serializers.ModelSerializer):
    """Serializer para Teste (legado)"""
    
    class Meta:
        model = Teste
        fields = ["id","os_id","torque_ok","pressao_ok","rodagem_ok","data"]
