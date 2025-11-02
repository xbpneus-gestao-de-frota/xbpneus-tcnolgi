"""
Views para o módulo de Configuracoes
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import ConfiguracaoSistema, ParametroEmpresa, PerfilUsuario, PermissaoCustomizada
from .serializers import ConfiguracaoSistemaSerializer, ParametroEmpresaSerializer, PerfilUsuarioSerializer, PermissaoCustomizadaSerializer


class ConfiguracaoSistemaViewSet(viewsets.ModelViewSet):
    """ViewSet para ConfiguracaoSistema"""
    permission_classes = [IsAuthenticated]
    serializer_class = ConfiguracaoSistemaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ConfiguracaoSistema.objects.all()
        return ConfiguracaoSistema.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class ParametroEmpresaViewSet(viewsets.ModelViewSet):
    """ViewSet para ParametroEmpresa"""
    permission_classes = [IsAuthenticated]
    serializer_class = ParametroEmpresaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ParametroEmpresa.objects.all()
        return ParametroEmpresa.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class PerfilUsuarioViewSet(viewsets.ModelViewSet):
    """ViewSet para PerfilUsuario"""
    permission_classes = [IsAuthenticated]
    serializer_class = PerfilUsuarioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return PerfilUsuario.objects.all()
        return PerfilUsuario.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class PermissaoCustomizadaViewSet(viewsets.ModelViewSet):
    """ViewSet para PermissaoCustomizada"""
    permission_classes = [IsAuthenticated]
    serializer_class = PermissaoCustomizadaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return PermissaoCustomizada.objects.all()
        return PermissaoCustomizada.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)





# =============================================================================
# VIEWSETS PARA TABELAS AUXILIARES
# =============================================================================

from .models import (
    CatalogoModeloVeiculo,
    MapaPosicaoPneu,
    OperacaoConfiguracao,
    MedidaPorPosicao,
    PressaoRecomendada,
    CatalogoPneuXBRI
)
from .serializers import (
    CatalogoModeloVeiculoSerializer,
    MapaPosicaoPneuSerializer,
    OperacaoConfiguracaoSerializer,
    MedidaPorPosicaoSerializer,
    PressaoRecomendadaSerializer,
    CatalogoPneuXBRISerializer
)


class CatalogoModeloVeiculoViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet somente leitura para CatalogoModeloVeiculo"""
    permission_classes = [IsAuthenticated]
    queryset = CatalogoModeloVeiculo.objects.all()
    serializer_class = CatalogoModeloVeiculoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'marca']
    search_fields = ['marca', 'familia_modelo', 'variante']
    ordering_fields = ['marca', 'familia_modelo', 'ano_inicio']
    ordering = ['marca', 'familia_modelo']


class MapaPosicaoPneuViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet somente leitura para MapaPosicaoPneu"""
    permission_classes = [IsAuthenticated]
    queryset = MapaPosicaoPneu.objects.all()
    serializer_class = MapaPosicaoPneuSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['config_id', 'componente', 'posicao_tipo']
    search_fields = ['config_id', 'position_id']
    ordering_fields = ['config_id', 'componente', 'eixo']
    ordering = ['config_id', 'componente', 'eixo']


class OperacaoConfiguracaoViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet somente leitura para OperacaoConfiguracao"""
    permission_classes = [IsAuthenticated]
    queryset = OperacaoConfiguracao.objects.all()
    serializer_class = OperacaoConfiguracaoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['op_code', 'implementos_recomendados']
    ordering_fields = ['op_code']
    ordering = ['op_code']


class MedidaPorPosicaoViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet somente leitura para MedidaPorPosicao"""
    permission_classes = [IsAuthenticated]
    queryset = MedidaPorPosicao.objects.all()
    serializer_class = MedidaPorPosicaoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['config_id', 'posicao_tipo']
    search_fields = ['config_id', 'medidas_tipicas']
    ordering_fields = ['config_id', 'posicao_tipo']
    ordering = ['config_id', 'posicao_tipo']


class PressaoRecomendadaViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet somente leitura para PressaoRecomendada"""
    permission_classes = [IsAuthenticated]
    queryset = PressaoRecomendada.objects.all()
    serializer_class = PressaoRecomendadaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'config_id', 'posicao_tipo']
    search_fields = ['medida_exemplo']
    ordering_fields = ['categoria', 'config_id']
    ordering = ['categoria', 'config_id']


class CatalogoPneuXBRIViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet somente leitura para CatalogoPneuXBRI"""
    permission_classes = [IsAuthenticated]
    queryset = CatalogoPneuXBRI.objects.all()
    serializer_class = CatalogoPneuXBRISerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['linha', 'modelo', 'medida']
    search_fields = ['linha', 'modelo', 'medida', 'linha_canonica']
    ordering_fields = ['linha', 'modelo', 'medida']
    ordering = ['linha', 'modelo', 'medida']

