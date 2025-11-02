from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import AnaliseIA, Gamificacao, Garantia
from .serializers import AnaliseIASerializer, GamificacaoSerializer, GarantiaSerializer
from .permissions import IsTransportadorOrAdmin


class AnaliseIAViewSet(viewsets.ModelViewSet):
    """
    ViewSet para análises de IA
    Acesso: Usuários Transportador e Admins
    """
    queryset = AnaliseIA.objects.all()
    serializer_class = AnaliseIASerializer
    permission_classes = [IsAuthenticated, IsTransportadorOrAdmin]
    
    def get_queryset(self):
        """Retorna apenas análises do usuário logado (ou todas se admin)"""
        if self.request.user.is_staff:
            return AnaliseIA.objects.all()
        return AnaliseIA.objects.filter(usuario=self.request.user)
    
    @action(detail=False, methods=['post'])
    def analisar(self, request):
        """
        Endpoint para realizar análise de imagem/vídeo/áudio
        """
        # TODO: Implementar lógica de análise com os módulos de IA
        return Response({
            'message': 'Análise iniciada com sucesso',
            'status': 'processando'
        }, status=status.HTTP_202_ACCEPTED)
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """
        Retorna métricas e estatísticas do dashboard
        """
        # TODO: Implementar lógica do dashboard
        return Response({
            'total_analises': AnaliseIA.objects.filter(usuario=request.user).count(),
            'precisao_media': 0.0,
            'tempo_medio': 0.0
        })


class GamificacaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gamificação
    Acesso: Usuários Transportador e Admins
    """
    queryset = Gamificacao.objects.all()
    serializer_class = GamificacaoSerializer
    permission_classes = [IsAuthenticated, IsTransportadorOrAdmin]
    
    @action(detail=False, methods=['get'])
    def ranking(self, request):
        """
        Retorna o ranking de usuários
        """
        ranking = Gamificacao.objects.all()[:10]
        serializer = self.get_serializer(ranking, many=True)
        return self.response(serializer.data)


class GarantiaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para garantias
    Acesso: Usuários Transportador e Admins
    """
    queryset = Garantia.objects.all()
    serializer_class = GarantiaSerializer
    permission_classes = [IsAuthenticated, IsTransportadorOrAdmin]
    
    def get_queryset(self):
        """Retorna apenas garantias do usuário logado (ou todas se admin)"""
        if self.request.user.is_staff:
            return Garantia.objects.all()
        return Garantia.objects.filter(usuario=self.request.user)
    
    @action(detail=True, methods=['post'])
    def aprovar(self, request, pk=None):
        """
        Aprova uma garantia (apenas admins)
        """
        if not request.user.is_staff:
            return Response(
                {'error': 'Apenas administradores podem aprovar garantias'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        garantia = self.get_object()
        garantia.status = 'aprovada'
        garantia.save()
        
        return Response({
            'message': 'Garantia aprovada com sucesso',
            'protocolo': garantia.protocolo
        })

