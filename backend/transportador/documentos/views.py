from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.common.permissions import OptionalRolePermission
from backend.common.audit import AuditedModelViewSet
from .models import Documento
from .serializers import DocumentoSerializer

class DocumentoViewSet(AuditedModelViewSet):
    queryset = Documento.objects.all().order_by('data_validade')
    serializer_class = DocumentoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['numero', 'tipo']
    ordering_fields = ['data_validade', 'data_emissao']
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions, OptionalRolePermission]
    filterset_fields = ['veiculo', 'tipo', 'status']
    
    @action(detail=False, methods=['get'])
    def vencidos(self, request):
        docs = [d for d in self.get_queryset() if d.esta_vencido()]
        return Response(self.get_serializer(docs, many=True).data)
    
    @action(detail=False, methods=['get'])
    def vencendo(self, request):
        docs = [d for d in self.get_queryset() if d.esta_vencendo()]
        return Response(self.get_serializer(docs, many=True).data)
