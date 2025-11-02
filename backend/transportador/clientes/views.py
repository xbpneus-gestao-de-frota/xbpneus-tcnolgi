from rest_framework import viewsets, permissions, filters
from backend.common.permissions import OptionalRolePermission
from backend.common.audit import AuditedModelViewSet
from backend.common.export import export_csv, export_xlsx, export_csv_streaming
from rest_framework.decorators import action
from .models import Cliente, ContatoCliente
from .serializers import ClienteSerializer, ContatoClienteSerializer


class ClienteViewSet(AuditedModelViewSet):
    queryset = Cliente.objects.all().order_by('nome_razao_social')
    serializer_class = ClienteSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome_razao_social', 'nome_fantasia', 'cpf_cnpj']
    ordering_fields = ['nome_razao_social', 'criado_em']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['tipo', 'status']
    
    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        fmt = request.query_params.get("format", "csv")
        qs = self.filter_queryset(self.get_queryset())
        fields = ['id', 'nome_razao_social', 'cpf_cnpj', 'telefone', 'email', 'status']
        filename = f"clientes." + ("xlsx" if fmt == "xlsx" else "csv")
        if fmt == "xlsx":
            return export_xlsx(qs, fields, filename=filename)
        return export_csv_streaming(qs, fields, filename=filename) if request.query_params.get("stream") in {"1","true","True"} else export_csv(qs, fields, filename=filename)


class ContatoClienteViewSet(AuditedModelViewSet):
    queryset = ContatoCliente.objects.all().order_by('-principal', 'nome')
    serializer_class = ContatoClienteSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['cliente']
