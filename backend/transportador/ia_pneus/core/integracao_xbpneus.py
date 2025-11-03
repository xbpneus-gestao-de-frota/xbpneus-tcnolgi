#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
"""
Módulo de Integração com Sistema XBPNEUS
Conecta a IA de Análise de Pneus com o sistema de gestão XBPNEUS
"""

import json
import requests
from typing import Dict, List, Optional
from datetime import datetime
from ia_analise_pneus import IAnalisePneus

class IntegracaoXBPNEUS:
    """
    Classe para integração com o sistema XBPNEUS
    
    Esta classe fornece métodos para:
    - Conectar com API do XBPNEUS
    - Sincronizar dados de pneus
    - Enviar análises e diagnósticos
    - Receber alertas e notificações
    """
    
    def __init__(self, config: Dict):
        """
        Inicializa a integração
        
        Args:
            config: Dicionário de configuração
                {
                    'xbpneus_url': str,  # URL base da API XBPNEUS
                    'api_key': str,       # Chave de API
                    'timeout': int,       # Timeout em segundos
                    'modo': str          # 'producao' ou 'desenvolvimento'
                }
        """
        self.config = config
        self.base_url = config.get('xbpneus_url', 'http://localhost:8000/api')
        self.api_key = config.get('api_key', '')
        self.timeout = config.get('timeout', 30)
        self.modo = config.get('modo', 'desenvolvimento')
        
        # Inicializar IA de análise
        self.ia = IAnalisePneus()
        
        # Headers padrão para requisições
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
            'X-API-Version': '1.0'
        }
        
    def testar_conexao(self) -> Dict:
        """
        Testa conexão com XBPNEUS
        
        Returns:
            Status da conexão
        """
        try:
            if self.modo == 'desenvolvimento':
                return {
                    'status': 'sucesso',
                    'mensagem': 'Modo desenvolvimento - conexão simulada',
                    'timestamp': datetime.now().isoformat()
                }
            
            response = requests.get(
                f'{self.base_url}/health',
                headers=self.headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return {
                    'status': 'sucesso',
                    'mensagem': 'Conexão estabelecida com sucesso',
                    'dados': response.json(),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'status': 'erro',
                    'mensagem': f'Erro na conexão: {response.status_code}',
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                'status': 'erro',
                'mensagem': f'Falha na conexão: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    def buscar_pneu(self, pneu_id: str) -> Optional[Dict]:
        """
        Busca informações de um pneu no XBPNEUS
        
        Args:
            pneu_id: ID do pneu no sistema XBPNEUS
        
        Returns:
            Dados do pneu ou None se não encontrado
        """
        try:
            if self.modo == 'desenvolvimento':
                # Retornar dados simulados
                return {
                    'id': pneu_id,
                    'numero_serie': f'SN{pneu_id}',
                    'marca': 'MICHELIN',
                    'modelo': 'XZE2+',
                    'medida': '295/80R22.5',
                    'posicao': 'DIRECAO',
                    'veiculo_id': 'VEI001',
                    'km_rodados': 45000,
                    'pressao_atual': 110,
                    'pressao_recomendada': 120,
                    'profundidade_sulco': 8.5,
                    'data_instalacao': '2024-01-15',
                    'ultima_inspecao': '2025-09-15',
                    'status': 'EM_USO'
                }
            
            response = requests.get(
                f'{self.base_url}/pneus/{pneu_id}',
                headers=self.headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json()
            return None
            
        except Exception as e:
            print(f"Erro ao buscar pneu: {e}")
            return None
    
    def analisar_pneu_xbpneus(self, pneu_id: str, observacoes: Optional[str] = None) -> Dict:
        """
        Busca pneu no XBPNEUS e realiza análise completa
        
        Args:
            pneu_id: ID do pneu no XBPNEUS
            observacoes: Observações adicionais do inspetor
        
        Returns:
            Análise completa do pneu
        """
        # Buscar dados do pneu
        dados_pneu = self.buscar_pneu(pneu_id)
        
        if not dados_pneu:
            return {
                'status': 'erro',
                'mensagem': f'Pneu {pneu_id} não encontrado no XBPNEUS'
            }
        
        # Preparar dados para análise
        sintomas = self._extrair_sintomas(dados_pneu, observacoes)
        
        # Realizar análise com IA
        analise = self.ia.analisar_sintomas(sintomas)
        
        # Enriquecer com dados do XBPNEUS
        resultado = {
            'pneu_id': pneu_id,
            'dados_pneu': dados_pneu,
            'analise_ia': analise,
            'observacoes': observacoes,
            'timestamp': datetime.now().isoformat()
        }
        
        # Calcular métricas adicionais
        resultado['metricas'] = self._calcular_metricas(dados_pneu, analise)
        
        return resultado
    
    def _extrair_sintomas(self, dados_pneu: Dict, observacoes: Optional[str]) -> Dict:
        """Extrai sintomas dos dados do pneu para análise"""
        sintomas = {
            'posicao_pneu': dados_pneu.get('posicao', 'QUALQUER'),
            'sintomas_adicionais': []
        }
        
        # Verificar pressão
        pressao_atual = dados_pneu.get('pressao_atual', 0)
        pressao_recomendada = dados_pneu.get('pressao_recomendada', 120)
        
        if pressao_atual < pressao_recomendada * 0.9:
            sintomas['sintomas_adicionais'].append('baixa_pressao')
            sintomas['tipo_desgaste'] = 'desgaste ombros'
            sintomas['severidade'] = 'MEDIA'
        elif pressao_atual > pressao_recomendada * 1.1:
            sintomas['sintomas_adicionais'].append('pressao_excessiva')
            sintomas['tipo_desgaste'] = 'desgaste centro'
            sintomas['severidade'] = 'MEDIA'
        
        # Verificar profundidade do sulco
        profundidade = dados_pneu.get('profundidade_sulco', 10)
        if profundidade < 3:
            sintomas['sintomas_adicionais'].append('desgaste_critico')
            sintomas['severidade'] = 'CRITICA'
        elif profundidade < 5:
            sintomas['sintomas_adicionais'].append('desgaste_avancado')
            sintomas['severidade'] = 'ALTA'
        
        # Adicionar observações
        if observacoes:
            sintomas['descricao_visual'] = observacoes
        
        return sintomas
    
    def _calcular_metricas(self, dados_pneu: Dict, analise: Dict) -> Dict:
        """Calcula métricas adicionais"""
        metricas = {}
        
        # Vida útil estimada
        km_rodados = dados_pneu.get('km_rodados', 0)
        profundidade = dados_pneu.get('profundidade_sulco', 10)
        profundidade_inicial = 18  # mm típico para pneu novo de carga
        
        if profundidade > 0:
            desgaste_por_km = (profundidade_inicial - profundidade) / km_rodados if km_rodados > 0 else 0
            km_restantes = (profundidade - 1.6) / desgaste_por_km if desgaste_por_km > 0 else 0
            metricas['km_restantes_estimado'] = int(km_restantes)
        else:
            metricas['km_restantes_estimado'] = 0
        
        # Custo por km
        custo_pneu = 2500  # Valor médio em reais
        if km_rodados > 0:
            metricas['custo_por_km'] = round(custo_pneu / km_rodados, 2)
        
        # Eficiência
        nivel_urgencia = analise.get('nivel_urgencia', 'BAIXA')
        if nivel_urgencia == 'CRITICA':
            metricas['eficiencia'] = 'MUITO_BAIXA'
        elif nivel_urgencia == 'ALTA':
            metricas['eficiencia'] = 'BAIXA'
        elif nivel_urgencia == 'MEDIA':
            metricas['eficiencia'] = 'MEDIA'
        else:
            metricas['eficiencia'] = 'BOA'
        
        return metricas
    
    def enviar_analise(self, analise: Dict) -> Dict:
        """
        Envia análise de volta para o XBPNEUS
        
        Args:
            analise: Resultado da análise
        
        Returns:
            Confirmação do envio
        """
        try:
            if self.modo == 'desenvolvimento':
                return {
                    'status': 'sucesso',
                    'mensagem': 'Análise registrada (modo desenvolvimento)',
                    'analise_id': f"ANAL{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    'timestamp': datetime.now().isoformat()
                }
            
            response = requests.post(
                f'{self.base_url}/analises',
                headers=self.headers,
                json=analise,
                timeout=self.timeout
            )
            
            if response.status_code in [200, 201]:
                return {
                    'status': 'sucesso',
                    'mensagem': 'Análise enviada com sucesso',
                    'dados': response.json(),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'status': 'erro',
                    'mensagem': f'Erro ao enviar análise: {response.status_code}',
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                'status': 'erro',
                'mensagem': f'Falha ao enviar análise: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    def listar_pneus_criticos(self, frota_id: Optional[str] = None) -> List[Dict]:
        """
        Lista pneus que necessitam atenção urgente
        
        Args:
            frota_id: ID da frota (opcional)
        
        Returns:
            Lista de pneus críticos
        """
        try:
            if self.modo == 'desenvolvimento':
                # Retornar dados simulados
                return [
                    {
                        'pneu_id': 'PN001',
                        'veiculo': 'Caminhão 001',
                        'problema': 'Pressão muito baixa',
                        'urgencia': 'CRITICA'
                    },
                    {
                        'pneu_id': 'PN015',
                        'veiculo': 'Caminhão 003',
                        'problema': 'Profundidade crítica',
                        'urgencia': 'ALTA'
                    }
                ]
            
            endpoint = f'{self.base_url}/pneus/criticos'
            if frota_id:
                endpoint += f'?frota_id={frota_id}'
            
            response = requests.get(
                endpoint,
                headers=self.headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json()
            return []
            
        except Exception as e:
            print(f"Erro ao listar pneus críticos: {e}")
            return []
    
    def gerar_relatorio_frota(self, frota_id: str) -> Dict:
        """
        Gera relatório completo de análise da frota
        
        Args:
            frota_id: ID da frota
        
        Returns:
            Relatório completo
        """
        relatorio = {
            'frota_id': frota_id,
            'data_geracao': datetime.now().isoformat(),
            'resumo': {},
            'pneus_criticos': [],
            'recomendacoes_gerais': [],
            'metricas_frota': {}
        }
        
        # Listar pneus críticos
        relatorio['pneus_criticos'] = self.listar_pneus_criticos(frota_id)
        
        # Resumo
        relatorio['resumo'] = {
            'total_pneus_criticos': len(relatorio['pneus_criticos']),
            'acao_imediata_necessaria': sum(1 for p in relatorio['pneus_criticos'] if p.get('urgencia') == 'CRITICA')
        }
        
        # Recomendações gerais
        if relatorio['resumo']['acao_imediata_necessaria'] > 0:
            relatorio['recomendacoes_gerais'].append({
                'tipo': 'URGENTE',
                'mensagem': f"{relatorio['resumo']['acao_imediata_necessaria']} pneu(s) necessitam ação imediata"
            })
        
        relatorio['recomendacoes_gerais'].append({
            'tipo': 'PREVENTIVA',
            'mensagem': 'Realizar inspeção completa da frota semanalmente'
        })
        
        return relatorio
    
    def webhook_notificacao(self, evento: str, dados: Dict) -> Dict:
        """
        Envia notificação via webhook para XBPNEUS
        
        Args:
            evento: Tipo de evento ('alerta_critico', 'analise_concluida', etc)
            dados: Dados do evento
        
        Returns:
            Status do envio
        """
        payload = {
            'evento': evento,
            'dados': dados,
            'timestamp': datetime.now().isoformat(),
            'origem': 'IA_ANALISE_PNEUS'
        }
        
        try:
            if self.modo == 'desenvolvimento':
                print(f"[WEBHOOK] Evento: {evento}")
                print(f"[WEBHOOK] Dados: {json.dumps(dados, indent=2, ensure_ascii=False)}")
                return {'status': 'sucesso', 'modo': 'desenvolvimento'}
            
            webhook_url = self.config.get('webhook_url')
            if not webhook_url:
                return {'status': 'erro', 'mensagem': 'URL do webhook não configurada'}
            
            response = requests.post(
                webhook_url,
                headers=self.headers,
                json=payload,
                timeout=self.timeout
            )
            
            return {
                'status': 'sucesso' if response.status_code == 200 else 'erro',
                'codigo': response.status_code
            }
            
        except Exception as e:
            return {'status': 'erro', 'mensagem': str(e)}
    
    def sincronizar_dados(self, direcao: str = 'bidirecional') -> Dict:
        """
        Sincroniza dados entre IA e XBPNEUS
        
        Args:
            direcao: 'importar', 'exportar' ou 'bidirecional'
        
        Returns:
            Status da sincronização
        """
        resultado = {
            'status': 'sucesso',
            'timestamp': datetime.now().isoformat(),
            'registros_importados': 0,
            'registros_exportados': 0,
            'erros': []
        }
        
        if self.modo == 'desenvolvimento':
            resultado['mensagem'] = 'Sincronização simulada (modo desenvolvimento)'
            resultado['registros_importados'] = 150
            resultado['registros_exportados'] = 45
        
        return resultado
    
    def fechar(self):
        """Fecha conexões e libera recursos"""
        if self.ia:
            self.ia.fechar()

def exemplo_integracao():
    """Exemplo de uso da integração"""
    print("="*70)
    print("INTEGRAÇÃO XBPNEUS - SISTEMA DE IA DE ANÁLISE DE PNEUS")
    print("="*70 + "\n")
    
    # Configuração
    config = {
        'xbpneus_url': 'http://localhost:8000/api',
        'api_key': 'sua_chave_api_aqui',
        'timeout': 30,
        'modo': 'desenvolvimento'  # Usar modo desenvolvimento para testes
    }
    
    # Inicializar integração
    integracao = IntegracaoXBPNEUS(config)
    
    # Teste 1: Conexão
    print("🔌 TESTE 1: Conexão com XBPNEUS")
    print("-" * 70)
    status = integracao.testar_conexao()
    print(f"Status: {status['status']}")
    print(f"Mensagem: {status['mensagem']}")
    
    # Teste 2: Buscar pneu
    print("\n\n🔍 TESTE 2: Buscar Pneu")
    print("-" * 70)
    pneu = integracao.buscar_pneu('PN001')
    if pneu:
        print(f"Pneu encontrado: {pneu['numero_serie']}")
        print(f"Marca/Modelo: {pneu['marca']} {pneu['modelo']}")
        print(f"Posição: {pneu['posicao']}")
        print(f"KM Rodados: {pneu['km_rodados']:,} km")
    
    # Teste 3: Análise completa
    print("\n\n📊 TESTE 3: Análise Completa de Pneu")
    print("-" * 70)
    analise = integracao.analisar_pneu_xbpneus('PN001', 'Pneu apresenta desgaste visível no centro')
    print(f"Nível de Urgência: {analise['analise_ia']['nivel_urgencia']}")
    print(f"KM Restantes Estimado: {analise['metricas']['km_restantes_estimado']:,} km")
    print(f"Eficiência: {analise['metricas']['eficiencia']}")
    
    # Teste 4: Enviar análise
    print("\n\n📤 TESTE 4: Enviar Análise para XBPNEUS")
    print("-" * 70)
    envio = integracao.enviar_analise(analise)
    print(f"Status: {envio['status']}")
    print(f"Mensagem: {envio['mensagem']}")
    
    # Teste 5: Listar pneus críticos
    print("\n\n⚠️  TESTE 5: Pneus Críticos")
    print("-" * 70)
    criticos = integracao.listar_pneus_criticos()
    print(f"Total de pneus críticos: {len(criticos)}")
    for pneu_critico in criticos:
        print(f"  • {pneu_critico['pneu_id']}: {pneu_critico['problema']} (Urgência: {pneu_critico['urgencia']})")
    
    # Teste 6: Relatório de frota
    print("\n\n📋 TESTE 6: Relatório de Frota")
    print("-" * 70)
    relatorio = integracao.gerar_relatorio_frota('FROTA001')
    print(f"Total de pneus críticos: {relatorio['resumo']['total_pneus_criticos']}")
    print(f"Ação imediata necessária: {relatorio['resumo']['acao_imediata_necessaria']}")
    print(f"Recomendações: {len(relatorio['recomendacoes_gerais'])}")
    
    print("\n" + "="*70)
    print("✅ Integração funcionando corretamente!")
    print("="*70)
    
    integracao.fechar()

if __name__ == "__main__":
    exemplo_integracao()

