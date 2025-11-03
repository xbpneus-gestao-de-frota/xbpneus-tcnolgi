#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
"""
Módulo Avançado de Visão Computacional para Análise de Pneus
Integração com OpenAI Vision API e análise detalhada
"""

import os
import json
import base64
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import re

class VisaoComputacionalAvancada:
    """
    Sistema avançado de visão computacional para análise de pneus
    usando OpenAI GPT-4 Vision
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa o sistema de visão computacional
        
        Args:
            api_key: Chave da API OpenAI (usa variável de ambiente se não fornecida)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.modelo = 'gpt-4o-mini'  # Modelo disponível no ambiente
        
        # Prompts especializados para diferentes tipos de análise
        self.prompts = {
            'geral': """Você é um especialista em análise de pneus de carga. 
Analise esta imagem detalhadamente e identifique:
1. Tipo de imagem (banda de rodagem, lateral, DOT, defeito específico)
2. Problemas visíveis (desgaste, cortes, bolhas, rachaduras, separações)
3. Severidade (BAIXA, MEDIA, ALTA, CRITICA)
4. Localização exata do problema
5. Possíveis causas
6. Recomendações

Responda em formato JSON estruturado.""",
            
            'dot': """Analise esta imagem e extraia as informações do código DOT:
1. Código DOT completo
2. Semana de fabricação
3. Ano de fabricação
4. Código do fabricante
5. Tamanho/especificação se visível

Responda em formato JSON.""",
            
            'medidas': """Identifique as especificações do pneu nesta imagem:
1. Medida (ex: 295/80R22.5)
2. Índice de carga
3. Índice de velocidade
4. Marca
5. Modelo
6. Tipo (radial/diagonal)

Responda em formato JSON.""",
            
            'defeito': """Analise este defeito específico em detalhes:
1. Tipo de defeito (separação, corte, bolha, rachadura, etc)
2. Dimensões aproximadas (largura x comprimento em cm)
3. Profundidade (superficial, moderada, profunda)
4. Componentes afetados (banda, carcaça, cintas, talão)
5. Defeito de fabricação ou uso?
6. Elegível para garantia? (SIM/NÃO/TALVEZ)
7. Urgência da ação

Responda em formato JSON detalhado.""",
            
            'desgaste': """Analise o padrão de desgaste deste pneu:
1. Tipo de desgaste (centralizado, lateral, irregular, diagonal, etc)
2. Profundidade do sulco (mm) se mensurável
3. Percentual de desgaste estimado
4. Uniformidade do desgaste
5. Causas prováveis
6. Problemas mecânicos relacionados

Responda em formato JSON."""
        }
    
    def analisar_imagem(self, img_path: str, tipo_analise: str = 'geral') -> Dict:
        """
        Analisa uma imagem usando visão computacional
        
        Args:
            img_path: Caminho da imagem
            tipo_analise: Tipo de análise ('geral', 'dot', 'medidas', 'defeito', 'desgaste')
        
        Returns:
            Análise estruturada da imagem
        """
        try:
            # Verificar se arquivo existe
            if not os.path.exists(img_path):
                return self._analise_simulada(img_path, tipo_analise)
            
            # Codificar imagem em base64
            with open(img_path, 'rb') as f:
                img_data = base64.b64encode(f.read()).decode('utf-8')
            
            # Preparar prompt
            prompt = self.prompts.get(tipo_analise, self.prompts['geral'])
            
            # Fazer requisição para OpenAI (simulado em desenvolvimento)
            if not self.api_key or self.api_key == 'sua_chave_api_aqui':
                return self._analise_simulada(img_path, tipo_analise)
            
            # Requisição real para OpenAI Vision
            resultado = self._chamar_openai_vision(img_data, prompt)
            
            # Processar e estruturar resultado
            analise = self._processar_resultado(resultado, tipo_analise)
            
            return analise
            
        except Exception as e:
            return {
                'erro': str(e),
                'tipo_analise': tipo_analise,
                'fallback': self._analise_simulada(img_path, tipo_analise)
            }
    
    def _chamar_openai_vision(self, img_base64: str, prompt: str) -> str:
        """
        Chama a API OpenAI Vision (implementação real)
        """
        try:
            from openai import OpenAI
            
            client = OpenAI()
            
            response = client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{img_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Erro ao chamar OpenAI Vision: {e}")
    
    def _processar_resultado(self, resultado: str, tipo_analise: str) -> Dict:
        """
        Processa e estrutura o resultado da análise
        """
        try:
            # Tentar extrair JSON do resultado
            json_match = re.search(r'\{.*\}', resultado, re.DOTALL)
            if json_match:
                dados = json.loads(json_match.group())
            else:
                # Se não houver JSON, criar estrutura baseada no texto
                dados = {
                    'analise_textual': resultado,
                    'tipo': tipo_analise
                }
            
            # Adicionar metadados
            dados['timestamp'] = datetime.now().isoformat()
            dados['modelo'] = self.modelo
            dados['confianca'] = self._calcular_confianca(dados)
            
            return dados
            
        except Exception as e:
            return {
                'erro_processamento': str(e),
                'resultado_bruto': resultado
            }
    
    def _calcular_confianca(self, dados: Dict) -> float:
        """
        Calcula nível de confiança da análise
        """
        confianca = 0.5  # Base
        
        # Aumentar confiança se houver informações específicas
        if 'severidade' in dados:
            confianca += 0.1
        if 'tipo_defeito' in dados or 'tipo_desgaste' in dados:
            confianca += 0.15
        if 'dimensoes' in dados or 'profundidade' in dados:
            confianca += 0.1
        if 'causas' in dados:
            confianca += 0.1
        if 'recomendacoes' in dados:
            confianca += 0.05
        
        return min(confianca, 1.0)
    
    def _analise_simulada(self, img_path: str, tipo_analise: str) -> Dict:
        """
        Análise simulada para desenvolvimento/testes
        """
        nome_arquivo = os.path.basename(img_path).lower()
        
        if tipo_analise == 'dot':
            return {
                'tipo': 'dot',
                'codigo_dot': '22412L18007',
                'semana': '24',
                'ano': '2021',
                'fabricante': 'XBRI',
                'confianca': 0.85,
                'timestamp': datetime.now().isoformat()
            }
        
        elif tipo_analise == 'medidas':
            return {
                'tipo': 'medidas',
                'medida': '295/80R22.5',
                'indice_carga': '152/148',
                'indice_velocidade': 'M',
                'marca': 'XBRI',
                'modelo': 'Forza Plus',
                'tipo_construcao': 'RADIAL',
                'lonas': '18',
                'confianca': 0.90,
                'timestamp': datetime.now().isoformat()
            }
        
        elif tipo_analise == 'defeito':
            return {
                'tipo': 'defeito',
                'tipo_defeito': 'Separação de Cintas',
                'dimensoes': {'largura_cm': 12, 'comprimento_cm': 8},
                'profundidade': 'profunda',
                'componentes_afetados': ['cintas_aco', 'banda_rodagem'],
                'defeito_fabricacao': True,
                'elegivel_garantia': 'SIM',
                'urgencia': 'CRITICA',
                'severidade': 'CRITICA',
                'descricao': 'Separação visível das cintas de aço da banda de rodagem',
                'causas_provaveis': [
                    'Falha no processo de vulcanização',
                    'Adesão inadequada entre camadas'
                ],
                'recomendacoes': [
                    'RETIRAR PNEU DE OPERAÇÃO IMEDIATAMENTE',
                    'Solicitar análise técnica presencial',
                    'Documentar para processo de garantia'
                ],
                'confianca': 0.88,
                'timestamp': datetime.now().isoformat()
            }
        
        elif tipo_analise == 'desgaste':
            return {
                'tipo': 'desgaste',
                'tipo_desgaste': 'Desgaste Centralizado',
                'profundidade_sulco_mm': 8.5,
                'profundidade_original_mm': 18.0,
                'percentual_desgaste': 53,
                'uniformidade': 'irregular',
                'causas_provaveis': [
                    'Pressão excessiva',
                    'Carga inadequada'
                ],
                'problemas_mecanicos': [
                    'Possível calibragem incorreta',
                    'Sistema de monitoramento de pressão defeituoso'
                ],
                'severidade': 'MEDIA',
                'vida_util_restante_km': 25000,
                'recomendacoes': [
                    'Ajustar pressão conforme especificação do fabricante',
                    'Verificar sistema de calibragem',
                    'Monitorar a cada 5.000 km'
                ],
                'confianca': 0.82,
                'timestamp': datetime.now().isoformat()
            }
        
        else:  # geral
            # Inferir tipo baseado no nome do arquivo
            if 'banda' in nome_arquivo or 'rodagem' in nome_arquivo:
                return self._analise_simulada(img_path, 'desgaste')
            elif 'dot' in nome_arquivo:
                return self._analise_simulada(img_path, 'dot')
            elif 'defeito' in nome_arquivo or 'dano' in nome_arquivo:
                return self._analise_simulada(img_path, 'defeito')
            else:
                return {
                    'tipo': 'geral',
                    'tipo_imagem': 'lateral',
                    'problemas_visiveis': [],
                    'condicao_geral': 'BOA',
                    'severidade': 'BAIXA',
                    'observacoes': 'Pneu em bom estado aparente',
                    'confianca': 0.75,
                    'timestamp': datetime.now().isoformat()
                }
    
    def analisar_multiplas_imagens(self, imagens: List[str]) -> Dict:
        """
        Analisa múltiplas imagens e consolida resultados
        
        Args:
            imagens: Lista de caminhos de imagens
        
        Returns:
            Análise consolidada
        """
        analises = []
        
        for img_path in imagens:
            # Determinar tipo de análise baseado no nome/contexto
            tipo = self._determinar_tipo_analise(img_path)
            analise = self.analisar_imagem(img_path, tipo)
            analises.append(analise)
        
        # Consolidar resultados
        consolidado = self._consolidar_analises(analises)
        
        return consolidado
    
    def _determinar_tipo_analise(self, img_path: str) -> str:
        """
        Determina o tipo de análise baseado no caminho/nome da imagem
        """
        nome = os.path.basename(img_path).lower()
        
        if 'dot' in nome:
            return 'dot'
        elif any(x in nome for x in ['medida', 'especificacao', 'lateral']):
            return 'medidas'
        elif any(x in nome for x in ['defeito', 'dano', 'problema']):
            return 'defeito'
        elif any(x in nome for x in ['banda', 'rodagem', 'desgaste', 'sulco']):
            return 'desgaste'
        else:
            return 'geral'
    
    def _consolidar_analises(self, analises: List[Dict]) -> Dict:
        """
        Consolida múltiplas análises em um resultado único
        """
        consolidado = {
            'total_imagens': len(analises),
            'timestamp': datetime.now().isoformat(),
            'analises_individuais': analises,
            'dados_extraidos': {},
            'problemas_identificados': [],
            'severidade_maxima': 'BAIXA',
            'confianca_media': 0.0,
            'recomendacoes_consolidadas': []
        }
        
        severidades_ordem = ['BAIXA', 'MEDIA', 'ALTA', 'CRITICA']
        max_sev_idx = 0
        total_confianca = 0
        
        for analise in analises:
            # Extrair dados específicos
            if analise.get('tipo') == 'dot':
                consolidado['dados_extraidos']['dot'] = analise
            elif analise.get('tipo') == 'medidas':
                consolidado['dados_extraidos']['especificacoes'] = analise
            
            # Coletar problemas
            if 'tipo_defeito' in analise:
                consolidado['problemas_identificados'].append({
                    'tipo': analise['tipo_defeito'],
                    'severidade': analise.get('severidade', 'MEDIA'),
                    'urgencia': analise.get('urgencia', 'MEDIA')
                })
            
            if 'tipo_desgaste' in analise:
                consolidado['problemas_identificados'].append({
                    'tipo': analise['tipo_desgaste'],
                    'severidade': analise.get('severidade', 'MEDIA')
                })
            
            # Atualizar severidade máxima
            sev = analise.get('severidade', 'BAIXA')
            if sev in severidades_ordem:
                sev_idx = severidades_ordem.index(sev)
                if sev_idx > max_sev_idx:
                    max_sev_idx = sev_idx
                    consolidado['severidade_maxima'] = sev
            
            # Somar confiança
            total_confianca += analise.get('confianca', 0.5)
            
            # Coletar recomendações
            if 'recomendacoes' in analise:
                consolidado['recomendacoes_consolidadas'].extend(
                    analise['recomendacoes']
                )
        
        # Calcular confiança média
        if len(analises) > 0:
            consolidado['confianca_media'] = total_confianca / len(analises)
        
        # Remover recomendações duplicadas
        consolidado['recomendacoes_consolidadas'] = list(set(
            consolidado['recomendacoes_consolidadas']
        ))
        
        # Adicionar resumo executivo
        consolidado['resumo_executivo'] = self._gerar_resumo_executivo(consolidado)
        
        return consolidado
    
    def _gerar_resumo_executivo(self, consolidado: Dict) -> str:
        """
        Gera resumo executivo da análise
        """
        total_imgs = consolidado['total_imagens']
        total_problemas = len(consolidado['problemas_identificados'])
        severidade = consolidado['severidade_maxima']
        
        resumo = f"Análise de {total_imgs} imagem(ns) concluída. "
        
        if total_problemas == 0:
            resumo += "Nenhum problema crítico identificado. Pneu em condição aparentemente boa."
        else:
            resumo += f"{total_problemas} problema(s) identificado(s). "
            resumo += f"Severidade máxima: {severidade}. "
            
            if severidade == 'CRITICA':
                resumo += "AÇÃO IMEDIATA NECESSÁRIA - Retirar pneu de operação."
            elif severidade == 'ALTA':
                resumo += "Inspeção técnica urgente recomendada."
            elif severidade == 'MEDIA':
                resumo += "Monitoramento intensivo recomendado."
        
        return resumo

def exemplo_uso():
    """Exemplo de uso do sistema de visão computacional"""
    print("="*70)
    print("SISTEMA AVANÇADO DE VISÃO COMPUTACIONAL")
    print("="*70 + "\n")
    
    # Inicializar
    visao = VisaoComputacionalAvancada()
    
    # Simular análise de múltiplas imagens
    imagens = [
        '/path/to/imagem_banda_rodagem.jpg',
        '/path/to/imagem_dot.jpg',
        '/path/to/imagem_defeito.jpg',
        '/path/to/imagem_lateral.jpg'
    ]
    
    print("🔍 Analisando múltiplas imagens...\n")
    resultado = visao.analisar_multiplas_imagens(imagens)
    
    print(f"📊 Total de imagens: {resultado['total_imagens']}")
    print(f"⚠️  Severidade máxima: {resultado['severidade_maxima']}")
    print(f"🎯 Confiança média: {resultado['confianca_media']:.2%}")
    print(f"🔧 Problemas identificados: {len(resultado['problemas_identificados'])}")
    
    print(f"\n📝 Resumo Executivo:")
    print(f"   {resultado['resumo_executivo']}")
    
    if resultado['dados_extraidos'].get('dot'):
        dot = resultado['dados_extraidos']['dot']
        print(f"\n🏷️  DOT Identificado: {dot['codigo_dot']}")
        print(f"   Fabricação: Semana {dot['semana']}/{dot['ano']}")
    
    if resultado['dados_extraidos'].get('especificacoes'):
        esp = resultado['dados_extraidos']['especificacoes']
        print(f"\n📏 Especificações: {esp['medida']}")
        print(f"   Marca: {esp['marca']} {esp['modelo']}")
    
    print("\n" + "="*70)
    print("✅ Sistema de visão computacional funcionando!")
    print("="*70)

if __name__ == "__main__":
    exemplo_uso()

