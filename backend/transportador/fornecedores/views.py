from rest_framework import viewsets, permissions, filters
from backend.common.permissions import OptionalRolePermission
from backend.common.audit import AuditedModelViewSet
from backend.common.export import export_csv, export_xlsx, export_csv_streaming
from rest_framework.decorators import action
from .models import Fornecedor, ContatoFornecedor
from .serializers import FornecedorSerializer, ContatoFornecedorSerializer


class FornecedorViewSet(AuditedModelViewSet):
    queryset = Fornecedor.objects.all().order_by('nome_razao_social')
    serializer_class = FornecedorSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome_razao_social', 'nome_fantasia', 'cpf_cnpj']
    ordering_fields = ['nome_razao_social', 'avaliacao', 'criado_em']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['tipo', 'categoria', 'status']
    
    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        fmt = request.query_params.get("format", "csv")
        qs = self.filter_queryset(self.get_queryset())
        fields = ['id', 'nome_razao_social', 'cpf_cnpj', 'categoria', 'telefone', 'status']
        filename = f"fornecedores." + ("xlsx" if fmt == "xlsx" else "csv")
        if fmt == "xlsx":
            return export_xlsx(qs, fields, filename=filename)
        return export_csv_streaming(qs, fields, filename=filename) if request.query_params.get("stream") in {"1","true","True"} else export_csv(qs, fields, filename=filename)


class ContatoFornecedorViewSet(AuditedModelViewSet):
    queryset = ContatoFornecedor.objects.all().order_by('-principal', 'nome')
    serializer_class = ContatoFornecedorSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['fornecedor']
