import time
from typing import Any, Dict, Tuple

from django.db import transaction
from django.db.models import Avg, Count, Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .core.analise_imagem_garantia import AnalisadorImagemGarantia
from .models import AnaliseIA, Gamificacao, Garantia
from .permissions import IsTransportadorOrAdmin
from .serializers import (
    AnaliseIASerializer,
    GamificacaoSerializer,
    GarantiaSerializer,
)


class AnaliseIAViewSet(viewsets.ModelViewSet):
    """
    ViewSet para análises de IA
    Acesso: Usuários Transportador e Admins
    """
    queryset = AnaliseIA.objects.all()
    serializer_class = AnaliseIASerializer
    permission_classes = [IsAuthenticated, IsTransportadorOrAdmin]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        """Retorna apenas análises do usuário logado (ou todas se admin)"""
        if self.request.user.is_staff:
            return AnaliseIA.objects.all()
        return AnaliseIA.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
    
    @action(detail=False, methods=['post'])
    def analisar(self, request):
        """
        Endpoint para realizar análise de imagem/vídeo/áudio
        """
        upload = request.FILES.get('arquivo')
        if upload is None:
            raise ValidationError({'arquivo': 'Um arquivo é obrigatório para realizar a análise.'})

        tipo = request.data.get('tipo_analise', AnaliseIA._meta.get_field('tipo_analise').choices[0][0])
        tipos_validos = {choice for choice, _ in AnaliseIA._meta.get_field('tipo_analise').choices}
        if tipo not in tipos_validos:
            raise ValidationError({'tipo_analise': 'Tipo de análise inválido.'})

        with transaction.atomic():
            analise = AnaliseIA.objects.create(
                usuario=request.user,
                tipo_analise=tipo,
                arquivo=upload,
                resultado={},
                status='processando',
            )

        inicio = time.perf_counter()
        try:
            resultado, precisao = self._executar_analise(analise, request.data)
            tempo_processamento = time.perf_counter() - inicio
            analise.resultado = resultado
            analise.precisao = precisao
            analise.tempo_processamento = tempo_processamento
            analise.status = 'concluida'
            analise.save(update_fields=['resultado', 'precisao', 'tempo_processamento', 'status'])
        except Exception as exc:  # pragma: no cover - proteção operacional
            analise.status = 'erro'
            analise.resultado = {'erro': str(exc)}
            analise.save(update_fields=['status', 'resultado'])
            raise ValidationError({'detail': f'Falha ao processar análise: {exc}'})

        serializer = self.get_serializer(analise)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """
        Retorna métricas e estatísticas do dashboard
        """
        analises = self.get_queryset()
        agregados = analises.aggregate(
            precisao_media=Avg('precisao'),
            tempo_medio=Avg('tempo_processamento'),
            processando=Count('id', filter=Q(status='processando')),
            concluidas=Count('id', filter=Q(status='concluida')),
            erros=Count('id', filter=Q(status='erro')),
        )

        return Response({
            'total_analises': analises.count(),
            'precisao_media': round(agregados['precisao_media'] or 0.0, 3),
            'tempo_medio': round(agregados['tempo_medio'] or 0.0, 3),
            'fila': {
                'processando': agregados['processando'],
                'concluidas': agregados['concluidas'],
                'erros': agregados['erros'],
            },
        })

    def _executar_analise(self, analise: AnaliseIA, payload) -> Tuple[Dict[str, Any], float]:
        if analise.tipo_analise == 'imagem':
            analisador = AnalisadorImagemGarantia()
            contexto = {
                'descricao_usuario': payload.get('descricao_usuario') or payload.get('descricao', ''),
            }
            resultado = analisador.analisar_imagens_whatsapp([analise.arquivo.path], contexto)
            confiancas = [item.get('confianca', 0) for item in resultado.get('analises_individuais', [])]
            precisao = sum(confiancas) / len(confiancas) if confiancas else 0.0
            return resultado, precisao

        return (
            {
                'mensagem': 'Tipo de análise ainda não suportado',
                'tipo': analise.tipo_analise,
            },
            0.0,
        )


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
        return Response(serializer.data)


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

