from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from backend.transportador.motorista_externo.models import MotoristaExterno, AlocacaoMotorista
from backend.transportador.motorista_externo.serializers import MotoristaExternoSerializer, AlocacaoMotoristaSerializer
from backend.transportador.frota.models import Vehicle
from backend.transportador.frota.serializers import VehicleSerializer
from rest_framework.decorators import action

class MotoristaExternoProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MotoristaExterno.objects.all()
    serializer_class = MotoristaExternoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Garante que o motorista externo só possa ver seu próprio perfil
        if self.request.user.is_authenticated and hasattr(self.request.user, 'motorista_externo_perfil'):
            return MotoristaExterno.objects.filter(usuario=self.request.user)
        return MotoristaExterno.objects.none()

class MotoristaExternoAlocacaoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AlocacaoMotorista.objects.all()
    serializer_class = AlocacaoMotoristaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Garante que o motorista externo só possa ver suas próprias alocações
        if self.request.user.is_authenticated and hasattr(self.request.user, 'motorista_externo_perfil'):
            motorista_externo = self.request.user.motorista_externo_perfil
            return AlocacaoMotorista.objects.filter(motorista_externo=motorista_externo)
        return AlocacaoMotorista.objects.none()

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def motorista_externo_me(request):
    if hasattr(request.user, 'motorista_externo_perfil'):
        serializer = MotoristaExternoSerializer(request.user.motorista_externo_perfil)
        return Response(serializer.data)
    return Response({"detail": "Não é um perfil de motorista externo."},
                    status=status.HTTP_403_FORBIDDEN)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def motorista_externo_dashboard(request):
    if not hasattr(request.user, 'motorista_externo_perfil'):
        return Response({"detail": "Não é um perfil de motorista externo."},
                        status=status.HTTP_403_FORBIDDEN)

    motorista_externo = request.user.motorista_externo_perfil

    # Perfil do Motorista
    profile_data = MotoristaExternoSerializer(motorista_externo).data

    # Alocações (Viagens)
    alocacoes_ativas = AlocacaoMotorista.objects.filter(
        motorista_externo=motorista_externo, status='ATIVA'
    ).select_related('veiculo')
    alocacoes_pendentes = AlocacaoMotorista.objects.filter(
        motorista_externo=motorista_externo, status='PENDENTE'
    ).select_related('veiculo')
    alocacoes_concluidas = AlocacaoMotorista.objects.filter(
        motorista_externo=motorista_externo, status='CONCLUIDA'
    ).select_related('veiculo')

    active_allocations_data = AlocacaoMotoristaSerializer(alocacoes_ativas, many=True).data
    pending_allocations_data = AlocacaoMotoristaSerializer(alocacoes_pendentes, many=True).data
    completed_allocations_data = AlocacaoMotoristaSerializer(alocacoes_concluidas, many=True).data

    # Informações do Veículo Atualmente Alocado (se houver)
    current_vehicle_data = None
    if alocacoes_ativas.exists():
        current_allocation = alocacoes_ativas.first()
        if current_allocation.veiculo:
            current_vehicle_data = VehicleSerializer(current_allocation.veiculo).data

    return Response({
        'profile': profile_data,
        'active_allocations': active_allocations_data,
        'pending_allocations': pending_allocations_data,
        'completed_allocations': completed_allocations_data,
        'current_vehicle': current_vehicle_data,
        'notifications': [] # Placeholder para notificações futuras
    }, status=status.HTTP_200_OK)


class MotoristaExternoActionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def accept_allocation(self, request, pk=None):
        try:
            allocation = AlocacaoMotorista.objects.get(pk=pk, motorista_externo__usuario=request.user)
        except AlocacaoMotorista.DoesNotExist:
            return Response({'detail': 'Alocação não encontrada ou acesso negado.'}, status=status.HTTP_404_NOT_FOUND)

        if allocation.status == 'PENDENTE':
            allocation.status = 'ATIVA'
            allocation.save()
            return Response({'detail': 'Alocação aceita com sucesso.', 'allocation': AlocacaoMotoristaSerializer(allocation).data}, status=status.HTTP_200_OK)
        return Response({'detail': 'Alocação não está no status PENDENTE.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def reject_allocation(self, request, pk=None):
        try:
            allocation = AlocacaoMotorista.objects.get(pk=pk, motorista_externo__usuario=request.user)
        except AlocacaoMotorista.DoesNotExist:
            return Response({'detail': 'Alocação não encontrada ou acesso negado.'}, status=status.HTTP_404_NOT_FOUND)

        if allocation.status == 'PENDENTE':
            allocation.status = 'CANCELADA'
            allocation.save()
            return Response({'detail': 'Alocação rejeitada com sucesso.', 'allocation': AlocacaoMotoristaSerializer(allocation).data}, status=status.HTTP_200_OK)
        return Response({'detail': 'Alocação não está no status PENDENTE.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def start_trip(self, request, pk=None):
        try:
            allocation = AlocacaoMotorista.objects.get(pk=pk, motorista_externo__usuario=request.user)
        except AlocacaoMotorista.DoesNotExist:
            return Response({'detail': 'Alocação não encontrada ou acesso negado.'}, status=status.HTTP_404_NOT_FOUND)

        if allocation.status == 'ATIVA':
            # Lógica para iniciar a viagem (ex: registrar km inicial, etc.)
            # Por enquanto, apenas atualiza o status se necessário ou registra um evento
            return Response({'detail': 'Viagem iniciada com sucesso.', 'allocation': AlocacaoMotoristaSerializer(allocation).data}, status=status.HTTP_200_OK)
        return Response({'detail': 'Alocação não está ativa.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def end_trip(self, request, pk=None):
        try:
            allocation = AlocacaoMotorista.objects.get(pk=pk, motorista_externo__usuario=request.user)
        except AlocacaoMotorista.DoesNotExist:
            return Response({'detail': 'Alocação não encontrada ou acesso negado.'}, status=status.HTTP_404_NOT_FOUND)

        if allocation.status == 'ATIVA':
            allocation.status = 'CONCLUIDA'
            allocation.save()
            # Lógica para finalizar a viagem (ex: registrar km final, etc.)
            return Response({'detail': 'Viagem finalizada com sucesso.', 'allocation': AlocacaoMotoristaSerializer(allocation).data}, status=status.HTTP_200_OK)
        return Response({'detail': 'Alocação não está ativa.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def update_status(self, request):
        # Endpoint para o motorista atualizar seu status geral (disponível, em descanso, etc.)
        # Isso pode ser um campo no modelo MotoristaExterno ou um modelo separado de StatusMotorista
        # Por simplicidade, vamos assumir que atualiza o status no perfil do motorista externo
        if not hasattr(request.user, 'motorista_externo_perfil'):
            return Response({"detail": "Não é um perfil de motorista externo."},
                            status=status.HTTP_403_FORBIDDEN)
        
        motorista_externo = request.user.motorista_externo_perfil
        new_status = request.data.get('status')
        if new_status and new_status in [choice[0] for choice in MotoristaExterno.STATUS_CHOICES]:
            motorista_externo.status = new_status
            motorista_externo.save()
            return Response({'detail': f'Status atualizado para {new_status}.', 'profile': MotoristaExternoSerializer(motorista_externo).data}, status=status.HTTP_200_OK)
        return Response({'detail': 'Status inválido ou não fornecido.'}, status=status.HTTP_400_BAD_REQUEST)

