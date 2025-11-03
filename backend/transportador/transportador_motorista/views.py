"""Visões unificadas para motoristas internos e externos do transportador."""
from typing import Dict, List

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from backend.common.permissions import OptionalRolePermission
from backend.transportador.motorista_externo.models import MotoristaExterno
from backend.transportador.motorista_interno.models import MotoristaInterno

from .serializers import MotoristaTransportadorSerializer


class MotoristaTransportadorPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class MotoristaTransportadorViewSet(viewsets.ViewSet):
    """Agrupa motoristas internos e externos em uma única rota."""

    permission_classes = [permissions.IsAuthenticated, OptionalRolePermission]
    serializer_class = MotoristaTransportadorSerializer
    pagination_class = MotoristaTransportadorPagination

    def list(self, request):
        dataset = self._collect_dataset(request)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(dataset, request, view=self)
        serializer = self.serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        record = self._get_record(request.user, pk)
        serializer = self.serializer_class(record)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def resumo(self, request):
        dataset = self._collect_dataset(request, ignore_tipo=True)
        total = len(dataset)
        internos = sum(1 for item in dataset if item["tipo"] == "interno")
        externos = total - internos
        return Response({
            "total": total,
            "internos": internos,
            "externos": externos,
        })

    def _collect_dataset(self, request, *, ignore_tipo: bool = False) -> List[Dict[str, object]]:
        user = request.user
        empresa = getattr(user, "empresa", None)
        if empresa is None:
            return []

        tipo_param = (request.query_params.get("tipo") or "").lower()
        if ignore_tipo:
            tipo_param = ""

        include_internos = True
        include_externos = True
        if tipo_param in {"interno", "internos"}:
            include_externos = False
        elif tipo_param in {"externo", "externos"}:
            include_internos = False

        status_param = request.query_params.get("status")
        search_param = request.query_params.get("search")

        dataset: List[Dict[str, object]] = []

        if include_internos:
            internos_qs = MotoristaInterno.objects.filter(empresa=empresa)
            if status_param:
                internos_qs = internos_qs.filter(status=status_param.upper())
            if search_param:
                internos_qs = internos_qs.filter(
                    Q(nome_completo__icontains=search_param)
                    | Q(cpf__icontains=search_param)
                    | Q(cnh__icontains=search_param)
                )
            internos_qs = internos_qs.select_related("filial")
            dataset.extend(self._serialize_interno(obj) for obj in internos_qs)

        if include_externos:
            externos_qs = MotoristaExterno.objects.filter(empresa=empresa)
            if status_param:
                externos_qs = externos_qs.filter(status=status_param.upper())
            if search_param:
                externos_qs = externos_qs.filter(
                    Q(nome_completo__icontains=search_param)
                    | Q(cpf__icontains=search_param)
                    | Q(cnh__icontains=search_param)
                    | Q(email__icontains=search_param)
                )
            externos_qs = externos_qs.select_related("filial")
            dataset.extend(self._serialize_externo(obj) for obj in externos_qs)

        dataset.sort(key=lambda item: (item.get("nome") or "").lower())
        return dataset

    def _get_record(self, user, composite_id: str) -> Dict[str, object]:
        if not composite_id:
            raise Http404

        tipo, separator, raw_id = composite_id.partition(":")
        if separator != ":":
            raise Http404

        empresa = getattr(user, "empresa", None)
        if empresa is None:
            raise Http404

        tipo = tipo.lower()
        if tipo == "interno":
            try:
                pk_int = int(raw_id)
            except (TypeError, ValueError):
                raise Http404
            queryset = MotoristaInterno.objects.filter(empresa=empresa)
            motorista = get_object_or_404(queryset, pk=pk_int)
            return self._serialize_interno(motorista)

        if tipo == "externo":
            queryset = MotoristaExterno.objects.filter(empresa=empresa)
            motorista = get_object_or_404(queryset, pk=raw_id)
            return self._serialize_externo(motorista)

        raise Http404

    def _serialize_interno(self, motorista: MotoristaInterno) -> Dict[str, object]:
        return {
            "id": f"interno:{motorista.pk}",
            "tipo": "interno",
            "origem_id": str(motorista.pk),
            "nome": motorista.nome_completo,
            "cpf": motorista.cpf,
            "cnh": motorista.cnh,
            "status": motorista.status,
            "empresa_id": motorista.empresa_id,
            "filial_id": motorista.filial_id,
            "telefone": motorista.telefone,
            "email": motorista.email,
            "conectado_app": motorista.conectado_app,
            "ultimo_acesso_app": motorista.ultimo_acesso_app,
        }

    def _serialize_externo(self, motorista: MotoristaExterno) -> Dict[str, object]:
        return {
            "id": f"externo:{motorista.pk}",
            "tipo": "externo",
            "origem_id": str(motorista.pk),
            "nome": motorista.nome_completo,
            "cpf": motorista.cpf,
            "cnh": motorista.cnh,
            "status": motorista.status,
            "empresa_id": motorista.empresa_id,
            "filial_id": motorista.filial_id,
            "telefone": motorista.telefone,
            "email": motorista.email,
            "conectado_app": False,
            "ultimo_acesso_app": None,
            "aprovado": motorista.aprovado,
        }
