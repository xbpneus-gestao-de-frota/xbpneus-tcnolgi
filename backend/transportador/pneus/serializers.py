from rest_framework import serializers
from .models import Tire, Application, MovimentacaoPneu, MedicaoPneu
from decimal import Decimal
import re

class TireSerializer(serializers.ModelSerializer):
    """Serializer para pneus com validações de negócio"""
    
    vida_util_percentual = serializers.SerializerMethodField()
    precisa_inspecao = serializers.SerializerMethodField()
    
    class Meta:
        model = Tire
        fields = "__all__"
        read_only_fields = ['criado_em', 'atualizado_em']
    
    def get_vida_util_percentual(self, obj):
        """Retorna percentual de vida útil"""
        return obj.vida_util_percentual()
    
    def get_precisa_inspecao(self, obj):
        """Retorna se pneu precisa de inspeção"""
        return obj.precisa_inspecao()
    
    def validate_codigo(self, value):
        """Valida código do pneu"""
        if not value:
            raise serializers.ValidationError("Código é obrigatório")
        
        codigo = value.strip().upper()
        
        if len(codigo) < 3:
            raise serializers.ValidationError("Código muito curto (mínimo 3 caracteres)")
        
        if len(codigo) > 100:
            raise serializers.ValidationError("Código muito longo (máximo 100 caracteres)")
        
        return codigo
    
    def validate_medida(self, value):
        """Valida formato da medida do pneu"""
        if not value:
            raise serializers.ValidationError("Medida é obrigatória")
        
        # Formato esperado: 295/80R22.5
        if not re.match(r'^\d+/\d+R\d+\.?\d*$', value):
            raise serializers.ValidationError(
                "Formato de medida inválido. Use formato como 295/80R22.5"
            )
        
        return value
    
    def validate_profundidade_sulco(self, value):
        """Valida profundidade do sulco"""
        if value is not None:
            if value < 0:
                raise serializers.ValidationError("Profundidade do sulco não pode ser negativa")
            
            if value > 30:
                raise serializers.ValidationError("Profundidade do sulco muito alta (máximo 30mm)")
            
            if value < Decimal('1.6'):
                raise serializers.ValidationError(
                    "Profundidade do sulco abaixo do limite legal (1.6mm)"
                )
        
        return value
    
    def validate_numero_recapagens(self, value):
        """Valida número de recapagens"""
        if value < 0:
            raise serializers.ValidationError("Número de recapagens não pode ser negativo")
        
        if value > 5:
            raise serializers.ValidationError("Número de recapagens muito alto (máximo: 5)")
        
        return value
    
    def validate(self, data):
        """Validações cruzadas"""
        km_atual = data.get('km_atual', 0)
        km_total = data.get('km_total', 0)
        
        if km_atual > km_total:
            raise serializers.ValidationError({
                'km_atual': 'KM atual não pode ser maior que KM total'
            })
        
        status = data.get('status')
        posicao_atual = data.get('posicao_atual', '')
        
        if status == 'MONTADO' and not posicao_atual:
            raise serializers.ValidationError({
                'posicao_atual': 'Pneu montado deve ter posição atual informada'
            })
        
        return data


class ApplicationSerializer(serializers.ModelSerializer):
    """Serializer para aplicações de pneus"""
    
    pneu_codigo = serializers.CharField(source='pneu.codigo', read_only=True)
    veiculo_placa = serializers.CharField(source='veiculo.placa', read_only=True)
    
    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ['criado_em']
    
    def validate_km_montagem(self, value):
        """Valida KM de montagem"""
        if value < 0:
            raise serializers.ValidationError("KM de montagem não pode ser negativo")
        return value
    
    def validate(self, data):
        """Validações cruzadas"""
        km_montagem = data.get('km_montagem', 0)
        km_desmontagem = data.get('km_desmontagem')
        
        if km_desmontagem and km_desmontagem <= km_montagem:
            raise serializers.ValidationError({
                'km_desmontagem': 'KM de desmontagem deve ser maior que KM de montagem'
            })
        
        return data


class MovimentacaoPneuSerializer(serializers.ModelSerializer):
    """Serializer para movimentações de pneus"""
    
    pneu_codigo = serializers.CharField(source='pneu.codigo', read_only=True)
    
    class Meta:
        model = MovimentacaoPneu
        fields = "__all__"
        read_only_fields = ['data_movimentacao']


class MedicaoPneuSerializer(serializers.ModelSerializer):
    """Serializer para medições de pneus"""
    
    pneu_codigo = serializers.CharField(source='pneu.codigo', read_only=True)
    
    class Meta:
        model = MedicaoPneu
        fields = "__all__"
        read_only_fields = ['data_medicao']
    
    def validate_sulco(self, value):
        """Valida profundidade do sulco"""
        if value < 0:
            raise serializers.ValidationError("Profundidade do sulco não pode ser negativa")
        
        if value > 30:
            raise serializers.ValidationError("Profundidade do sulco muito alta (máximo 30mm)")
        
        if value < Decimal('1.6'):
            raise serializers.ValidationError(
                "Profundidade do sulco abaixo do limite legal (1.6mm)"
            )
        
        return value
