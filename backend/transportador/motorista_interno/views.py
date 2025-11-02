from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from backend.common.permissions import OptionalRolePermission
from backend.common.audit import AuditedModelViewSet
from backend.common.export import export_csv, export_xlsx, export_csv_streaming
from .models import (
    MotoristaInterno, VinculoMotoristaVeiculo, RegistroJornada,
    MensagemMotorista, AlertaMotorista
)
from .serializers import (
    MotoristaInternoSerializer, VinculoMotoristaVeiculoSerializer,
    RegistroJornadaSerializer, MensagemMotoristaSerializer, AlertaMotoristaSerializer
)


class MotoristaInternoViewSet(AuditedModelViewSet):
    queryset = MotoristaInterno.objects.all().order_by('nome_completo')
    serializer_class = MotoristaInternoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome_completo', 'cpf', 'cnh', 'telefone']
    ordering_fields = ['nome_completo', 'data_admissao', 'status']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['status', 'tipo_contrato', 'conectado_app']
    
    @action(detail=False, methods=['get'])
    def cnh_vencendo(self, request):
        """Lista motoristas com CNH vencendo em 30 dias"""
        from datetime import date, timedelta
        data_limite = date.today() + timedelta(days=30)
        motoristas = self.get_queryset().filter(
            validade_cnh__lte=data_limite,
            validade_cnh__gte=date.today(),
            status='ATIVO'
        )
        serializer = self.get_serializer(motoristas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def conectados_app(self, request):
        """Lista motoristas conectados ao app externo"""
        motoristas = self.get_queryset().filter(conectado_app=True, status='ATIVO')
        serializer = self.get_serializer(motoristas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def conectar_app(self, request, pk=None):
        """Conecta motorista ao app externo"""
        motorista = self.get_object()
        motorista_externo_id = request.data.get('motorista_externo_id')
        
        if not motorista_externo_id:
            return Response(
                {'error': 'motorista_externo_id é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        motorista.motorista_externo_id = motorista_externo_id
        motorista.conectado_app = True
        motorista.ultimo_acesso_app = timezone.now()
        motorista.save()
        
        return Response(self.get_serializer(motorista).data)
    
    @action(detail=True, methods=['post'])
    def desconectar_app(self, request, pk=None):
        """Desconecta motorista do app externo"""
        motorista = self.get_object()
        motorista.conectado_app = False
        motorista.save()
        
        return Response(self.get_serializer(motorista).data)
    
    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        fmt = request.query_params.get("format", "csv")
        qs = self.filter_queryset(self.get_queryset())
        fields = ['id', 'nome_completo', 'cpf', 'cnh', 'status', 'tipo_contrato']
        filename = f"motoristas." + ("xlsx" if fmt == "xlsx" else "csv")
        if fmt == "xlsx":
            return export_xlsx(qs, fields, filename=filename)
        return export_csv_streaming(qs, fields, filename=filename) if request.query_params.get("stream") in {"1","true","True"} else export_csv(qs, fields, filename=filename)


class VinculoMotoristaVeiculoViewSet(AuditedModelViewSet):
    queryset = VinculoMotoristaVeiculo.objects.all().order_by('-data_inicio')
    serializer_class = VinculoMotoristaVeiculoSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['motorista', 'veiculo', 'status']
    
    @action(detail=True, methods=['post'])
    def encerrar(self, request, pk=None):
        """Encerra um vínculo ativo"""
        vinculo = self.get_object()
        
        if vinculo.status != 'ATIVO':
            return Response(
                {'error': 'Apenas vínculos ativos podem ser encerrados'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        vinculo.status = 'INATIVO'
        vinculo.data_fim = timezone.now()
        vinculo.save()
        
        return Response(self.get_serializer(vinculo).data)


class RegistroJornadaViewSet(AuditedModelViewSet):
    queryset = RegistroJornada.objects.all().order_by('-data_hora')
    serializer_class = RegistroJornadaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['motorista__nome_completo', 'veiculo__placa']
    ordering_fields = ['data_hora']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['motorista', 'veiculo', 'tipo_registro', 'origem']
    
    @action(detail=False, methods=['post'])
    def registrar_app(self, request):
        """Endpoint para receber registros do app externo"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Atualizar último acesso do motorista
        motorista = serializer.validated_data['motorista']
        motorista.ultimo_acesso_app = timezone.now()
        motorista.save()
        
        serializer.save(origem='APP')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def jornada_hoje(self, request):
        """Lista registros de jornada de hoje"""
        from datetime import date
        hoje = date.today()
        registros = self.get_queryset().filter(data_hora__date=hoje)
        serializer = self.get_serializer(registros, many=True)
        return Response(serializer.data)


class MensagemMotoristaViewSet(AuditedModelViewSet):
    queryset = MensagemMotorista.objects.all().order_by('-data_envio')
    serializer_class = MensagemMotoristaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['motorista__nome_completo', 'assunto', 'mensagem']
    ordering_fields = ['data_envio']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['motorista', 'tipo', 'status']
    
    @action(detail=True, methods=['post'])
    def marcar_lida(self, request, pk=None):
        """Marca mensagem como lida"""
        mensagem = self.get_object()
        mensagem.status = 'LIDA'
        mensagem.data_leitura = timezone.now()
        mensagem.save()
        
        return Response(self.get_serializer(mensagem).data)
    
    @action(detail=False, methods=['get'])
    def nao_lidas(self, request):
        """Lista mensagens não lidas"""
        mensagens = self.get_queryset().filter(tipo='RECEBIDA').exclude(status='LIDA')
        serializer = self.get_serializer(mensagens, many=True)
        return Response(serializer.data)


class AlertaMotoristaViewSet(AuditedModelViewSet):
    queryset = AlertaMotorista.objects.all().order_by('-data_alerta', '-prioridade')
    serializer_class = AlertaMotoristaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['motorista__nome_completo', 'titulo', 'descricao']
    ordering_fields = ['data_alerta', 'prioridade']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['motorista', 'tipo', 'prioridade', 'status']
    
    @action(detail=True, methods=['post'])
    def resolver(self, request, pk=None):
        """Resolve um alerta"""
        alerta = self.get_object()
        resolvido_por = request.data.get('resolvido_por')
        observacoes = request.data.get('observacoes_resolucao', '')
        
        alerta.status = 'RESOLVIDO'
        alerta.data_resolucao = timezone.now()
        alerta.resolvido_por = resolvido_por
        alerta.observacoes_resolucao = observacoes
        alerta.save()
        
        return Response(self.get_serializer(alerta).data)
    
    @action(detail=False, methods=['get'])
    def abertos(self, request):
        """Lista alertas abertos"""
        alertas = self.get_queryset().filter(status='ABERTO')
        serializer = self.get_serializer(alertas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def urgentes(self, request):
        """Lista alertas urgentes"""
        alertas = self.get_queryset().filter(prioridade='URGENTE', status='ABERTO')
        serializer = self.get_serializer(alertas, many=True)
        return Response(serializer.data)
