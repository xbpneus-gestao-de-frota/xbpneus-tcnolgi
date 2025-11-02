"""
Views para o módulo de Notas Fiscais
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count, Q
from datetime import datetime, timedelta

from .models import NotaFiscal, ItemNotaFiscal, ImpostoNotaFiscal, AnexoNotaFiscal
from .serializers import (
    NotaFiscalListSerializer,
    NotaFiscalDetailSerializer,
    NotaFiscalCreateUpdateSerializer,
    ItemNotaFiscalSerializer,
    ImpostoNotaFiscalSerializer,
    AnexoNotaFiscalSerializer
)


class NotaFiscalViewSet(viewsets.ModelViewSet):
    """ViewSet para Notas Fiscais"""
    
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo', 'status', 'modelo']
    search_fields = ['numero', 'serie', 'destinatario_nome', 'chave_acesso']
    ordering_fields = ['data_emissao', 'numero', 'valor_total']
    ordering = ['-data_emissao']
    
    def get_queryset(self):
        """Retorna queryset filtrado por empresa do usuário"""
        user = self.request.user
        if user.is_superuser:
            return NotaFiscal.objects.all()
        return NotaFiscal.objects.filter(empresa=user.empresa)
    
    def get_serializer_class(self):
        """Retorna o serializer apropriado"""
        if self.action == 'list':
            return NotaFiscalListSerializer
        elif self.action == 'retrieve':
            return NotaFiscalDetailSerializer
        return NotaFiscalCreateUpdateSerializer
    
    def perform_create(self, serializer):
        """Salva o usuário que criou a nota"""
        serializer.save(criado_por=self.request.user)
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Retorna estatísticas de notas fiscais"""
        queryset = self.get_queryset()
        
        # Filtrar por período se fornecido
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        
        if data_inicio and data_fim:
            queryset = queryset.filter(
                data_emissao__gte=data_inicio,
                data_emissao__lte=data_fim
            )
        
        # Calcular estatísticas
        stats = queryset.aggregate(
            total_notas=Count('id'),
            valor_total=Sum('valor_total'),
            total_icms=Sum('valor_icms'),
            total_ipi=Sum('valor_ipi'),
            total_pis=Sum('valor_pis'),
            total_cofins=Sum('valor_cofins')
        )
        
        # Estatísticas por tipo
        por_tipo = {}
        for tipo in ['ENTRADA', 'SAIDA', 'SERVICO', 'DEVOLUCAO']:
            tipo_stats = queryset.filter(tipo=tipo).aggregate(
                quantidade=Count('id'),
                valor_total=Sum('valor_total')
            )
            por_tipo[tipo] = tipo_stats
        
        # Estatísticas por status
        por_status = {}
        for status_nf in ['RASCUNHO', 'EMITIDA', 'AUTORIZADA', 'CANCELADA']:
            status_stats = queryset.filter(status=status_nf).aggregate(
                quantidade=Count('id'),
                valor_total=Sum('valor_total')
            )
            por_status[status_nf] = status_stats
        
        return Response({
            'geral': stats,
            'por_tipo': por_tipo,
            'por_status': por_status
        })
    
    @action(detail=True, methods=['post'])
    def autorizar(self, request, pk=None):
        """Autoriza uma nota fiscal"""
        nota = self.get_object()
        
        if nota.status != 'EMITIDA':
            return Response(
                {'erro': 'Apenas notas emitidas podem ser autorizadas'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Aqui seria a integração com SEFAZ
        # Por enquanto, apenas muda o status
        nota.status = 'AUTORIZADA'
        nota.data_autorizacao = datetime.now()
        nota.protocolo_autorizacao = f"PROTO{datetime.now().strftime('%Y%m%d%H%M%S')}"
        nota.save()
        
        serializer = NotaFiscalDetailSerializer(nota)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        """Cancela uma nota fiscal"""
        nota = self.get_object()
        motivo = request.data.get('motivo')
        
        if not motivo:
            return Response(
                {'erro': 'Motivo do cancelamento é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if nota.status != 'AUTORIZADA':
            return Response(
                {'erro': 'Apenas notas autorizadas podem ser canceladas'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Aqui seria a integração com SEFAZ
        # Por enquanto, apenas muda o status
        nota.status = 'CANCELADA'
        nota.data_cancelamento = datetime.now()
        nota.motivo_cancelamento = motivo
        nota.save()
        
        serializer = NotaFiscalDetailSerializer(nota)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def xml(self, request, pk=None):
        """Retorna o XML da nota fiscal"""
        nota = self.get_object()
        
        if not nota.xml_enviado:
            return Response(
                {'erro': 'XML não disponível'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response({
            'xml_enviado': nota.xml_enviado,
            'xml_retorno': nota.xml_retorno
        })
    
    @action(detail=False, methods=['get'])
    def relatorio_mensal(self, request):
        """Relatório mensal de notas fiscais"""
        mes = request.query_params.get('mes', datetime.now().month)
        ano = request.query_params.get('ano', datetime.now().year)
        
        queryset = self.get_queryset().filter(
            data_emissao__month=mes,
            data_emissao__year=ano
        )
        
        # Agrupar por dia
        relatorio = []
        for dia in range(1, 32):
            try:
                data = datetime(int(ano), int(mes), dia)
                notas_dia = queryset.filter(data_emissao__day=dia)
                
                if notas_dia.exists():
                    stats = notas_dia.aggregate(
                        quantidade=Count('id'),
                        valor_total=Sum('valor_total')
                    )
                    relatorio.append({
                        'data': data.strftime('%Y-%m-%d'),
                        'quantidade': stats['quantidade'],
                        'valor_total': stats['valor_total']
                    })
            except ValueError:
                break
        
        return Response(relatorio)


class ItemNotaFiscalViewSet(viewsets.ModelViewSet):
    """ViewSet para Itens de Nota Fiscal"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = ItemNotaFiscalSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['nota_fiscal']
    search_fields = ['codigo_produto', 'descricao']
    
    def get_queryset(self):
        """Retorna queryset filtrado por empresa do usuário"""
        user = self.request.user
        if user.is_superuser:
            return ItemNotaFiscal.objects.all()
        return ItemNotaFiscal.objects.filter(nota_fiscal__empresa=user.empresa)


class ImpostoNotaFiscalViewSet(viewsets.ModelViewSet):
    """ViewSet para Impostos de Nota Fiscal"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = ImpostoNotaFiscalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nota_fiscal', 'tipo_imposto']
    
    def get_queryset(self):
        """Retorna queryset filtrado por empresa do usuário"""
        user = self.request.user
        if user.is_superuser:
            return ImpostoNotaFiscal.objects.all()
        return ImpostoNotaFiscal.objects.filter(nota_fiscal__empresa=user.empresa)


class AnexoNotaFiscalViewSet(viewsets.ModelViewSet):
    """ViewSet para Anexos de Nota Fiscal"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = AnexoNotaFiscalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nota_fiscal']
    
    def get_queryset(self):
        """Retorna queryset filtrado por empresa do usuário"""
        user = self.request.user
        if user.is_superuser:
            return AnexoNotaFiscal.objects.all()
        return AnexoNotaFiscal.objects.filter(nota_fiscal__empresa=user.empresa)
    
    def perform_create(self, serializer):
        """Salva o usuário que criou o anexo"""
        arquivo = self.request.FILES.get('arquivo')
        serializer.save(
            criado_por=self.request.user,
            tamanho_arquivo=arquivo.size if arquivo else 0,
            tipo_arquivo=arquivo.content_type if arquivo else ''
        )
