from rest_framework import serializers
from .models import Dashboard, Widget, KPI

class WidgetSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = Widget
        fields = '__all__'
        read_only_fields = ['criado_em', 'atualizado_em']

class DashboardSerializer(serializers.ModelSerializer):
    widgets = WidgetSerializer(many=True, read_only=True)
    
    class Meta:
        model = Dashboard
        fields = '__all__'
        read_only_fields = ['criado_em', 'atualizado_em']

class KPISerializer(serializers.ModelSerializer):
    categoria_display = serializers.CharField(source='get_categoria_display', read_only=True)
    variacao_percentual_calc = serializers.DecimalField(source='variacao_percentual', max_digits=10, decimal_places=2, read_only=True)
    atingiu_meta_calc = serializers.BooleanField(source='atingiu_meta', read_only=True)
    
    class Meta:
        model = KPI
        fields = '__all__'
        read_only_fields = ['criado_em', 'atualizado_em']
