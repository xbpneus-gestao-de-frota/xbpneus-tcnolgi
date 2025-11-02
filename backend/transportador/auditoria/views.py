"""
Views para o módulo de Auditoria
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from .models import (
    LogAuditoria,
    LogAcesso,
    LogAlteracao,
    SessaoUsuario,
    ConfiguracaoAuditoria
)
from .serializers import (
    LogAuditoriaSerializer,
    LogAcessoSerializer,
    LogAlteracaoSerializer,
    SessaoUsuarioSerializer,
    ConfiguracaoAuditoriaSerializer
)


class LogAuditoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para Logs de Auditoria (somente leitura)"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = LogAuditoriaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['usuario', 'empresa', 'acao', 'severidade', 'modulo']
    search_fields = ['descricao', 'usuario__username', 'ip_address']
    ordering_fields = ['criado_em', 'severidade']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        """Retorna queryset filtrado por empresa do usuário"""
        user = self.request.user
        if user.is_superuser:
            return LogAuditoria.objects.all()
        return LogAuditoria.objects.filter(empresa=user.empresa)
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Retorna estatísticas de logs de auditoria"""
        queryset = self.get_queryset()
        
        # Filtrar por período
        periodo = request.query_params.get('periodo', '30')  # dias
        data_inicio = timezone.now() - timedelta(days=int(periodo))
        queryset = queryset.filter(criado_em__gte=data_inicio)
        
        # Estatísticas gerais
        stats = {
            'total_logs': queryset.count(),
            'por_acao': {},
            'por_severidade': {},
            'por_usuario': {},
            'por_modulo': {}
        }
        
        # Por ação
        for acao in queryset.values('acao').annotate(total=Count('id')):
            stats['por_acao'][acao['acao']] = acao['total']
        
        # Por severidade
        for sev in queryset.values('severidade').annotate(total=Count('id')):
            stats['por_severidade'][sev['severidade']] = sev['total']
        
        # Top 10 usuários
        top_usuarios = queryset.values(
            'usuario__username', 'usuario__first_name', 'usuario__last_name'
        ).annotate(total=Count('id')).order_by('-total')[:10]
        
        stats['por_usuario'] = [
            {
                'usuario': f"{u['usuario__first_name']} {u['usuario__last_name']}".strip() or u['usuario__username'],
                'total': u['total']
            }
            for u in top_usuarios
        ]
        
        # Por módulo
        for mod in queryset.values('modulo').annotate(total=Count('id')).order_by('-total')[:10]:
            if mod['modulo']:
                stats['por_modulo'][mod['modulo']] = mod['total']
        
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def timeline(self, request):
        """Retorna timeline de eventos"""
        queryset = self.get_queryset()
        
        # Filtrar por período
        periodo = request.query_params.get('periodo', '7')  # dias
        data_inicio = timezone.now() - timedelta(days=int(periodo))
        queryset = queryset.filter(criado_em__gte=data_inicio)
        
        # Agrupar por dia
        timeline = []
        for dia in range(int(periodo)):
            data = timezone.now() - timedelta(days=dia)
            logs_dia = queryset.filter(
                criado_em__year=data.year,
                criado_em__month=data.month,
                criado_em__day=data.day
            )
            
            timeline.append({
                'data': data.strftime('%Y-%m-%d'),
                'total': logs_dia.count(),
                'por_severidade': {
                    'INFO': logs_dia.filter(severidade='INFO').count(),
                    'WARNING': logs_dia.filter(severidade='WARNING').count(),
                    'ERROR': logs_dia.filter(severidade='ERROR').count(),
                    'CRITICAL': logs_dia.filter(severidade='CRITICAL').count(),
                }
            })
        
        return Response(timeline)
    
    @action(detail=False, methods=['get'])
    def alteracoes_objeto(self, request):
        """Retorna histórico de alterações de um objeto específico"""
        content_type_id = request.query_params.get('content_type')
        object_id = request.query_params.get('object_id')
        
        if not content_type_id or not object_id:
            return Response(
                {'erro': 'content_type e object_id são obrigatórios'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        logs = self.get_queryset().filter(
            content_type_id=content_type_id,
            object_id=object_id
        ).order_by('-criado_em')
        
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)


class LogAcessoViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para Logs de Acesso (somente leitura)"""
    
    permission_classes = [IsAdminUser]
    serializer_class = LogAcessoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['usuario', 'tipo_acesso', 'sucesso']
    search_fields = ['usuario__username', 'ip_address']
    ordering_fields = ['criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        """Retorna todos os logs de acesso"""
        return LogAcesso.objects.all()
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Retorna estatísticas de acessos"""
        queryset = self.get_queryset()
        
        # Filtrar por período
        periodo = request.query_params.get('periodo', '30')  # dias
        data_inicio = timezone.now() - timedelta(days=int(periodo))
        queryset = queryset.filter(criado_em__gte=data_inicio)
        
        stats = {
            'total_acessos': queryset.count(),
            'logins_sucesso': queryset.filter(tipo_acesso='LOGIN', sucesso=True).count(),
            'logins_falhos': queryset.filter(tipo_acesso='LOGIN_FALHO').count(),
            'logouts': queryset.filter(tipo_acesso='LOGOUT').count(),
            'sessoes_expiradas': queryset.filter(tipo_acesso='SESSAO_EXPIRADA').count(),
            'usuarios_unicos': queryset.values('usuario').distinct().count(),
            'ips_unicos': queryset.values('ip_address').distinct().count(),
        }
        
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def acessos_suspeitos(self, request):
        """Identifica acessos suspeitos"""
        queryset = self.get_queryset()
        
        # Últimas 24 horas
        data_inicio = timezone.now() - timedelta(hours=24)
        queryset = queryset.filter(criado_em__gte=data_inicio)
        
        suspeitos = []
        
        # Múltiplos logins falhos
        usuarios_falhas = queryset.filter(
            tipo_acesso='LOGIN_FALHO'
        ).values('usuario', 'ip_address').annotate(
            total=Count('id')
        ).filter(total__gte=3)
        
        for u in usuarios_falhas:
            suspeitos.append({
                'tipo': 'Múltiplos logins falhos',
                'usuario_id': u['usuario'],
                'ip_address': u['ip_address'],
                'quantidade': u['total']
            })
        
        # Acessos de IPs diferentes
        usuarios_multi_ip = queryset.filter(
            tipo_acesso='LOGIN',
            sucesso=True
        ).values('usuario').annotate(
            ips_diferentes=Count('ip_address', distinct=True)
        ).filter(ips_diferentes__gte=3)
        
        for u in usuarios_multi_ip:
            suspeitos.append({
                'tipo': 'Múltiplos IPs',
                'usuario_id': u['usuario'],
                'quantidade': u['ips_diferentes']
            })
        
        return Response(suspeitos)


class LogAlteracaoViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para Logs de Alteração (somente leitura)"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = LogAlteracaoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['usuario', 'empresa', 'tipo_alteracao', 'content_type']
    search_fields = ['object_repr', 'campo', 'valor_anterior', 'valor_novo']
    ordering_fields = ['criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        """Retorna queryset filtrado por empresa do usuário"""
        user = self.request.user
        if user.is_superuser:
            return LogAlteracao.objects.all()
        return LogAlteracao.objects.filter(empresa=user.empresa)
    
    @action(detail=False, methods=['get'])
    def historico_objeto(self, request):
        """Retorna histórico completo de alterações de um objeto"""
        content_type_id = request.query_params.get('content_type')
        object_id = request.query_params.get('object_id')
        
        if not content_type_id or not object_id:
            return Response(
                {'erro': 'content_type e object_id são obrigatórios'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        logs = self.get_queryset().filter(
            content_type_id=content_type_id,
            object_id=object_id
        ).order_by('-criado_em')
        
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)


class SessaoUsuarioViewSet(viewsets.ModelViewSet):
    """ViewSet para Sessões de Usuário"""
    
    permission_classes = [IsAdminUser]
    serializer_class = SessaoUsuarioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['usuario', 'ativa']
    search_fields = ['usuario__username', 'ip_address']
    ordering_fields = ['iniciada_em', 'ultima_atividade']
    ordering = ['-iniciada_em']
    
    def get_queryset(self):
        """Retorna todas as sessões"""
        return SessaoUsuario.objects.all()
    
    @action(detail=False, methods=['get'])
    def ativas(self, request):
        """Retorna apenas sessões ativas"""
        sessoes = self.get_queryset().filter(ativa=True)
        serializer = self.get_serializer(sessoes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def encerrar(self, request, pk=None):
        """Encerra uma sessão"""
        sessao = self.get_object()
        
        if not sessao.ativa:
            return Response(
                {'erro': 'Sessão já está encerrada'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        sessao.ativa = False
        sessao.encerrada_em = timezone.now()
        sessao.motivo_encerramento = 'ADMIN'
        sessao.save()
        
        serializer = self.get_serializer(sessao)
        return Response(serializer.data)


class ConfiguracaoAuditoriaViewSet(viewsets.ModelViewSet):
    """ViewSet para Configuração de Auditoria"""
    
    permission_classes = [IsAdminUser]
    serializer_class = ConfiguracaoAuditoriaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = []
    
    def get_queryset(self):
        """Retorna todas as configurações"""
        return ConfiguracaoAuditoria.objects.all()
