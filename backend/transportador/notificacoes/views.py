from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from backend.common.permissions import OptionalRolePermission
from backend.common.audit import AuditedModelViewSet
from .models import CanalNotificacao, Notificacao, TemplateNotificacao, PreferenciaNotificacao
from .serializers import CanalNotificacaoSerializer, NotificacaoSerializer, TemplateNotificacaoSerializer, PreferenciaNotificacaoSerializer

class CanalNotificacaoViewSet(AuditedModelViewSet):
    queryset = CanalNotificacao.objects.all().order_by('tipo', 'nome')
    serializer_class = CanalNotificacaoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome']
    ordering_fields = ['tipo', 'nome']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['tipo', 'ativo']

class NotificacaoViewSet(AuditedModelViewSet):
    queryset = Notificacao.objects.all().order_by('-criado_em')
    serializer_class = NotificacaoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['titulo', 'mensagem']
    ordering_fields = ['criado_em', 'prioridade']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['canal', 'status', 'prioridade', 'categoria']
    
    @action(detail=False, methods=['get'])
    def nao_lidas(self, request):
        notificacoes = self.get_queryset().filter(destinatario_usuario=request.user).exclude(status='LIDA')
        return Response(self.get_serializer(notificacoes, many=True).data)
    
    @action(detail=True, methods=['post'])
    def marcar_lida(self, request, pk=None):
        notificacao = self.get_object()
        notificacao.marcar_como_lida()
        return Response(self.get_serializer(notificacao).data)
    
    @action(detail=True, methods=['post'])
    def reenviar(self, request, pk=None):
        notificacao = self.get_object()
        if notificacao.pode_reenviar():
            notificacao.status = 'PENDENTE'
            notificacao.tentativas += 1
            notificacao.save()
            return Response({'message': 'Notificação reenviada'})
        return Response({'error': 'Não é possível reenviar esta notificação'}, status=400)

class TemplateNotificacaoViewSet(AuditedModelViewSet):
    queryset = TemplateNotificacao.objects.all().order_by('categoria', 'nome')
    serializer_class = TemplateNotificacaoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'categoria']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['categoria', 'ativo']

class PreferenciaNotificacaoViewSet(AuditedModelViewSet):
    queryset = PreferenciaNotificacao.objects.all()
    serializer_class = PreferenciaNotificacaoSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    
    @action(detail=False, methods=['get'])
    def minhas_preferencias(self, request):
        preferencia, created = PreferenciaNotificacao.objects.get_or_create(
            usuario=request.user,
            empresa=request.user.empresa
        )
        return Response(self.get_serializer(preferencia).data)
