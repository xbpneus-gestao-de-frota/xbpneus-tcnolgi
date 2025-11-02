#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de Machine Learning para Previsão de Vida Útil e Análise Preditiva
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import os

class MachineLearningPneus:
    """
    Sistema de Machine Learning para análise preditiva de pneus
    """
    
    def __init__(self, db_path: str = 'problemas_pneus.db'):
        self.db_path = db_path
        self.conn = None
        
        # Parâmetros do modelo (baseados em conhecimento técnico)
        self.params = {
            'vida_util_base_km': 80000,  # Vida útil base para pneu de carga
            'desgaste_normal_mm_por_10k': 1.2,  # Desgaste normal
            'profundidade_minima_legal': 1.6,  # mm
            'profundidade_nova': 18.0,  # mm
        }
        
        # Fatores de ajuste baseados em condições
        self.fatores_ajuste = {
            'pressao': {
                'muito_baixa': 0.6,  # 40% mais desgaste
                'baixa': 0.8,
                'normal': 1.0,
                'alta': 0.85,
                'muito_alta': 0.7
            },
            'estrada': {
                'asfalto': 1.0,
                'terra': 0.7,
                'pedras': 0.5,
                'mista': 0.8
            },
            'posicao': {
                'DIRECAO': 1.0,
                'TRACAO': 0.85,  # Desgasta mais rápido
                'REBOQUE': 1.1   # Desgasta mais devagar
            },
            'carga': {
                'normal': 1.0,
                'sobrecarga_leve': 0.85,
                'sobrecarga_pesada': 0.6
            }
        }
    
    def prever_vida_util(self, dados_pneu: Dict) -> Dict:
        """
        Prevê a vida útil restante do pneu
        
        Args:
            dados_pneu: Dados do pneu incluindo:
                - km_rodados: Quilometragem atual
                - profundidade_sulco: Profundidade atual em mm
                - pressao_atual: Pressão atual
                - pressao_recomendada: Pressão recomendada
                - posicao: Posição do pneu
                - tipo_estrada: Tipo de estrada predominante
                - condicao_carga: Condição de carga
        
        Returns:
            Previsão detalhada
        """
        km_rodados = dados_pneu.get('km_rodados', 0)
        profundidade_atual = dados_pneu.get('profundidade_sulco', 10)
        
        # Calcular taxa de desgaste real
        desgaste_total = self.params['profundidade_nova'] - profundidade_atual
        if km_rodados > 0:
            taxa_desgaste_real = desgaste_total / (km_rodados / 10000)
        else:
            taxa_desgaste_real = self.params['desgaste_normal_mm_por_10k']
        
        # Ajustar taxa baseado em condições
        fator_total = self._calcular_fator_ajuste(dados_pneu)
        taxa_desgaste_ajustada = taxa_desgaste_real / fator_total
        
        # Calcular km restantes
        profundidade_restante = profundidade_atual - self.params['profundidade_minima_legal']
        if profundidade_restante <= 0:
            km_restantes = 0
        else:
            km_restantes = (profundidade_restante / taxa_desgaste_ajustada) * 10000
        
        # Calcular vida útil total esperada
        vida_util_total = km_rodados + km_restantes
        percentual_vida_util = (km_rodados / vida_util_total * 100) if vida_util_total > 0 else 100
        
        # Calcular data estimada de substituição
        km_medio_mes = dados_pneu.get('km_medio_mes', 5000)
        meses_restantes = km_restantes / km_medio_mes if km_medio_mes > 0 else 0
        data_substituicao = datetime.now() + timedelta(days=meses_restantes * 30)
        
        # Classificar eficiência
        eficiencia = self._classificar_eficiencia(
            vida_util_total,
            taxa_desgaste_real,
            fator_total
        )
        
        return {
            'km_restantes': int(km_restantes),
            'vida_util_total_estimada': int(vida_util_total),
            'percentual_vida_util_usado': round(percentual_vida_util, 1),
            'taxa_desgaste_mm_10k': round(taxa_desgaste_real, 2),
            'taxa_desgaste_ajustada': round(taxa_desgaste_ajustada, 2),
            'fator_ajuste_total': round(fator_total, 2),
            'data_substituicao_estimada': data_substituicao.strftime('%Y-%m-%d'),
            'meses_restantes': round(meses_restantes, 1),
            'eficiencia': eficiencia,
            'confianca': self._calcular_confianca_previsao(dados_pneu),
            'timestamp': datetime.now().isoformat()
        }
    
    def _calcular_fator_ajuste(self, dados_pneu: Dict) -> float:
        """
        Calcula fator de ajuste total baseado em todas as condições
        """
        fator = 1.0
        
        # Ajuste por pressão
        pressao_atual = dados_pneu.get('pressao_atual', 120)
        pressao_rec = dados_pneu.get('pressao_recomendada', 120)
        diferenca_pct = abs(pressao_atual - pressao_rec) / pressao_rec
        
        if diferenca_pct > 0.15:
            fator *= self.fatores_ajuste['pressao']['muito_baixa'] if pressao_atual < pressao_rec else self.fatores_ajuste['pressao']['muito_alta']
        elif diferenca_pct > 0.08:
            fator *= self.fatores_ajuste['pressao']['baixa'] if pressao_atual < pressao_rec else self.fatores_ajuste['pressao']['alta']
        
        # Ajuste por tipo de estrada
        tipo_estrada = dados_pneu.get('tipo_estrada', 'asfalto')
        fator *= self.fatores_ajuste['estrada'].get(tipo_estrada, 1.0)
        
        # Ajuste por posição
        posicao = dados_pneu.get('posicao', 'DIRECAO')
        fator *= self.fatores_ajuste['posicao'].get(posicao, 1.0)
        
        # Ajuste por carga
        condicao_carga = dados_pneu.get('condicao_carga', 'normal')
        fator *= self.fatores_ajuste['carga'].get(condicao_carga, 1.0)
        
        return fator
    
    def _classificar_eficiencia(self, vida_util_total: float, 
                                taxa_desgaste: float, 
                                fator_ajuste: float) -> str:
        """
        Classifica a eficiência do pneu
        """
        vida_base = self.params['vida_util_base_km']
        
        if vida_util_total >= vida_base * 1.2:
            return 'EXCELENTE'
        elif vida_util_total >= vida_base:
            return 'BOA'
        elif vida_util_total >= vida_base * 0.8:
            return 'REGULAR'
        elif vida_util_total >= vida_base * 0.6:
            return 'BAIXA'
        else:
            return 'MUITO_BAIXA'
    
    def _calcular_confianca_previsao(self, dados_pneu: Dict) -> float:
        """
        Calcula nível de confiança da previsão
        """
        confianca = 0.5
        
        # Aumentar confiança se houver mais dados
        if dados_pneu.get('km_rodados', 0) > 10000:
            confianca += 0.2
        if 'profundidade_sulco' in dados_pneu:
            confianca += 0.15
        if 'pressao_atual' in dados_pneu:
            confianca += 0.1
        if 'tipo_estrada' in dados_pneu:
            confianca += 0.05
        
        return min(confianca, 0.95)
    
    def analisar_tendencia_desgaste(self, historico: List[Dict]) -> Dict:
        """
        Analisa tendência de desgaste baseado em histórico
        
        Args:
            historico: Lista de medições históricas
                [{'data': '2024-01-01', 'profundidade': 15.0, 'km': 20000}, ...]
        
        Returns:
            Análise de tendência
        """
        if len(historico) < 2:
            return {
                'erro': 'Histórico insuficiente',
                'minimo_medicoes': 2
            }
        
        # Ordenar por data
        historico_ordenado = sorted(historico, key=lambda x: x['data'])
        
        # Calcular taxa de desgaste entre medições
        taxas = []
        for i in range(1, len(historico_ordenado)):
            atual = historico_ordenado[i]
            anterior = historico_ordenado[i-1]
            
            delta_prof = anterior['profundidade'] - atual['profundidade']
            delta_km = atual['km'] - anterior['km']
            
            if delta_km > 0:
                taxa = (delta_prof / delta_km) * 10000  # mm por 10k km
                taxas.append(taxa)
        
        # Calcular estatísticas
        taxa_media = sum(taxas) / len(taxas) if taxas else 0
        taxa_min = min(taxas) if taxas else 0
        taxa_max = max(taxas) if taxas else 0
        
        # Detectar aceleração do desgaste
        if len(taxas) >= 3:
            ultima_taxa = taxas[-1]
            media_anteriores = sum(taxas[:-1]) / len(taxas[:-1])
            aceleracao = ((ultima_taxa - media_anteriores) / media_anteriores * 100) if media_anteriores > 0 else 0
        else:
            aceleracao = 0
        
        # Classificar tendência
        if aceleracao > 20:
            tendencia = 'ACELERANDO_RAPIDO'
            alerta = 'ALTA'
        elif aceleracao > 10:
            tendencia = 'ACELERANDO'
            alerta = 'MEDIA'
        elif aceleracao < -10:
            tendencia = 'DESACELERANDO'
            alerta = 'BAIXA'
        else:
            tendencia = 'ESTAVEL'
            alerta = 'BAIXA'
        
        return {
            'total_medicoes': len(historico),
            'taxa_desgaste_media': round(taxa_media, 2),
            'taxa_minima': round(taxa_min, 2),
            'taxa_maxima': round(taxa_max, 2),
            'variacao_percentual': round(((taxa_max - taxa_min) / taxa_media * 100) if taxa_media > 0 else 0, 1),
            'aceleracao_percentual': round(aceleracao, 1),
            'tendencia': tendencia,
            'nivel_alerta': alerta,
            'recomendacao': self._gerar_recomendacao_tendencia(tendencia, aceleracao),
            'timestamp': datetime.now().isoformat()
        }
    
    def _gerar_recomendacao_tendencia(self, tendencia: str, aceleracao: float) -> str:
        """
        Gera recomendação baseada na tendência
        """
        if tendencia == 'ACELERANDO_RAPIDO':
            return 'URGENTE: Desgaste acelerando rapidamente. Investigar causas imediatamente (pressão, alinhamento, carga).'
        elif tendencia == 'ACELERANDO':
            return 'Desgaste acelerando. Verificar condições de operação e realizar manutenção preventiva.'
        elif tendencia == 'DESACELERANDO':
            return 'Desgaste desacelerando. Condições de operação melhoraram. Manter práticas atuais.'
        else:
            return 'Desgaste estável. Continuar monitoramento regular.'
    
    def correlacionar_problemas_mecanicos(self, 
                                         problemas_pneu: List[str],
                                         dados_veiculo: Dict) -> Dict:
        """
        Correlaciona problemas do pneu com possíveis problemas mecânicos
        
        Args:
            problemas_pneu: Lista de problemas identificados
            dados_veiculo: Dados do veículo (km, última manutenção, etc)
        
        Returns:
            Correlações identificadas
        """
        correlacoes = []
        
        # Mapeamento de problemas para causas mecânicas
        mapa_correlacao = {
            'Desgaste Unilateral': [
                {'componente': 'Alinhamento', 'probabilidade': 0.9, 'urgencia': 'ALTA'},
                {'componente': 'Suspensão', 'probabilidade': 0.6, 'urgencia': 'MEDIA'}
            ],
            'Desgaste Centralizado': [
                {'componente': 'Sistema de Calibragem', 'probabilidade': 0.85, 'urgencia': 'MEDIA'},
                {'componente': 'Válvulas', 'probabilidade': 0.4, 'urgencia': 'BAIXA'}
            ],
            'Desgaste nos Ombros': [
                {'componente': 'Sistema de Calibragem', 'probabilidade': 0.8, 'urgencia': 'MEDIA'},
                {'componente': 'Sobrecarga', 'probabilidade': 0.7, 'urgencia': 'ALTA'}
            ],
            'Desgaste em Concha': [
                {'componente': 'Amortecedores', 'probabilidade': 0.9, 'urgencia': 'ALTA'},
                {'componente': 'Balanceamento', 'probabilidade': 0.7, 'urgencia': 'MEDIA'}
            ],
            'Desgaste Diagonal': [
                {'componente': 'Alinhamento', 'probabilidade': 0.85, 'urgencia': 'ALTA'},
                {'componente': 'Rolamentos', 'probabilidade': 0.6, 'urgencia': 'MEDIA'}
            ],
            'Serrilhado': [
                {'componente': 'Convergência', 'probabilidade': 0.9, 'urgencia': 'ALTA'},
                {'componente': 'Terminais de Direção', 'probabilidade': 0.5, 'urgencia': 'MEDIA'}
            ]
        }
        
        # Buscar correlações
        for problema in problemas_pneu:
            if problema in mapa_correlacao:
                for causa in mapa_correlacao[problema]:
                    correlacoes.append({
                        'problema_pneu': problema,
                        'componente_mecanico': causa['componente'],
                        'probabilidade': causa['probabilidade'],
                        'urgencia': causa['urgencia'],
                        'acao_recomendada': self._gerar_acao_mecanica(causa)
                    })
        
        # Priorizar por urgência e probabilidade
        correlacoes.sort(key=lambda x: (
            ['BAIXA', 'MEDIA', 'ALTA'].index(x['urgencia']),
            x['probabilidade']
        ), reverse=True)
        
        # Gerar plano de ação
        plano_acao = self._gerar_plano_acao_mecanico(correlacoes, dados_veiculo)
        
        return {
            'total_correlacoes': len(correlacoes),
            'correlacoes': correlacoes,
            'plano_acao': plano_acao,
            'custo_estimado': self._estimar_custo_manutencao(correlacoes),
            'timestamp': datetime.now().isoformat()
        }
    
    def _gerar_acao_mecanica(self, causa: Dict) -> str:
        """
        Gera ação recomendada para problema mecânico
        """
        componente = causa['componente']
        urgencia = causa['urgencia']
        
        acoes = {
            'Alinhamento': 'Realizar alinhamento completo do eixo',
            'Suspensão': 'Inspecionar e substituir componentes desgastados da suspensão',
            'Sistema de Calibragem': 'Verificar e calibrar sistema de monitoramento de pressão',
            'Amortecedores': 'Testar e substituir amortecedores defeituosos',
            'Balanceamento': 'Realizar balanceamento das rodas',
            'Rolamentos': 'Inspecionar e substituir rolamentos com folga',
            'Convergência': 'Ajustar convergência das rodas',
            'Terminais de Direção': 'Inspecionar e substituir terminais desgastados',
            'Válvulas': 'Verificar e substituir válvulas defeituosas',
            'Sobrecarga': 'Revisar distribuição de carga e capacidade do veículo'
        }
        
        acao = acoes.get(componente, f'Inspecionar {componente}')
        
        if urgencia == 'ALTA':
            return f'URGENTE: {acao}'
        else:
            return acao
    
    def _gerar_plano_acao_mecanico(self, correlacoes: List[Dict], dados_veiculo: Dict) -> List[Dict]:
        """
        Gera plano de ação priorizado
        """
        plano = []
        componentes_unicos = set()
        
        for corr in correlacoes:
            comp = corr['componente_mecanico']
            if comp not in componentes_unicos:
                componentes_unicos.add(comp)
                plano.append({
                    'prioridade': len(plano) + 1,
                    'componente': comp,
                    'acao': corr['acao_recomendada'],
                    'urgencia': corr['urgencia'],
                    'prazo_dias': 7 if corr['urgencia'] == 'ALTA' else 30
                })
        
        return plano
    
    def _estimar_custo_manutencao(self, correlacoes: List[Dict]) -> Dict:
        """
        Estima custo de manutenção
        """
        custos_base = {
            'Alinhamento': 250,
            'Suspensão': 1500,
            'Sistema de Calibragem': 800,
            'Amortecedores': 2000,
            'Balanceamento': 150,
            'Rolamentos': 1200,
            'Convergência': 200,
            'Terminais de Direção': 600,
            'Válvulas': 100,
            'Sobrecarga': 0  # Ajuste operacional
        }
        
        total_min = 0
        total_max = 0
        
        componentes_unicos = set()
        for corr in correlacoes:
            comp = corr['componente_mecanico']
            if comp not in componentes_unicos:
                componentes_unicos.add(comp)
                custo_base = custos_base.get(comp, 500)
                total_min += custo_base * 0.8
                total_max += custo_base * 1.5
        
        return {
            'minimo': round(total_min, 2),
            'maximo': round(total_max, 2),
            'medio': round((total_min + total_max) / 2, 2),
            'moeda': 'BRL'
        }

def exemplo_uso():
    """Exemplo de uso do sistema de ML"""
    print("="*70)
    print("SISTEMA DE MACHINE LEARNING PARA ANÁLISE DE PNEUS")
    print("="*70 + "\n")
    
    ml = MachineLearningPneus()
    
    # Exemplo 1: Previsão de vida útil
    print("📊 EXEMPLO 1: Previsão de Vida Útil")
    print("-" * 70)
    
    dados_pneu = {
        'km_rodados': 45000,
        'profundidade_sulco': 8.5,
        'pressao_atual': 110,
        'pressao_recomendada': 120,
        'posicao': 'DIRECAO',
        'tipo_estrada': 'mista',
        'condicao_carga': 'normal',
        'km_medio_mes': 5000
    }
    
    previsao = ml.prever_vida_util(dados_pneu)
    print(f"KM restantes: {previsao['km_restantes']:,} km")
    print(f"Vida útil total: {previsao['vida_util_total_estimada']:,} km")
    print(f"Eficiência: {previsao['eficiencia']}")
    print(f"Data substituição: {previsao['data_substituicao_estimada']}")
    print(f"Confiança: {previsao['confianca']:.0%}")
    
    # Exemplo 2: Análise de tendência
    print("\n\n📈 EXEMPLO 2: Análise de Tendência de Desgaste")
    print("-" * 70)
    
    historico = [
        {'data': '2024-01-01', 'profundidade': 18.0, 'km': 0},
        {'data': '2024-03-01', 'profundidade': 15.5, 'km': 15000},
        {'data': '2024-06-01', 'profundidade': 12.0, 'km': 30000},
        {'data': '2024-09-01', 'profundidade': 8.5, 'km': 45000}
    ]
    
    tendencia = ml.analisar_tendencia_desgaste(historico)
    print(f"Taxa média: {tendencia['taxa_desgaste_media']} mm/10k km")
    print(f"Tendência: {tendencia['tendencia']}")
    print(f"Alerta: {tendencia['nivel_alerta']}")
    print(f"Recomendação: {tendencia['recomendacao']}")
    
    # Exemplo 3: Correlação com problemas mecânicos
    print("\n\n🔧 EXEMPLO 3: Correlação com Problemas Mecânicos")
    print("-" * 70)
    
    problemas = ['Desgaste Unilateral', 'Desgaste em Concha']
    dados_veiculo = {'km_total': 250000, 'ultima_manutencao': '2024-08-01'}
    
    correlacao = ml.correlacionar_problemas_mecanicos(problemas, dados_veiculo)
    print(f"Correlações encontradas: {correlacao['total_correlacoes']}")
    print(f"\nPlano de Ação:")
    for item in correlacao['plano_acao']:
        print(f"  {item['prioridade']}. {item['componente']} - {item['acao']}")
    
    custo = correlacao['custo_estimado']
    print(f"\nCusto estimado: R$ {custo['minimo']:.2f} - R$ {custo['maximo']:.2f}")
    
    print("\n" + "="*70)
    print("✅ Sistema de ML funcionando!")
    print("="*70)

if __name__ == "__main__":
    exemplo_uso()

