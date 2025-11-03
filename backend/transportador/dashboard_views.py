"""Views de Dashboard e Perfil para Transportador."""
from datetime import timedelta
from typing import Any, Dict, Tuple

from django.db.models import F, Q
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.transportador.alertas.models import Alerta
from backend.transportador.estoque.models import MovimentacaoEstoque, StockMove
from backend.transportador.frota.models import Position, Vehicle
from backend.transportador.manutencao.models import (
    OrdemServico,
    StatusOS,
    Teste,
    WorkOrder,
)
from backend.transportador.pneus.models import Application, Tire


def collect_dashboard_payload(user) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    """Centraliza a coleta de dados usados pelos endpoints de dashboard."""

    empresa = getattr(user, "empresa", None)
    message = (
        "Nenhuma empresa associada ao usuário. Entre em contato com o administrador."
        if empresa is None
        else None
    )

    base_dashboard: Dict[str, Any] = {
        "usuario": {
            "email": user.email,
            "nome": getattr(user, "nome_razao_social", user.email),
            "tipo": "transportador",
            "empresa": getattr(empresa, "nome", None),
        },
        "frota": {
            "total_veiculos": 0,
            "veiculos_ativos": 0,
            "veiculos_manutencao": 0,
            "veiculos_inativos": 0,
            "precisam_manutencao": 0,
            "veiculos_alerta": [],
        },
        "pneus": {
            "total_posicoes": 0,
            "posicoes_ocupadas": 0,
            "posicoes_vazias": 0,
            "taxa_ocupacao": 0,
        },
        "manutencao": {
            "os_abertas": 0,
            "os_em_andamento": 0,
            "os_atrasadas": 0,
            "total_pendentes": 0,
            "ultimas_os": [],
        },
        "estoque": {
            "entradas_30d": 0,
            "saidas_30d": 0,
            "saldo_30d": 0,
            "ultimas_movimentacoes": [],
        },
        "alertas": {
            "veiculos_manutencao": 0,
            "os_atrasadas": 0,
            "veiculos_precisam_manutencao": 0,
        },
        "mensagem": message,
    }

    stats: Dict[str, Any] = {
        "veiculos_totais": 0,
        "veiculos_ativos": 0,
        "veiculos_manutencao": 0,
        "veiculos_inativos": 0,
        "pneus_em_uso": 0,
        "pneus_estoque": 0,
        "pneus_manutencao": 0,
        "os_abertas": 0,
        "os_em_andamento": 0,
        "os_concluidas_30d": 0,
        "alertas_ativos": 0,
    }

    metrics: Dict[str, Any] = {
        "vehicles": 0,
        "positions": 0,
        "tires": 0,
        "applications": 0,
        "stock_moves": 0,
        "work_orders": 0,
        "tests": 0,
    }

    if not empresa:
        return base_dashboard, stats, metrics

    veiculos = Vehicle.objects.filter(empresa=empresa)
    total_veiculos = veiculos.count()
    veiculos_ativos = veiculos.filter(status="ATIVO").count()
    veiculos_manutencao = veiculos.filter(status="MANUTENCAO").count()
    veiculos_inativos = veiculos.filter(status="INATIVO").count()

    veiculos_precisam_manutencao = veiculos.filter(
        km_proxima_manutencao__isnull=False,
        km__gte=F("km_proxima_manutencao"),
    ).count()

    veiculos_alerta_qs = veiculos.filter(
        km_proxima_manutencao__isnull=False,
        km__gte=F("km_proxima_manutencao") - 500,
        km__lt=F("km_proxima_manutencao"),
    ).order_by("km_proxima_manutencao")[:5]

    veiculos_alerta = [
        {
            "placa": v.placa,
            "modelo": str(v.modelo_veiculo) if v.modelo_veiculo else "",
            "km_atual": v.km,
            "km_proxima_manutencao": v.km_proxima_manutencao,
            "km_restante": max(0, (v.km_proxima_manutencao or 0) - v.km),
        }
        for v in veiculos_alerta_qs
    ]

    posicoes = Position.objects.filter(veiculo__empresa=empresa)
    total_posicoes = posicoes.count()
    posicoes_ocupadas = posicoes.exclude(
        Q(pneu_atual_codigo__isnull=True) | Q(pneu_atual_codigo__exact="")
    ).count()
    posicoes_vazias = total_posicoes - posicoes_ocupadas
    taxa_ocupacao = round((posicoes_ocupadas / total_posicoes * 100), 1) if total_posicoes else 0

    pneus_qs = Tire.objects.filter(empresa=empresa)
    pneus_em_uso = pneus_qs.filter(status="MONTADO").count()
    pneus_estoque = pneus_qs.filter(status="ESTOQUE").count()
    pneus_manutencao = pneus_qs.filter(status="MANUTENCAO").count()

    ordens_servico = OrdemServico.objects.filter(empresa=empresa)
    os_abertas = ordens_servico.filter(status=StatusOS.ABERTA).count()
    os_em_andamento = ordens_servico.filter(status=StatusOS.EM_ANDAMENTO).count()
    hoje = timezone.now()
    os_atrasadas = ordens_servico.filter(
        data_agendamento__isnull=False,
        data_agendamento__lt=hoje,
        status__in=[StatusOS.ABERTA, StatusOS.AGENDADA, StatusOS.EM_ANDAMENTO],
    ).count()
    total_pendentes = os_abertas + os_em_andamento
    os_concluidas_30d = ordens_servico.filter(
        status=StatusOS.CONCLUIDA,
        data_conclusao__isnull=False,
        data_conclusao__gte=hoje - timedelta(days=30),
    ).count()

    ultimas_os = [
        {
            "numero": os.numero,
            "veiculo_placa": os.veiculo.placa if os.veiculo else None,
            "tipo": os.tipo,
            "status": os.status,
            "prioridade": os.prioridade,
            "data_abertura": os.data_abertura.isoformat() if os.data_abertura else None,
        }
        for os in ordens_servico.select_related("veiculo").order_by("-data_abertura")[:5]
    ]

    data_30d_atras = hoje - timedelta(days=30)
    movimentacoes = MovimentacaoEstoque.objects.filter(
        produto__empresa=empresa,
        data_movimentacao__gte=data_30d_atras,
    )
    entradas_30d = movimentacoes.filter(tipo="ENTRADA").count()
    saidas_30d = movimentacoes.filter(tipo="SAIDA").count()
    saldo_30d = entradas_30d - saidas_30d

    ultimas_movimentacoes = [
        {
            "tipo": mov.tipo,
            "produto": mov.produto.descricao if mov.produto else None,
            "quantidade": float(mov.quantidade),
            "data": mov.data_movimentacao.isoformat() if mov.data_movimentacao else None,
            "documento": mov.documento_referencia,
        }
        for mov in (
            MovimentacaoEstoque.objects
            .filter(produto__empresa=empresa)
            .select_related("produto")
            .order_by("-data_movimentacao")[:5]
        )
    ]

    dashboard_data = {
        "usuario": {
            "email": user.email,
            "nome": getattr(user, "nome_razao_social", user.email),
            "tipo": "transportador",
            "empresa": empresa.nome if hasattr(empresa, "nome") else None,
        },
        "frota": {
            "total_veiculos": total_veiculos,
            "veiculos_ativos": veiculos_ativos,
            "veiculos_manutencao": veiculos_manutencao,
            "veiculos_inativos": veiculos_inativos,
            "precisam_manutencao": veiculos_precisam_manutencao,
            "veiculos_alerta": veiculos_alerta,
        },
        "pneus": {
            "total_posicoes": total_posicoes,
            "posicoes_ocupadas": posicoes_ocupadas,
            "posicoes_vazias": posicoes_vazias,
            "taxa_ocupacao": taxa_ocupacao,
        },
        "manutencao": {
            "os_abertas": os_abertas,
            "os_em_andamento": os_em_andamento,
            "os_atrasadas": os_atrasadas,
            "total_pendentes": total_pendentes,
            "ultimas_os": ultimas_os,
        },
        "estoque": {
            "entradas_30d": entradas_30d,
            "saidas_30d": saidas_30d,
            "saldo_30d": saldo_30d,
            "ultimas_movimentacoes": ultimas_movimentacoes,
        },
        "alertas": {
            "veiculos_manutencao": veiculos_manutencao,
            "os_atrasadas": os_atrasadas,
            "veiculos_precisam_manutencao": veiculos_precisam_manutencao,
        },
        "mensagem": None,
    }

    stats.update(
        {
            "veiculos_totais": total_veiculos,
            "veiculos_ativos": veiculos_ativos,
            "veiculos_manutencao": veiculos_manutencao,
            "veiculos_inativos": veiculos_inativos,
            "pneus_em_uso": pneus_em_uso,
            "pneus_estoque": pneus_estoque,
            "pneus_manutencao": pneus_manutencao,
            "os_abertas": os_abertas,
            "os_em_andamento": os_em_andamento,
            "os_concluidas_30d": os_concluidas_30d,
            "alertas_ativos": Alerta.objects.filter(ativo=True).count(),
        }
    )

    metrics.update(
        {
            "vehicles": total_veiculos,
            "positions": total_posicoes,
            "tires": pneus_qs.count(),
            "applications": Application.objects.filter(empresa=empresa).count(),
            "stock_moves": StockMove.objects.filter(produto__empresa=empresa).count(),
            "work_orders": WorkOrder.objects.count(),
            "tests": Teste.objects.count(),
        }
    )

    return dashboard_data, stats, metrics


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_view(request):
    """Endpoint com estatísticas consolidadas para o transportador."""

    dashboard_data, _, _ = collect_dashboard_payload(request.user)
    return Response(dashboard_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats_view(request):
    """Estatísticas agregadas para o dashboard avançado."""

    _, stats, _ = collect_dashboard_payload(request.user)
    return Response(stats)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    """
    Endpoint de perfil do usuário transportador
    GET: Retorna dados do perfil
    PUT/PATCH: Atualiza dados do perfil
    """
    user = request.user
    
    if request.method == 'GET':
        # Retornar dados do perfil
        profile_data = {
            'id': user.id,
            'email': user.email,
            'nome_razao_social': getattr(user, 'nome_razao_social', ''),
            'cnpj': getattr(user, 'cnpj', ''),
            'telefone': getattr(user, 'telefone', ''),
            'aprovado': getattr(user, 'aprovado', False),
            'is_active': user.is_active,
            'criado_em': getattr(user, 'criado_em', None),
            'aprovado_em': getattr(user, 'aprovado_em', None),
            'aprovado_por': getattr(user, 'aprovado_por', None),
            'tipo_usuario': 'transportador',
            'empresa_id': getattr(user, 'empresa_id', None)
        }
        
        # Converter datas para string
        if profile_data['criado_em']:
            profile_data['criado_em'] = profile_data['criado_em'].isoformat()
        if profile_data['aprovado_em']:
            profile_data['aprovado_em'] = profile_data['aprovado_em'].isoformat()
        
        return Response(profile_data)
    
    elif request.method in ['PUT', 'PATCH']:
        # Atualizar dados do perfil
        campos_permitidos = ['nome_razao_social', 'telefone']
        
        for campo in campos_permitidos:
            if campo in request.data:
                setattr(user, campo, request.data[campo])
        
        user.save()
        
        return Response({
            'message': 'Perfil atualizado com sucesso',
            'email': user.email,
            'nome_razao_social': getattr(user, 'nome_razao_social', '')
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    """
    Endpoint simplificado para retornar dados básicos do usuário logado
    """
    user = request.user
    
    user_data = {
        'id': user.id,
        'email': user.email,
        'nome': getattr(user, 'nome_razao_social', user.email),
        'tipo': 'transportador',
        'aprovado': getattr(user, 'aprovado', False),
        'is_active': user.is_active,
        'is_superuser': user.is_superuser
    }
    
    return Response(user_data)

